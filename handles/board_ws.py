# -*- coding: utf-8 -*-
import tornado.websocket

class BoardWebSocketHandler(tornado.websocket.WebSocketHandler):

    boards = {}

    def open(self, borad_id):
        print(borad_id)
        self.boards.get(borad_id, self)
        # print('Session {} opened by {}'.format(board_id, self.request.remote_ip))

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print('Session closed by {}'.format(self.request.remote_ip))
