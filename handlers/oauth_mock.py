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


class OAuthAccessToken(BaseHandler):

    def post(self):
        handle_type = self.get_argument("grant_type")
        if handle_type == 'refresh_token':
            refresh_token = self.get_argument("refresh_token")
            client_id = self.get_argument("client_id")
            client_secret = self.get_argument("client_secret")

            access_token = AccessToken(self.application.access_token_store).refresh(refresh_token)

            data = {
                'token_type': 'Bearer',
                'access_token': access_token.access_token,
                'expires_in': access_token.access_token_store.options.expire,
                'refresh_token': access_token.refresh_token,
            }

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))


class OAuthRevoke(BaseHandler):

    def post(self):
        refresh_token = self.get_argument("refresh_token")
        access_token = AccessToken(self.application.access_token_store).refresh(refresh_token)
        access_token.revoke()

        self.write('')
