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
        data = self.redis.hget(self.prefixed(sid), name)
        data = data.decode('utf-8') if data else None
        return data

    def get_sessions(self, sid):
        data = self.redis.hgetall(self.prefixed(sid))
        data = dict((item[0].decode('utf-8'), item[1].decode('utf-8')) for item in data.items()) if data else None
        return data

    def set_session(self, sid, name, data):
        expire = self.options['expire']
        response = self.redis.hset(self.prefixed(sid), name, data)
        if expire and response:
            return self.redis.expire(self.prefixed(sid), expire)
        else:
            return response

    def set_sessions(self, sid, data):
        expire = self.options['expire']
        response = self.redis.hmset(self.prefixed(sid), data)
        if expire and response:
            return self.redis.expire(self.prefixed(sid), expire)
        else:
            return response

    def delete_session(self, sid):
        return self.redis.delete(self.prefixed(sid))


class Session(object):

    def __init__(self, session_store, session_id=None):
        self.store = session_store
        self.session_id = session_id if session_id else self.store.generate_sid()
        self.data = {}
        if session_id:
            self.data = self.store.get_sessions(self.session_id)

    def save(self):
        self.store.set_sessions(self.session_id, self.data)
