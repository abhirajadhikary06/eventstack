import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import sqlite3
import json
from handlers.auth import GitHubAuthHandler, LoginHandler, LogoutHandler
from handlers.events import EventCreateHandler, EventViewHandler, EventVoteHandler, DashboardHandler
from handlers.websocket import VoteWebSocketHandler
from models.db import init_db

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        user_cookie = self.get_secure_cookie("user")
        user = None
        if user_cookie:
            try:
                user = json.loads(user_cookie)
                self.redirect("/dashboard")
                return
            except:
                pass
        
        self.render("index.html", user=user)

def make_app():
    # Initialize database
    init_db()
    
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/auth/github", GitHubAuthHandler),
        (r"/complete/github/?", GitHubAuthHandler),
        (r"/logout", LogoutHandler),
        (r"/dashboard", DashboardHandler),
        (r"/create", EventCreateHandler),
        (r"/event/([^/]+)", EventViewHandler),
        (r"/api/vote", EventVoteHandler),
        (r"/ws/vote/([^/]+)", VoteWebSocketHandler),
    ], 
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret=os.getenv("COOKIE_SECRET", "your-secret-key-change-in-production"),
    login_url="/login",
    debug=True
    )

if __name__ == "__main__":
    # Only run the Tornado server locally
    port = int(os.environ.get("PORT", 5000))
    app = make_app()
    app.listen(port, address="0.0.0.0")
    print(f"EventStack server running on http://localhost:{port}")
    tornado.ioloop.IOLoop.current().start()

