import webapp2
from main import *

class AdminHandler(Handler):
    @check_auth
    def get(self, **kwargs):
        self.render("admin.html", user_logged=kwargs['user_logged'])

