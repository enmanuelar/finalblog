import webapp2
from main import Handler


class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")


app = webapp2.WSGIApplication([
    ('/signup', SignupHandler)
], debug=True)