# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import json

from .board_ws import BoardWebSocketHandler
from models import BoardGameMaster, User
from .base import BaseHandler


class BoardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, board_id):
        board = self.application.boards.get(board_id, BoardGameMaster(board_id))
        response = board.extract_data()

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response))
