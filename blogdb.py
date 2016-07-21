from google.appengine.ext import db

class Entry(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    date = db.DateProperty(auto_now_add=True)
    category = db.StringProperty(required = True)
    enabled = db.BooleanProperty(required = True)