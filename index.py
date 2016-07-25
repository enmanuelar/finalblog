from main import Handler
import blogdb
from collections import namedtuple

class MainPage(Handler):
    def get_post_data(self, entries):
        post_list = []
        d = namedtuple('post',['id', 'title', 'date', 'category', 'content', 'comments_count'])
        for entry in entries:
            comments = blogdb.get_comments(entry.key().id())
            comments_count = 0
            if comments:
                comments_count = comments.count()
            post_data = d(entry.key().id(), entry.title, entry.date, entry.category, entry.content, comments_count)
            post_list.append(post_data)
        return  post_list

    def get(self):
        entries = blogdb.get_entries(0)
        post_data = self.get_post_data(entries)
        self.render("index.html", post_data=post_data)


    def post(self):
        current_page = self.request.get("page")
        entries = blogdb.get_entries(int(current_page))
        post_data = self.get_post_data(entries)
        self.render("more_posts.html", post_data=post_data)