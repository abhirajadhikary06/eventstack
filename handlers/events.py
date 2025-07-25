import tornado.web
import json
import uuid
from datetime import datetime
from models.db import (
    create_event, get_event_by_id, get_events_by_user, 
    add_time_slot, get_time_slots_by_event, vote_for_slot,
    get_votes_by_event, add_comment, get_comments_by_event,
    finalize_event, update_event
)

class BaseAuthHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")
        if user_cookie:
            return json.loads(user_cookie)
        return None

class DashboardHandler(BaseAuthHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        created_events = get_events_by_user(user["id"], created_by=True)
        participated_events = get_events_by_user(user["id"], created_by=False)
        
        self.render("dashboard.html", 
                   user=user,
                   created_events=created_events,
                   participated_events=participated_events)

class EventCreateHandler(BaseAuthHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        self.render("create_event.html", user=user)
    
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        
        title = self.get_argument("title")
        description = self.get_argument("description", "")
        location = self.get_argument("location", "")
        time_slots = self.get_arguments("time_slots")
        
        if not title or not time_slots:
            self.render("create_event.html", 
                       user=user, 
                       error="Title and at least one time slot are required")
            return
        
        unlimited = self.get_argument("unlimited", "off") == "on"
        max_applicants_str = self.get_argument("max_applicants", "50")
        max_applicants = None if unlimited else int(max_applicants_str)

        # Create event
        event_id = str(uuid.uuid4())
        event = create_event(
            event_id=event_id,
            title=title,
            description=description,
            location=location,
            created_by=user["id"],
            max_applicants=max_applicants
        )
        
        # Add time slots
        for slot_datetime in time_slots:
            if slot_datetime.strip():
                add_time_slot(event_id, slot_datetime)
        
        self.redirect(f"/event/{event_id}")

class EventViewHandler(BaseAuthHandler):
    def get(self, event_id):
        user = self.get_current_user()
        event = get_event_by_id(event_id)
        
        if not event:
            raise tornado.web.HTTPError(404, "Event not found")
        
        time_slots = get_time_slots_by_event(event_id)
        votes = get_votes_by_event(event_id)
        comments = get_comments_by_event(event_id)
        
        # Organize votes by slot
        votes_by_slot = {}
        user_votes = {}
        for vote in votes:
            slot_id = vote["time_slot_id"]
            if slot_id not in votes_by_slot:
                votes_by_slot[slot_id] = []
            votes_by_slot[slot_id].append(vote)
            
            if user and vote["user_id"] == user["id"]:
                user_votes[slot_id] = True
        
        self.render("event.html",
                   event=event,
                   time_slots=time_slots,
                   votes_by_slot=votes_by_slot,
                   user_votes=user_votes,
                   comments=comments,
                   user=user)
    
    @tornado.web.authenticated
    def post(self, event_id):
        user = self.get_current_user()
        action = self.get_argument("action", "")
        
        if action == "comment":
            comment_text = self.get_argument("comment", "")
            if comment_text.strip():
                add_comment(event_id, user["id"], comment_text)
        
        elif action == "finalize":
            event = get_event_by_id(event_id)
            if event and event["created_by"] == user["id"]:
                slot_id = self.get_argument("slot_id", "")
                if slot_id:
                    finalize_event(event_id, slot_id)
        
        self.redirect(f"/event/{event_id}")

class EventVoteHandler(BaseAuthHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        event_id = self.get_argument("event_id")
        slot_id = self.get_argument("slot_id")
        action = self.get_argument("action", "vote")  # vote or unvote
        
        result = vote_for_slot(event_id, slot_id, user["id"], action == "vote")
        
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"success": result}))

class EventEditHandler(BaseAuthHandler):
    @tornado.web.authenticated
    def get(self, event_id):
        user = self.get_current_user()
        event = get_event_by_id(event_id)
        if not event or event["created_by"] != user["id"]:
            raise tornado.web.HTTPError(403, "Not authorized")
        self.render("edit_event.html", user=user, event=event)

    @tornado.web.authenticated
    def post(self, event_id):
        user = self.get_current_user()
        event = get_event_by_id(event_id)
        if not event or event["created_by"] != user["id"]:
            raise tornado.web.HTTPError(403, "Not authorized")

        title = self.get_argument("title")
        description = self.get_argument("description", "")
        location = self.get_argument("location", "")
        unlimited = self.get_argument("unlimited", "off") == "on"
        max_applicants_str = self.get_argument("max_applicants", "50")
        max_applicants = None if unlimited else int(max_applicants_str)

        updated_event = update_event(
            event_id=event_id,
            title=title,
            description=description,
            location=location,
            max_applicants=max_applicants
        )

        self.redirect(f"/event/{event_id}")
