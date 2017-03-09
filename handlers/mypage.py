# -*- coding: utf-8 -*-
import tornado.web

from models import User, AccessToken
from .base import BaseHandler


class MyPageHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        access_token = AccessToken(self.application.access_token_store, user_id=user.id)
        data = {
            "user": user,
            "access_token": access_token,
        }
        self.render("mypage.pug", **data)

    @tornado.web.authenticated
    def post(self):
        pass
