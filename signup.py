from main import Handler
import webapp2_extras.appengine.auth.models as auth_models
from google.appengine.ext import ndb


class User(auth_models.User):
    email = ndb.StringProperty()

class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")

