from google.appengine.api import memcache


##CACHE
def get_post_title_cache(title):
    return memcache.get(title)

def add_post_title_cache(title):
    memcache.set(title, title)