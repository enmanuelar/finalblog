import webapp2
from main import Handler
import blogdb

class PostHandler(Handler):
    def get(self, *args):
        post_url = self.request.url
        post_id = int(post_url.split('/')[-1])
        entity = blogdb.Entry.get_by_id(post_id)
        comments = blogdb.get_comments(post_id)
        if comments:
            self.render("post.html", article_id=post_id, entry=entity, comments=comments)
        else:
            self.render("post.html", article_id=post_id, entry=entity)

    def post(self, *args):
        user = self.request.get('user')
        content = self.request.get('content')
        if user and content:
            post_id = int(self.request.url.split('/')[-1])
            comment_entity = blogdb.Comments(user=user, content=content, post_id=post_id)
            comment_entity.put()


app = webapp2.WSGIApplication([
    ((r'/(\d+)'), PostHandler)
], debug=True)