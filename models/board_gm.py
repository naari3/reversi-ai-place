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
            duplicated = False

            for p in self.players:
                if not duplicated:
                    duplicated = player['user'] == p['user']

            if not duplicated:
                self.players.append(player)
                if len(self.players) == 2:
                    self.game_start()
                data_message = json.dumps(
                    self.extract_data(), sort_keys=True, ensure_ascii=False)
                self.send_all(data_message)
                return True
            else:
                print('this user is already entered this board')
        else:
            print(f'{self.board_id} is already full')
        return False

    def remove_player(self, player_ws):
        _p = None
        for p in self.players:
            if player_ws == p['ws']:
                _p = p
        if _p in self.players:
            self.players.remove(_p)

    def send_all(self, message):
        for p in self.players:
            p['ws'].write_message(message)

    def extract_data(self, status=True):
        user_data = {
            'first': {
                'id': self.players[0]['user'].id,
            } if len(self.players) >= 1 else None,
            'second': {
                'id': self.players[1]['user'].id,
            } if len(self.players) >= 2 else None,
        }

        meta_data = {
            'status': 200 if status else 400
        }
        game_data = {
            'users': user_data,
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
        print("passing", count)
        if count == 2:
            self.finish()
        else:
            putable = self.board.able_to_put(self.status.turn)
            print(self.status.turn, "putable", putable)
            if len(putable) == 0:  # どこにも置けなかったら
                print(self.status.turn, "has passed!")
                self.status.progress_turn()
                self.pass_check(count + 1)
        print()

    def finish(self):
        self.status.finish()
        print("finished")

    def receive_move(self, user, x, y):
        ind = None
        for i, p in enumerate(self.players):
            if p['user'] == user:
                ind = i + 1
        place = x + y * 8
        reverse_num = 0

        try:
            reverse_num = self.board.put_piece(place, ind)
            self.status.progress_turn()
            if self.pass_check():
                pass
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
        if self.status.finished:
            self.close_board()
        return bool(reverse_num)

    def close_board(self):
        for p in self.players:
            p['ws'].close(code=1000, reason="board no.[{board_id}] is closed")
