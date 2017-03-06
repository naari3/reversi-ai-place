# -*- coding: utf-8 -*-
import sys
from models import SessionStore, Session

import redis
import os
from os.path import join, dirname
from dotenv import load_dotenv
from functools import wraps

import pytest

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)


class TestSessionStore(object):

    @classmethod
    def setup_class(cls):
        cls.redis = redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")), password=os.environ.get("REDIS_PASS", None))
        cls.redis.flushall()

    def teardown_method(self):
        self.redis.flushall()

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

    def test_set_sessions(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test', expire=0))
        insert_data = {
            'testname1': 'testdata1',
            'testname2': 'testdata2'
        }
        ss.set_sessions('testsid', insert_data)
        data = self.redis.hgetall('test:testsid')

        assert data == {
            b'testname1': b'testdata1',
            b'testname2': b'testdata2',
        }

    def test_get_session(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        self.redis.hset('test:testsid', 'testname', 'testdata')
        data = ss.get_session('testsid', 'testname')

        assert 'testdata' == data

    def test_get_sessions(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        insert_data = {
            'testname1': 'testdata1',
            'testname2': 'testdata2'
        }
        self.redis.hmset('test:testsid', insert_data)
        data = ss.get_sessions('testsid')

        assert data == insert_data

    def test_delete_session(self):
        ss = SessionStore(self.redis, **dict(key_prefix='test'))
        ss.delete_session('testsid')

        assert self.redis.hgetall('testsid') == {}
