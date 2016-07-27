from main import *
import blogdb, logging

class EditHandler(Handler):
    @check_auth
    def get(self, *args, **kwargs):
        post_id = int(self.request.get('post_id'))
        entry = blogdb.get_single_entry(post_id)
        self.render('edit.html', entry=entry, user_logged=kwargs['user_logged'], username=kwargs['username'] )

    def post(self):
        post_id = int(self.request.get('post_id'))
        content = self.request.get('content')
        if content:
            content = "<br>".join(content.split("\n"))
        entry = blogdb.get_single_entry(post_id)
        entry.content = content
        entry.put()
        self.redirect('/')