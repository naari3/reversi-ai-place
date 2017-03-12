# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web
import tornado.websocket
from tornado.web import HTTPError

from models import User, AccessToken

import re
import functools

token_pattern = r"Bearer ([a-zA-Z0-9=\+\/]+)"
token_repatter = re.compile(token_pattern)


class BaseAPIHandler(tornado.web.RequestHandler):

    def need_access_token(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_token_user()
            if user:
                method(self, *args, **kwargs)
            else:
                raise HTTPError(403)
        return wrapper

    def get_token_user(self):
        authorization = self.request.headers.get('Authorization', None)
        if authorization:
            match = token_repatter.match(authorization)
            if match:
                token = match.groups()[0]
                access_token = AccessToken(self.application.access_token_store).find_by_access_token(token)
                if access_token.user_id:
                    user = User.get(id=access_token.user_id)
                    return user
        return None


class BaseAPIWebSocketHandler(tornado.websocket.WebSocketHandler):

    def need_access_token(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_token_user()
            if user:
                method(self, *args, **kwargs)
            else:
                raise HTTPError(403)
        return wrapper

    def get_token_user(self):
        authorization = self.request.headers.get('Authorization', None)
        if authorization:
            match = token_repatter.match(authorization)
            if match:
                token = match.groups()[0]
                access_token = AccessToken(self.application.access_token_store).find_by_access_token(token)
                if access_token.user_id:
                    user = User.get(id=access_token.user_id)
                    return user
        return None
