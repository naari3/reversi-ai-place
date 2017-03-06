# -*- coding: utf-8 -*-
import sys
from models import User

import redis
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime

import pytest

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)


class TestUser(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_init(self):
        datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = User(
            twitter_id=1,
            created_at=datetime_str,
            updated_at=datetime_str,
        )

        assert user.twitter_id == 1
        assert user.name is None
        assert user.created_at == datetime_str
        assert user.updated_at == datetime_str
