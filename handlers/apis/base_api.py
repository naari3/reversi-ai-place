# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web

from models import User, AccessToken

import re
import functools

token_pattern = r"Bearer ([a-zA-Z0-9=\+\/]+)"
token_repatter = re.compile(token_pattern)


class BaseAPIHandler(tornado.web.RequestHandler):

    def need_access_token(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            authorization = self.headers.get('Authorization', None)
            if authorization:
                user = self.get_current_user(authorization)
                if user:
                    method(self, *args, **kwargs)
            raise HTTPError(403)
        return wrapper

    def get_token_user(self, authorization):
        match = token_repatte.match(authorization)
        if match:
            token = match.groups()[0]
            access_token = AccessToken.find_by_access_token(token)
            if access_token.user_id:
                user = User.get(user_id=access_token.user_id)
                return user
        return None
