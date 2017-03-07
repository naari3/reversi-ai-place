# -*- coding: utf-8 -*-
import tornado.auth
import tornado.escape
from tornado import gen
import tornado.web

import datetime

from .base import BaseHandler
from models import User


class AuthHandler(BaseHandler, tornado.auth.TwitterMixin):
    @gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            if not user:
                return tornado.web.HTTPError(500, "Twitter auth failed")

            reversi_user = User.get_or_create(twitter_id=user['id'])[0]
            reversi_user.name = user['name']
            reversi_user.save()

            self.save_current_user(reversi_user)
            self.redirect(self.get_argument("next", "/"))
        else:
            yield self.authorize_redirect(callback_uri=self.request.full_url())

        self.authenticate_redirect()
