import webapp2, logging
from main import *
from itertools import groupby
from collections import namedtuple
from json import JSONEncoder

def get_top_categories():
    d = namedtuple('top_tags',['category', 'comments_count'])
    entities = blogdb.get_categories_by_comments()
    entity_l = [(e.category, e.post_id) for e in entities]
    entity_l.sort()
    top_categories = [d(category, len(list(post_id))) for category, post_id in groupby(entity_l, lambda x: x[0])]
    top_categories.sort(key=lambda comment: comment.comments_count, reverse=True)
    return top_categories

class AdminHandler(Handler):
    def get_top_posts(self):
        comments = blogdb.get_comments_sorted_by_post_id()
        post_id_list = []
        l = []
        d = namedtuple('top_post', ['id', 'title', 'user', 'category', 'comments_count'])
        for comment in comments:
            if comment.post_id in post_id_list:
                post_id_list.append((str(comment.post_id)))
            else:
                post_id_list.append((str(comment.post_id)))
        for key, group in groupby(post_id_list):
            entry = blogdb.get_single_entry(int(key))
            l.append([d(key, entry.title, entry.user, entry.category, len(list(group)))])
        l.sort(key=lambda comment: comment[0].comments_count, reverse=True)
        return l


    @check_auth
    def get(self, **kwargs):
        posts = blogdb.get_admin_entries()
        top_posts_l = self.get_top_posts()
        top_categories = get_top_categories()
        self.render("admin.html", posts=posts, top_posts=top_posts_l[:5], top_categories=top_categories, user_logged=kwargs['user_logged'], username=kwargs['username'])

    def post(self):
        post_id = int(self.request.get("post_id"))
        status = self.request.get("status")
        entity = blogdb.Entry.get_by_id(post_id)
        if status == "true":
            entity.enabled = False
        else:
            entity.enabled = True
        entity.put()

class ChartsHandler(Handler):
    def get(self):
        ##Categories order in charts ["Random", "Music", "Science", "Technology", "Funny"]
        top_categories = get_top_categories()
        l = [0, 0, 0, 0, 0]
        total = 0
        for c in top_categories:
            i = {'random': 0, 'music': 1, 'science': 2, 'technology': 3, 'funny': 4}.get(c.category)
            l[i] = {'random': c.comments_count,
                    'music': c.comments_count,
                    'science': c.comments_count,
                    'technology': c.comments_count,
                    'funny': c.comments_count}.get(c.category)
            #total += c.comments_count
        ##CONVERTS COUNT TO PERCENTAGE
        #for i in range(len(l)):
        #    l[i] = (l[i] * 100) / total
        response = JSONEncoder().encode({'data': l})
        self.response.out.write(response)