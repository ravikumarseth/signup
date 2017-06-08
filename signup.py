import webapp2
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASS_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)

class MainPage(Handler):
    def get(self):
        self.render('signup_page.html', first_login="1")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_valid = username and valid_username(username)
        password_valid = password and valid_password(password)
        email_valid = email and valid_email(email)
        verify_valid = verify and (password == verify)

        if(username and username_valid and password and password_valid and verify and verify_valid):
            self.redirect('/welcome_page?username=' + username)
        else:
            self.render('signup_page.html', verify_valid = verify_valid, username = username, password = password, username_valid = username_valid, password_valid = password_valid)

class WelcomePage(Handler):
    def get(self):
        username = self.request.get("username")
        if (valid_username(username)):
            self.render("welcome_page.html", username=username)
        else:
            self.render('signup_page.html', first_login="1")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome_page', WelcomePage)
], debug=True)
