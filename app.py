# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv

import random

from pypugjs.ext.tornado import patch_tornado

import tornado.httpserver
import tornado.ioloop
from tornado import options
from tornado import template
import tornado.web
import tornado.websocket
from tornado.web import url

import json

from handlers import HomeHandler, BoardHandler, BoardWebSocketHandler, AuthHandler

patch_tornado()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Application(tornado.web.Application):

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        handlers = [
            url(r'/', HomeHandler, name='home'),
            url(r"/auth/login", AuthHandler, name='auth_login'),
            url(r'/v1/board/([0-9]+)', BoardHandler, name='board'),
            url(r'/v1/board/([0-9]+)/ws', BoardWebSocketHandler, name='board_ws'),
        ]
        settings = dict(
            template_path=os.path.join(BASE_DIR, 'templates'),
            static_path=os.path.join(BASE_DIR, 'static'),
            twitter_consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
            twitter_consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
            debug=True,
            cookie_secret="29fa40fccfa544d36e771025a195250222ab79679053f6127eac5da90272ab6f00f03cb1622d1b79b8606ce4df8ef5111ae54ff1115740b8d5df6c85066d21288d1ef5b892ff85ef89dc5cd09aee2fecbdacb661dcac3c312a8660a9f7b8012ffa85543ce15d973ab70dc1e61da514be0062e9875f642ba8c627709f0f47b20c3cab8b68cd850043275782e12030edf4098c52cbccef4f8cb6e4f6b1f0132e9de1fbdafdcad435f9b8d00e4607bcc41fa43d628de98c1a36b8520418a58a42e5edd5a778dfa86d82dcb2d627e3503fe95bdd261267a10f8ee9aba17edb783198f810b923c868aa030107d342bd85dc6061de6626147903f9e712b3650be6b0a8",
            login_url="/auth/login",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
