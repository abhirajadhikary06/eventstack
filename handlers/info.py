import tornado.web

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")

class PrivacyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("privacy.html")

class SupportHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("support.html")
