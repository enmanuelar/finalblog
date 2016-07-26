import webapp2
from index import MainPage
from login import LoginHandler, LogoutHandler
from signup import SignupHandler
from admin import AdminHandler
from newpost import NewpostHandler
from post import PostHandler
from validation import ValidationHandler

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/signup', SignupHandler),
    ('/admin', AdminHandler),
    ('/newpost', NewpostHandler),
    ((r'/(\d+)'), PostHandler),
    ('/validation', ValidationHandler)
], debug=True)
