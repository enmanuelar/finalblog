from main import *
import blogdb

class NewpostHandler(Handler):
    @check_auth
    def get(self, **kwargs):
        self.render("newpost.html", user_logged=kwargs['user_logged'], username=kwargs['username'])

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        category = self.request.get("category")
        username = self.request.get("hidden-username")
        content = "<br>".join(content.split("\n"))
        add_to_cache(title, title)
        entry = blogdb.Entry(title=title, content=content, user=username, category=category, enabled=True)
        entry_key = entry.put()
        self.redirect('/' + str(entry_key.id()))

