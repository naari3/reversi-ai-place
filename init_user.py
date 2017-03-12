# -*- coding: utf-8 -*-
from models import User

User.create_table()

User.create(id=1, twitter_id=1, name='one')
User.create(id=2, twitter_id=2, name='two')
User.create(id=3, twitter_id=3, name='thr')
