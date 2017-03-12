# -*- coding: utf-8 -*-
import tornado.websocket

from .base_api import BaseAPIWebSocketHandler
from models import BoardGameMaster, User
from handlers import BoardWebSocketHandler

import json


class BoardWebSocketAPIHandler(BaseAPIWebSocketHandler):

    @BaseAPIWebSocketHandler.need_access_token
    def open(self, board_id):
        print(f"opened and connected to {board_id} by {self.request.remote_ip}")
        self.application.boards[board_id] = self.application.boards.get(
            board_id, BoardGameMaster(board_id))
        print(self.application.boards)
        self.application.board_id_dict[self] = board_id  # 逆引き: ダサい
        # 追加できたらTrue返ってくる
        player = {
            'ws': self,
            'user': self.get_token_user(),
        }
        print(player['user'].id)
        if not self.application.boards[board_id].add_player(player):
            self.close(code=1003, reason="You can't join to [{board_id}]")

    def on_close(self):
        board_id = self.application.board_id_dict[self]
        print(f"closed and disconnected to {board_id} by {self.request.remote_ip}")
        if self.application.boards.get(board_id, None):
            self.application.boards[board_id].close_board()
            del self.application.boards[board_id]

    def on_message(self, message):
        board_id = self.application.board_id_dict[self]
        input_data = json.loads(message)
        try:
            if input_data.get('x', False) and input_data.get('y', False):
                self.application.boards[board_id].receive_move(
                    self.get_token_user(), input_data['x'], input_data['y'])
            else:
                data = self.application.boards[board_id].extract_data()
                data['meta'] = {
                    'status': 400,
                    'message': 'illegal move'
                }
                self.write_message(json.dumps(data))
        except Exception as e:
            data = self.application.boards[board_id].extract_data()
            data['meta'] = {
                'status': 400,
                'message': 'illegal move'
            }
            self.write_message(json.dumps(data))
