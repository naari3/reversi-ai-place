# -*- coding: utf-8 -*-
import tornado.auth
import tornado.escape
from tornado import gen
import tornado.web

import datetime

from .base import BaseHandler
from models import User


class AuthHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield gen.Task(self.get_authenticated_user)
            print(user)
            # user = yield self.get_authenticated_user()
            if not user:
                raise tornado.web.HTTPError(500, "Twitter auth failed")

            # exist = bool(list(User.select().where(User.twitter_id == user['id'])))
            reversi_user = User.get_or_create(twitter_id=user['id'])[0]
            reversi_user.name = user['name']
            reversi_user.save()

            self.save_current_user(user)
            self.redirect(self.get_argument("next", "/"))

        self.authenticate_redirect()
