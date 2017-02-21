# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import random

from .board_ws import BoardWebSocketHandler


class BoardHandler(tornado.web.RequestHandler):

    def get(self, borad_id):
        print(BoardWebSocketHandler.boards)
        response = {
            'meta': {
                'status': 200
            },
            'data': {
                'id': borad_id,
                'random': random.randint(0, 100)
            },
        }

        self.write(response)
        self.set_header("Content-Type", "application/json")
