import webapp2
from main import Handler

class AdminHandler(Handler):
    def get(self):
        self.render("admin.html")

