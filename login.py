import webapp2
from main import Handler


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")


app = webapp2.WSGIApplication([
    ('/login', LoginHandler)
], debug=True)