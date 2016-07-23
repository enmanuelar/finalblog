from google.appengine.ext import db

class Entry(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    date = db.DateProperty(auto_now_add=True)
    category = db.StringProperty(required=True)
    enabled = db.BooleanProperty(required=True)

class Comments(db.Model):
    user = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date = db.DateProperty(auto_now_add=True)
    created = db.DateTimeProperty(auto_now_add=True)
    post_id = db.IntegerProperty(required=True)

def get_entries(page):
    limit = 3
    offset = limit * page
    return db.GqlQuery("SELECT * FROM Entry WHERE enabled = TRUE ORDER BY created DESC LIMIT %d OFFSET %d" %(limit, offset))

def get_comments(post_id):
    return db.GqlQuery("SELECT * FROM Comments WHERE post_id = %d ORDER BY created DESC" % (post_id))