# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web

import uuid


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

    def save_current_user(self, user):
        sid = str(uuid.uuid4())
        self.set_secure_cookie("sid", sid)
