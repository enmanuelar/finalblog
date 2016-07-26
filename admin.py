import webapp2, logging
from main import *
from itertools import groupby
from collections import namedtuple, Counter

class AdminHandler(Handler):
    @check_auth
    def get(self, **kwargs):
        posts = blogdb.get_admin_entries()
        post_id = blogdb.get_posts_id_by_comments()
        post_id_list = []
        l = []
        d = namedtuple('top_post', ['key', 'title', 'user', 'comments_count'])
        for post in post_id:
            if post.post_id in post_id_list:
                post_id_list.append((str(post.post_id)))
            else:
                post_id_list.append((str(post.post_id)))
        for key, group in groupby(post_id_list):
            entry = blogdb.get_single_entry(int(key))
            l.append([d(key, entry.title, entry.user, len(list(group)))])
        l.sort(key=lambda comment: comment[0].comments_count, reverse=True)
        self.render("admin.html", posts=posts, top_posts=l[:5], user_logged=kwargs['user_logged'])

