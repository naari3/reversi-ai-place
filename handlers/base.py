# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web

from models import User, SessionStore, Session


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        sid = self.get_secure_cookie("sid")
        session = Session(self.application.session_store, sid)
        user = User.get(twitter_id=session.data['twitter_id'])
        if not user:
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
