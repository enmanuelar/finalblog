from main import *
import blogdb, logging

class LoginHandler(Handler):
    @check_auth
    def get(self, **kwargs):
        self.render("login.html", user_logged=kwargs['user_logged'])

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        entity = blogdb.get_user(username)
        if entity:
            if validpw(password, entity.password):
                cookie = str(hash_cookie(username))
                self.response.headers.add_header('Set-Cookie', 'user=%s|%s; Path=/' % (cookie, entity.key().id()))
                self.redirect('/')
            else:
                #handle not match error
                self.redirect('/signup')
        else:
            self.redirect('/signup')

class LogoutHandler(Handler):
    def get(self):
        self.response.delete_cookie('user')
        self.redirect("/")
