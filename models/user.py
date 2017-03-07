# -*- coding: utf-8 -*-
from db import db
from peewee import *

import datetime


class User(Model):

    class Meta:
        database = db

    twitter_id = BigIntegerField()
    name = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def fields(self):
        return {
            'id': self.id,
            'twitter_id': self.twitter_id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
