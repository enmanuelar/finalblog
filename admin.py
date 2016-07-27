import webapp2, logging
from main import *
from itertools import groupby
from collections import namedtuple, Counter

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

    def get_top_categories(self):
        d = namedtuple('top_tags',['category', 'comments_count'])
        entities = blogdb.get_categories_by_comments()
        entity_l = [(e.category, e.post_id) for e in entities]
        entity_l.sort()
        top_categories = [d(category, len(list(post_id))) for category, post_id in groupby(entity_l, lambda x: x[0])]
        top_categories.sort(key=lambda comment: comment.comments_count, reverse=True)
        return top_categories


    @check_auth
    def get(self, **kwargs):
        posts = blogdb.get_admin_entries()
        top_posts_l = self.get_top_posts()
        top_categories = self.get_top_categories()
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