from main import *
import blogdb, logging

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        entity = blogdb.get_user(username)
        if entity:
            if validpw(password, entity.password):
                logging.error("GFGSDFGDFPGSKGPKRWET$%$$$$$$$$$")
                cookie = str(hash_cookie(username))
                self.response.headers.add_header('Set-Cookie', 'user=%s|%s; Path=/' % (cookie, entity.key().id()))
                self.redirect('/')
            else:
                #handle not match error
                self.redirect('/signup')
        else:
            self.redirect('/signup')

