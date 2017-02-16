# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import random

class BoardHandler(tornado.web.RequestHandler):

    def get(self, borad_id):
        response = {
            'meta': {
                'status': 200
            },
            'data': {
                'id': borad_id,
                'random': random.randint(0,100)
            },
        }

        self.write(response)
        self.set_header("Content-Type", "application/json")

class BoardWebSocketHandler(tornado.websocket.WebSocketHandler):

    users = set()

    def open(self):
        self.users.add(self)
        print('Session opened by {}'.format(self.request.remote_ip))

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
