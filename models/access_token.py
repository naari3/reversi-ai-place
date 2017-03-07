# -*- coding: utf-8 -*-
import os
import binascii
import base64

from .session import SessionStore
from .user import User


class AccessTokenStore(SessionStore):

    def __init__(self, redis_connection, options={}):
        self.options = {
            'key_prefix': 'access_token',
            'expire': 60 * 60,
        }
        self.options.update(options)
        super().__init__(redis_connection, **self.options)

    def get_expire(self, sid):
        return self.redis.ttl(self.prefixed(sid))


class AccessToken(object):

    def __init__(self, access_token_store, access_token=None, user_id=None):
        self.access_token_store = access_token_store
        self.access_token = access_token if access_token else self.generate_access_token()
        self.user_id = user_id if user_id else None

    def generate_access_token(self):
        return base64.b64encode(binascii.hexlify(os.urandom(128))).decode('utf-8')

    def find_by_access_token(self, access_token):
        user_id = self.access_token_store.get_session(access_token, 'user_id')
        return AccessToken(self.access_token_store, access_token, user_id)

    def save(self):
        return self.access_token_store.set_session(self.access_token, 'user_id', self.user_id)

    def refresh(self):
        self.access_token = self.generate_access_token()
        return self.save()

    def verify(self):
        expire = self.access_token_store.get_expire(self.access_token)
        return {
            'client_id': self.user_id,
            'expires_in': expire,
        }

    def revoke(self):
        pass
