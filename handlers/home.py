# -*- coding: utf-8 -*-
import tornado.web
from .base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        self.render("index.pug", user=self.get_current_user())
