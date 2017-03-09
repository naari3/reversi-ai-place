# -*- coding: utf-8 -*-
import sys
from models import AccessToken, AccessTokenStore

import redis
import os
from os.path import join, dirname
from dotenv import load_dotenv

import pytest

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)


class TestAccessToken(object):

    @classmethod
    def setup_class(cls):
        cls.redis = redis.StrictRedis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")), password=os.environ.get("REDIS_PASS", None))
        cls.redis.flushall()
        cls.access_token_store = AccessTokenStore(cls.redis, dict(key_prefix='test', expire=3600))

    def test_generate_access_token(self):
        assert isinstance(AccessToken(self.access_token_store).generate_access_token(), str)

    def test_initialize(self):
        user_id = 1
        access_token = AccessToken(self.access_token_store, user_id=user_id)

        assert isinstance(access_token.access_token, str)
        assert access_token.user_id == user_id

    def test_find_by_access_token(self):
        pass

    def test_save(self):
        pass

    def test_refresh(self):
        pass

    def test_verify(self):
        pass

    def test_revoke(self):
        pass
