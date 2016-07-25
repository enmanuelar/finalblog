#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, os, jinja2, blogdb, logging, utils, codecs
from google.appengine.ext import db
from collections import namedtuple
from json import JSONEncoder


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get_post_data(self, entries):
        post_list = []
        d = namedtuple('post',['id', 'title', 'date', 'category', 'content', 'comments_count'])
        for entry in entries:
            comments = blogdb.get_comments(entry.key().id())
            comments_count = 0
            if comments:
                comments_count = comments.count()
            post_data = d(entry.key().id(), entry.title, entry.date, entry.category, entry.content, comments_count)
            post_list.append(post_data)
        return  post_list

    def get(self):
        entries = blogdb.get_entries(0)
        post_data = self.get_post_data(entries)
        self.render("index.html", post_data=post_data)


    def post(self):
        current_page = self.request.get("page")
        entries = blogdb.get_entries(int(current_page))
        post_data = self.get_post_data(entries)
        self.render("more_posts.html", post_data=post_data)

class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

class NewpostHandler(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        category = self.request.get("category")
        content = "<br>".join(content.split("\n"))
        utils.add_post_title_cache(title)
        entry = blogdb.Entry(title=title, content=content, category=category, enabled=True)
        entry_key = entry.put()
        self.redirect('/' + str(entry_key.id()))


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

class ArticleHandler(Handler):
    def get(self, *args):
        post_url = self.request.url
        post_id = int(post_url.split('/')[-1])
        entity = blogdb.Entry.get_by_id(post_id)
        comments = blogdb.get_comments(post_id)
        if comments:
            self.render("post.html", article_id=post_id, entry=entity, comments=comments)
        else:
            self.render("post.html", article_id=post_id, entry=entity)

    def post(self, *args):
        user = self.request.get('user')
        content = self.request.get('content')
        if user and content:
            post_id = int(self.request.url.split('/')[-1])
            comment_entity = blogdb.Comments(user=user, content=content, post_id=post_id)
            comment_entity.put()

class AdminHandler(Handler):
    def get(self):
        self.render("admin.html")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignupHandler),
    ('/login', LoginHandler),
    ('/newpost', NewpostHandler),
    ('/validation', ValidationHandler),
    ((r'/(\d+)'), ArticleHandler),
    ('/admin', AdminHandler)
], debug=True)
