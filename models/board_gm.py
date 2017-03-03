# -*- coding: utf-8 -*-
import json
from models import ReversiStatus, ReversiBoard


class BoardGameMaster(object):
    """docstring for BoardGameMaster"""

    def __init__(self, board_id):
        super(BoardGameMaster, self).__init__()
        self.board_id = board_id
        self.players = []
        self.status = ReversiStatus()
        self.board = ReversiBoard()

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)
            if len(self.players) == 2:
                self.game_start()
            return True
        else:
            print(f'{self.board_id} is already full')
            return False

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def send_all(self, message):
        for p in self.players:
            p.write_message(message)

    def extract_data(self, status=True):
        meta_data = {
            'status': 200 if status else 400
        }
        game_data = {
            'board': self.board.export_board(),
            **self.status.export_status(),
        }

        if self.status.finished:
            score1 = (self.board.board == 1).sum()
            score2 = (self.board.board == 2).sum()
            game_data['result'] = {
                'win': 'player1' if score1 > score2 else 'player2',
                'lose': 'player1' if score1 < score2 else 'player2',
                'draw': True if score1 == score2 else False,
            }

        data = {
            "meta": meta_data,
            "data": game_data,
        }

        return data

    def game_start(self):
        self.status.start()

    def pass_check(self, count=0):
        if count == 2:
            self.finish()
        putable = self.board.able_to_put(self.status.turn)
        if len(putable) == 0 and count < 2:  # どこにも置けなかったら
            self.status.progress_turn()
            self.pass_check(count + 1)

    def finish(self):
        self.status.finish()

    def receive_move(self, player, x, y):
        ind = self.players.index(player) + 1
        place = x + y * 8
        reverse_num = 0

        try:
            reverse_num = self.board.put_piece(place, ind)
            self.status.progress_turn()
            self.pass_check()
        except Exception as e:
            if isinstance(e, AssertionError):
                print("invalid move")
            else:
                raise e

        send_data = self.extract_data(bool(reverse_num))
        send_data['data']['move'] = {
            'x': x,
            'y': y,
            'correct': bool(reverse_num),
        }

        data_message = json.dumps(
            send_data, sort_keys=True, ensure_ascii=False)
        self.send_all(data_message)
        return bool(reverse_num)
