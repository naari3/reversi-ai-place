# -*- coding: utf-8 -*-
import os
import random

from pypugjs.ext.tornado import patch_tornado

import tornado.httpserver
import tornado.ioloop
from tornado import options
from tornado import template
import tornado.web
import tornado.websocket
from tornado.web import url

patch_tornado()

import json

from handles import HomeHandler, BoardHandler

class Application(tornado.web.Application):
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        handlers = [
            url(r'/', HomeHandler, name='home'),
            url(r'/v1/board/([0-9]+)', BoardHandler, name='board'),
        ]
        settings = dict(
            template_path=os.path.join(BASE_DIR, 'templates'),
            static_path=os.path.join(BASE_DIR, 'static'),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
