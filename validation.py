from main import *
from json import JSONEncoder


class ValidationHandler(Handler):
    def post(self):
        title = self.request.get("title")
        cached_title = get_post_title_cache(title)
        if cached_title:
            response = JSONEncoder().encode({"valid_title": False})
            self.response.out.write(response)
        elif title and not cached_title:
            response = JSONEncoder().encode({"valid_title": True})
            self.response.out.write(response)


