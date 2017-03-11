# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import json

from .base_api import BaseAPIHandler
from models import BoardGameMaster, User
from handlers import BoardWebSocketHandler


class BoardAPIHandler(BaseAPIHandler):

    @BaseAPIHandler.need_access_token
    def get(self, board_id):
        board = self.application.boards.get(board_id, BoardGameMaster(board_id))
        response = board.extract_data()

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response))
