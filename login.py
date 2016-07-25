from main import Handler


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")


