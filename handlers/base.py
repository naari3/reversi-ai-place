# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web

from models import User, Session


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        sid = self.get_secure_cookie("sid")
        if not sid:
            return None
        sid = sid.decode('utf-8')
        session = Session(self.application.session_store, sid)
        if session.data.get('twitter_id'):
            user = User.get(twitter_id=session.data['twitter_id'])
        else:
            return None

        return user
        # return tornado.escape.json_decode(sid)

    def save_current_user(self, user):
        session = Session(self.application.session_store)
        session.data = user.fields()
        session.save()
        self.set_secure_cookie("sid", session.session_id)

    def destroy_current_user(self, user):
        self.set_secure_cookie("sid", '')
