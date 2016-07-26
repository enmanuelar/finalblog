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
import webapp2, os, jinja2, hashlib, random, string, logging
from google.appengine.api import memcache


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

##CACHE
##FOR POSTS USE TITLE AS KEY, FOR USERS USE USERNAME AS KEY
def get_from_cache(key):
    return memcache.get(key)

##FOR POSTS USE TITLE AS KEY AND VALUE, FOR USERS USE USERNAME AS KEY AND ENTITY KEY AS VALUE
def add_to_cache(key, value):
    memcache.set(key, value)

## HASHING FUNCTIONS
secret = 'salvnnlKLKNjfasmvkmnvKNLOcxre'

def hashpw(password):
    h = hashlib.sha256(password + secret).hexdigest()
    return h


def validpw(password, compare):
    if hashpw(password) == compare:
        return True


def hash_cookie(username):
    h = hashpw(username)
    return "%s" % (h)


def check_secure_val(hashed_password, user_input):
    if validpw(hashed_password, user_input):
        return True
    else:
        return None

def check_cookie(self):
    cookie = self.request.cookies.get('user')
    if cookie:
        return True

##DECORATORS
def check_auth(func):
    def func_wrapper(*args, **kwargs):
        if check_cookie(*args):
            kwargs['user_logged'] = True
        else:
            kwargs['user_logged'] = False
        return func(*args, **kwargs)
    return func_wrapper




