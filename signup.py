from main import *
from json import JSONEncoder
import blogdb

class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        email = self.request.get("email")
        validation = self.request.get("validation")
        if get_from_cache(username) and validation == "true":
            response = JSONEncoder().encode({"status": False})
            self.response.out.write(response)
        else:
            response = JSONEncoder().encode({"status": True})
            self.response.out.write(response)
        if validation == "false":
            hash_pw = hashpw(password)
            if email:
                user = blogdb.Users(username=username, password=hash_pw, email=email)
            else:
                user = blogdb.Users(username=username, password=hash_pw)
            user_key = user.put()
            add_to_cache(username, user_key)
            cookie = str(hash_cookie(username))
            self.response.headers.add_header('Set-Cookie', 'user=%s|%s; Path=/' % (cookie, user_key.id()))
            self.redirect("/")
