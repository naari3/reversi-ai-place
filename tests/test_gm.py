# -*- config: utf-8 -*-

import sys
from models import BoardGameMaster, ReversiStatus, ReversiBoard
from errors import NoPutablePlaceError

import pytest

import json

sys.path.append('..')


class _player(object):

    def __init__(self):
        message = None

    def write_message(self, message):
        self.message = message


class TestGameMaster(object):

    def test_instance(self):
        gm = BoardGameMaster(1)
        assert gm.board_id == 1
        assert isinstance(gm.status, ReversiStatus)
        assert isinstance(gm.board, ReversiBoard)

    def test_add_player(self):
        gm = BoardGameMaster(1)
        player1 = _player()
        player2 = _player()
        player3 = _player()

        assert gm.add_player(player1) is True
        assert gm.add_player(player2) is True
        assert gm.add_player(player3) is False

        assert player1 in gm.players
        assert player2 in gm.players
        assert player3 not in gm.players

    def test_remove_player(self):
        gm = BoardGameMaster(1)
        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        gm.remove_player(player1)
        assert player1 not in gm.players

        gm.remove_player(player2)
        assert player2 not in gm.players

    def test_game_start(self):
        gm = BoardGameMaster(1)
        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)
        assert gm.status.started is True

    def test_send_all(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        message = 'ya'
        gm.send_all(message)

        for p in gm.players:
            assert p.message == message

    def test_extract_data(self):
        gm = BoardGameMaster(1)

        correct_data = {
            "meta": {
                "status": 200,
            },
            "data": {
                "board": [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 2, 0, 0, 0],
                    [0, 0, 0, 2, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ],
                "finished": False,
                "started": False,
                "turn": 0,
                "turns": 0,
            }
        }

        assert correct_data == gm.extract_data()

    def test_receive_move_valid(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        assert gm.receive_move(player1, 4, 2) is True

        correct_data = {
            "meta": {
                "status": 200,
            },
            "data": {
                "board": [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 2, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ],
                "move": {
                    "x": 4,
                    "y": 2,
                    "correct": True,
                },
                "finished": False,
                "started": True,
                "turn": 2,
                "turns": 1
            }
        }
        for p in gm.players:
            assert json.loads(p.message) == correct_data

    def test_receive_move_invalid(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        assert gm.receive_move(player1, 0, 0) is False

        correct_data = {
            "meta": {
                "status": 400,
            },
            "data": {
                "board": [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 2, 0, 0, 0],
                    [0, 0, 0, 2, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ],
                "move": {
                    "x": 0,
                    "y": 0,
                    "correct": False,
                },
                "finished": False,
                "started": True,
                "turn": 1,
                "turns": 1
            }
        }
        for p in gm.players:
            assert json.loads(p.message) == correct_data

    def test_receive_move_pass(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        gm.status.turn = 1

        gm.board.board[0:8] = [0, 0, 0, 0, 0, 0, 0, 0]
        gm.board.board[8:16] = [0, 0, 0, 0, 0, 0, 0, 0]
        gm.board.board[16:24] = [0, 0, 0, 0, 0, 0, 0, 0]
        gm.board.board[24:32] = [0, 0, 2, 2, 2, 0, 0, 0]
        gm.board.board[32:40] = [0, 0, 0, 2, 2, 2, 2, 2]
        gm.board.board[40:48] = [0, 0, 0, 0, 0, 1, 0, 1]
        gm.board.board[48:56] = [0, 0, 0, 2, 2, 2, 2, 1]
        gm.board.board[56:64] = [0, 0, 0, 0, 0, 0, 0, 1]

        gm.receive_move(player1, 5, 7)
        assert gm.status.turn == 1

        gm.receive_move(player1, 3, 7)
        assert gm.status.turn == 1

        gm.receive_move(player1, 2, 6)
        assert gm.status.turn == 1

        gm.receive_move(player1, 7, 3)
        assert gm.status.turn == 1

    def test_finish1(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        gm.board.board[0:8] = [1, 1, 1, 1, 1, 1, 1, 1]
        gm.board.board[8:16] = [1, 1, 1, 1, 1, 1, 1, 1]
        gm.board.board[16:24] = [1, 1, 1, 1, 1, 1, 1, 1]
        gm.board.board[24:32] = [1, 1, 1, 1, 1, 1, 1, 1]
        gm.board.board[32:40] = [1, 1, 1, 1, 1, 1, 1, 1]
        gm.board.board[40:48] = [1, 1, 1, 1, 1, 1, 1, 1]
        gm.board.board[48:56] = [1, 1, 1, 1, 1, 1, 1, 2]
        gm.board.board[56:64] = [1, 1, 1, 1, 1, 1, 1, 0]

        print(gm.status.export_status())
        gm.receive_move(player1, 7, 7)

        correct_data = {
            "meta": {
                "status": 200,
            },
            "data": {
                "board": [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ],
                "move": {
                    "x": 7,
                    "y": 7,
                    "correct": True,
                },
                "finished": True,
                "result": {
                    "draw": False,
                    "lose": "player2",
                    "win": "player1"
                },
                "started": True,
                "turn": 2,
                "turns": 2
            }
        }
        for p in gm.players:
            assert json.loads(p.message) == correct_data

    def test_finish2(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        gm.board.board[0:8] = [1, 1, 1, 1, 1, 1, 1, 0]
        gm.board.board[8:16] = [1, 1, 1, 1, 1, 1, 1, 0]
        gm.board.board[16:24] = [1, 1, 1, 1, 1, 1, 1, 0]
        gm.board.board[24:32] = [1, 1, 1, 1, 1, 1, 1, 0]
        gm.board.board[32:40] = [1, 1, 1, 1, 1, 1, 1, 0]
        gm.board.board[40:48] = [1, 1, 1, 1, 1, 1, 1, 0]
        gm.board.board[48:56] = [1, 1, 1, 1, 1, 1, 1, 2]
        gm.board.board[56:64] = [1, 1, 1, 1, 1, 1, 1, 1]

        print(gm.status.export_status())
        gm.receive_move(player1, 7, 5)

        correct_data = {
            "meta": {
                "status": 200,
            },
            "data": {
                "board": [
                    [1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ],
                "move": {
                    "x": 7,
                    "y": 5,
                    "correct": True,
                },
                "finished": True,
                "result": {
                    "draw": False,
                    "lose": "player2",
                    "win": "player1"
                },
                "started": True,
                "turn": 2,
                "turns": 2
            }
        }
        for p in gm.players:
            assert json.loads(p.message) == correct_data
