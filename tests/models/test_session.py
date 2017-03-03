# -*- coding: utf-8 -*-
import sys
from models import SessionStore

import redis
from os.path import join, dirname
from dotenv import load_dotenv

import pytest

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class TestSession(object):

    def __init__(self):
        self.redis = redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), password=os.environ.get("REDIS_PASS"))

    @classmethod
    def setup_class(self):
        self.redis.flushall()
        ss = SessionStore(self.redis, dict(key_prefix='test'))

    def test_prefixed(self):
        prxd = ss.prefixed('testsid')

        assert prxd == 'test:testsid'

    def test_gen_sid(self):
        sid = ss.generate_sid()

        assert isinstance(sid, str)

    def test_set_session(self):
        ss.set_session('testsid', 'testname', 'testdata')
        data = self.redis.hget('test:testsid', 'testname')

        assert data == b'testdata'

    def test_get_session(self):
        self.redis.hset('test:testsid', 'testname', 'testdata')
        data = ss.get_session('testsid', 'testname')

        assert 'testdata' == data

    def test_delete_session(self):
        ss.delete_session('testsid')

        assert self.redis.hgetall('testsid') == {}
