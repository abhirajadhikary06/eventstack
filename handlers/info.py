import tornado.web

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html", user=None, upcoming_events=[], flash_messages=[])

class PrivacyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("privacy.html", user=None, upcoming_events=[], flash_messages=[])

class SupportHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("support.html", user=None, upcoming_events=[], flash_messages=[])

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("contact.html", success=None, user=None, upcoming_events=[], flash_messages=[])

    def post(self):
        name = self.get_argument("name")
        email = self.get_argument("email")
        subject = self.get_argument("subject")
        msg_type = self.get_argument("type", "Feedback")
        message = self.get_argument("message")

        # Optional: store to DB or send email
        print(f"[Contact] {msg_type} - {subject} from {name} <{email}>:\n{message}")

        self.render("contact.html", success="Thank you! Your message has been received.", user=None, upcoming_events=[], flash_messages=[])
