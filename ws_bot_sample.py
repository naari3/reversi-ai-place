# -*- coding: utf-8 -*-
import sys

import websocket


class SampleReversiBot(object):

    def __init__(self, board_id, access_token):
        self.board_id = board_id
        self.access_token = access_token
        ws = websocket.WebSocketApp(
            f"ws://c163e4ee.ngrok.io/v1/board/{self.board_id}/ws",
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

    def on_message(self, ws, message):
        print(message)

    # エラーが起こった時
    def on_error(self, ws, error):
        print(error)

    # websocketを閉じた時
    def on_close(self, ws):
        print('disconnected streaming server')

    # websocketを開いた時
    def on_open(self, ws):
        print('connected streaming server')


access_token = ''
bot = SampleReversiBot(11, access_token)
