from google.appengine.ext import db

class Entry(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    user = db.StringProperty(required=False)
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
    category = db.StringProperty(required=False)

class Users(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty(required=False)

def get_entries(page):
    limit = 4
    offset = limit * page
    return db.GqlQuery("SELECT * FROM Entry WHERE enabled = TRUE ORDER BY created DESC LIMIT %d OFFSET %d" %(limit, offset))

def get_posts_count_by_category(*args):
    l = []
    for c in args:
        l.append((db.Query(Entry).filter('category =', c).count()))
    return l

def get_admin_entries():
    return db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC")

def get_comments(post_id):
    return db.GqlQuery("SELECT * FROM Comments WHERE post_id = %d ORDER BY created DESC" % (post_id))

def get_single_entry(post_id):
    return Entry.get_by_id(post_id)

def get_comments_sorted_by_post_id():
    return Comments.all().order('-post_id').run()

def get_categories_by_comments():
    return Comments.all().order('-post_id').run()

def get_user(username):
    return  db.Query(Users).filter('username =', username).get()

def get_user_by_id(user_id):
    return Users.get_by_id(user_id)