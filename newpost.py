from main import *
import blogdb

class NewpostHandler(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        category = self.request.get("category")
        content = "<br>".join(content.split("\n"))
        add_to_cache(title, title)
        entry = blogdb.Entry(title=title, content=content, category=category, enabled=True)
        entry_key = entry.put()
        self.redirect('/' + str(entry_key.id()))

