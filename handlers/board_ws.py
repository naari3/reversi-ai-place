# -*- coding: utf-8 -*-
import tornado.websocket

from models import BoardGameMaster, User

import json


class BoardWebSocketHandler(tornado.websocket.WebSocketHandler):

    boards = {}

    board_id_dict = {}

    def open(self, board_id):
        print(f"opened and connected to {board_id} by {self.request.remote_ip}")
        self.application.boards[board_id] = self.application.boards.get(
            board_id, BoardGameMaster(board_id))
        print(self.application.boards)
        self.application.board_id_dict[self] = board_id  # 逆引き: ダサい
        # 追加できたらTrue返ってくる
        player = {
            'ws': self,
            'user': self.get_current_user(),
        }
        if not self.application.boards[board_id].add_player(player):
            self.close(code=1003, reason="You can't join to [{board_id}]")

    def on_close(self):
        board_id = self.application.board_id_dict[self]
        print(f"closed and disconnected to {board_id} by {self.request.remote_ip}")
        self.application.boards[board_id].remove_player(self)

    def on_message(self, message):
        board_id = self.application.board_id_dict[self]
        input_data = json.loads(message)
        if input_data.get('x', False) and input_data.get('y', False):
            self.application.boards[board_id].receive_move(
                self, input_data['x'], input_data['y'])
        else:
            self.write_message(json.dumps(
                {meta: {'status': 400, 'message': 'illegal move'}}))
