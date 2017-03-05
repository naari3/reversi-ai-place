# -*- coding: utf-8 -*-
import sys
from models import SessionStore

import redis
import os
from os.path import join, dirname
from dotenv import load_dotenv
from functools import wraps

import pytest

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)


class TestSession(object):

    @classmethod
    def setup_class(cls):
        cls.redis = redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")), password=os.environ.get("REDIS_PASS", None))
        cls.redis.flushall()

    def test_prefixed(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        prxd = ss.prefixed('testsid')

        assert prxd == 'test:testsid'

    def test_gen_sid(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        sid = ss.generate_sid()

        assert isinstance(sid, str)

    def test_set_session(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test', expire=0))
        ss.set_session('testsid', 'testname', 'testdata')
        data = self.redis.hget('test:testsid', 'testname')

        assert data == b'testdata'

    def test_set_session_with_expire(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test', expire=1000))
        ss.set_session('testsid', 'testname', 'testdata')
        data = self.redis.hget('test:testsid', 'testname')

        assert data == b'testdata'
        assert self.redis.ttl('test:testsid')

    def test_get_session(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        self.redis.hset('test:testsid', 'testname', 'testdata')
        data = ss.get_session('testsid', 'testname')

        assert 'testdata' == data

    def test_delete_session(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        ss.delete_session('testsid')

        assert self.redis.hgetall('testsid') == {}
