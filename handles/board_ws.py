# -*- coding: utf-8 -*-
import tornado.websocket

class BoardWebSocketHandler(tornado.websocket.WebSocketHandler):

    boards = {}

    def open(self, borad_id):
        self.boards.get(borad_id, self)
        print('Session {} opened by {}'.format(board_id, self.request.remote_ip))

    def on_message(self, message):
        message = json.loads(message)
        t = Tokenizer()
        tokens = t.tokenize(message["text"])
        message["text"] = ""
        for token in tokens:
            message["text"] += "{} ".format(token.surface)
        for user in self.users:
            user.write_message(message)

    def on_close(self):
        self.users.remove(self)
        print('Session closed by {}'.format(self.request.remote_ip))
