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
import webapp2, os, jinja2, blogdb, logging, utils
from collections import namedtuple



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






app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
