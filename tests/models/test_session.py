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


@pytest.fixture(autouse=True, scope='class')
def redis_set():
    return redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))


@pytest.mark.usefixtures('redis_set')
class TestSession(object):

    @classmethod
    def setup_class(cls):
        r = redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")), password=os.environ.get("REDIS_PASS", None))
        r.flushall()
        ss = SessionStore(r, **dict(key_prefix='test'))

    def test_prefixed(self, redis_set):
        ss = SessionStore(redis_set, **dict(key_prefix='test'))
        prxd = ss.prefixed('testsid')

        assert prxd == 'test:testsid'

    def test_gen_sid(self, redis_set):
        ss = SessionStore(redis_set, **dict(key_prefix='test'))
        sid = ss.generate_sid()

        assert isinstance(sid, str)

    def test_set_session(self, redis_set):
        ss = SessionStore(redis_set, **dict(key_prefix='test', expire=0))
        ss.set_session('testsid', 'testname', 'testdata')
        data = redis_set.hget('test:testsid', 'testname')

        assert data == b'testdata'

    def test_set_session_with_expire(self, redis_set):
        ss = SessionStore(redis_set, **dict(key_prefix='test', expire=1000))
        ss.set_session('testsid', 'testname', 'testdata')
        data = redis_set.hget('test:testsid', 'testname')

        assert data == b'testdata'
        assert redis_set.ttl('test:testsid')

    def test_get_session(self, redis_set):
        ss = SessionStore(redis_set, **dict(key_prefix='test'))
        redis_set.hset('test:testsid', 'testname', 'testdata')
        data = ss.get_session('testsid', 'testname')

        assert 'testdata' == data

    def test_delete_session(self, redis_set):
        ss = SessionStore(redis_set, **dict(key_prefix='test'))
        ss.delete_session('testsid')

        assert redis_set.hgetall('testsid') == {}
