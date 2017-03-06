# -*- coding: utf-8 -*-
from db import db
from peewee import *

import datetime


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):

    twitter_id = BigIntegerField()
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    # def __init__(self, user_data={}):
    #     self.twitter_id = user_data.get("twitter_id", None)
    #     self.name = user_data.get("name", None)
    #     self.created_at = user_data.get("created_at", None)
    #     self.updated_at = user_data.get("updated_at", None)
