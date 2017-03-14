# -*- coding: utf-8 -*-
import sys

import websocket
import json

import numpy as np
from math import exp
import random

import requests

from models import ReversiBoard


args = sys.argv


class SampleReversiBot(object):

    def __init__(self, board_id, access_token, user_id):
        self.board_id = board_id
        self.access_token = access_token
        self.user_id = user_id
        self.turn = None
        self.v_board = ReversiBoard()
        ws = websocket.WebSocketApp(
            f"ws://localhost:8000/v1/board/{self.board_id}/ws",
            header=[f"Authorization: Bearer {self.access_token}"],
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()

    def print_board(self, board):
        print("  0 1 2 3 4 5 6 7")
        for i, bo in enumerate(board):
            print(str(i) + " " + " ".join([".*o"[b] for b in bo]))

    def get_board(self, board):
        for i, bo in enumerate(board):
            self.v_board.board[i*8:(i+1)*8] = bo

    def move(self, ws, board):
        print(".*o"[self.turn])

        places = self.v_board.able_to_put(self.turn)

        place = random.choice(places)

        y, x = divmod(place, 8)

        message = json.dumps({'x': x, 'y': y})
        ws.send(message)

    def handler(self, ws, data):
        print(data)
        self.print_board(data['data']['board'])
        self.get_board(data['data']['board'])
        if data.get('data'):
            if data['data']['users']['first']['id'] == self.user_id:
                self.turn = 1
            elif data['data']['users']['second']['id'] == self.user_id:
                self.turn = 2
            if data['data']['started'] and not data['data']['finished']:
                print("my turn", self.turn, ": now turn", data['data']['turn'])
                if self.turn == data['data']['turn']:
                    self.move(ws, data['data']['board'])

    def on_message(self, ws, message):
        data = json.loads(message)
        self.handler(ws, data)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        if self.v_board:
            score1 = (self.v_board.board == 1).sum()
            score2 = (self.v_board.board == 2).sum()
            print(f"{score1} - {score2}")
            if score1 > score2:
                print(f'You {"win" if self.turn == 1 else "lose"}')
            elif score1 < score2:
                print(f'You {"lose" if self.turn == 1 else "win"}')
            elif score1 == score2:
                print("draw")

        print('disconnected streaming server')

    def on_open(self, ws):
        print('connected streaming server')


board_id = args[1]
access_token = args[2]
user_id = args[3]
bot = SampleReversiBot(int(board_id), access_token, int(user_id))
