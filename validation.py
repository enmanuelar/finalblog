import webapp2
from main import Handler
from json import JSONEncoder
import utils

class ValidationHandler(Handler):
    def post(self):
        title = self.request.get("title")
        cached_title = utils.get_post_title_cache(title)
        if cached_title:
            response = JSONEncoder().encode({"valid_title": False})
            self.response.out.write(response)
        elif title and not cached_title:
            response = JSONEncoder().encode({"valid_title": True})
            self.response.out.write(response)


app = webapp2.WSGIApplication([
    ('/validation', ValidationHandler)
], debug=True)