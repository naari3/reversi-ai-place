# -*- coding: utf-8 -*-
import uuid


class SessionStore(object):

    def __init__(self, redis_connection, **options):
        self.options = {
            'key_prefix': 'session',
            'expire': 30 * 60 * 60 * 24,
        }
        self.options.update(options)
        self.redis = redis_connection

    def prefixed(self, sid):
        return f'{self.options["key_prefix"]}:{sid}'

    def generate_sid(self):
        return uuid.uuid4().hex

    def get_session(self, sid, name):
        return self.redis.hget(self.prefixed(sid), name).decode('utf-8')

    def set_session(self, sid, name, data):
        expire = self.options['expire']
        response = self.redis.hset(self.prefixed(sid), name, data)
        if expire:
            return self.redis.expire(self.prefixed(sid), expire) and response
        else:
            return response

    def delete_session(self, sid):
        return self.redis.delete(self.prefixed(sid))
