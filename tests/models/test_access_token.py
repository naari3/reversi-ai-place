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
        user_id = '1'
        access_token = AccessToken(self.access_token_store, user_id=user_id)

        assert isinstance(access_token.access_token, str)
        assert access_token.user_id == user_id

    def test_save(self):
        user_id = '1'
        access_token = AccessToken(self.access_token_store, user_id=user_id)
        access_token.save()

        fetched_user_id = self.access_token_store.get_session(access_token.access_token, 'user_id')

        assert user_id == fetched_user_id

    def test_find_by_access_token(self):
        user_id = '1'
        access_token = AccessToken(self.access_token_store, user_id=user_id)
        access_token.save()

        at = AccessToken(self.access_token_store).find_by_access_token(access_token.access_token)

        assert at.user_id == access_token.user_id
        assert at.access_token == access_token.access_token
        assert at.refresh_token == access_token.refresh_token

    def test_prefixed_for_refresh(self):
        result = AccessToken.prefixed_for_refresh('aa')
        assert result == 'refresh_token:aa'

    def test_refresh(self):
        user_id = '1'
        access_token = AccessToken(self.access_token_store, user_id=user_id)
        access_token.save()

        at = AccessToken(self.access_token_store).refresh(access_token.refresh_token)

        assert at.user_id == access_token.user_id
        assert at.access_token != access_token.access_token
        assert at.refresh_token != access_token.refresh_token

        fail_at = AccessToken(self.access_token_store).find_by_access_token(access_token.access_token)
        assert fail_at.user_id is None

    def test_verify(self):
        user_id = '1'
        access_token = AccessToken(self.access_token_store, user_id=user_id)
        access_token.save()

        fetched_data = access_token.verify()

        assert fetched_data['client_id'] == user_id
        assert 0 <= fetched_data['expires_in'] <= 3600

    def test_revoke(self):
        pass
