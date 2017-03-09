# -*- coding: utf-8 -*-
import tornado.web
import json

from models import User, AccessToken
from .base import BaseHandler


class OAuthVerify(BaseHandler):

    def post(self):
        token = self.get_argument("access_token")
        access_token = AccessToken(self.application.access_token_store).find_by_access_token(token)
        data = access_token.verify()

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))
