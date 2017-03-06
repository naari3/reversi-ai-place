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


class TestSession(object):

    @classmethod
    def setup_class(cls):
        cls.redis = redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")), password=os.environ.get("REDIS_PASS", None))
        cls.redis.flushall()
        cls.session_store = SessionStore(cls.redis, **dict(key_prefix='test', expire=0))

    def test_initialize(self):
        session = Session(self.session_store)
        assert isinstance(session.session_id, str)

        sid = 'test'
        session = Session(self.session_store, sid)
        assert session.session_id == sid

    def test_save(self):
        session = Session(self.session_store)
        pass

    def test_delete(self):
        session = Session(self.session_store)
        pass
