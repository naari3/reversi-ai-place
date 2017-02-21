# -*- config: utf-8 -*-
import sys
sys.path.append('..')
from models import BoardGameMaster, ReversiStatus, ReversiBoard

import pytest

class _player(object):

    def __init__(self):
        write_message = None

    def write_message(self, message):
        self.write_message = message



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

        assert gm.add_player(player1) == True
        assert gm.add_player(player2) == True
        assert gm.add_player(player3) == False

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
        assert gm.status.started == True

    def test_send_all(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        message = 'ya'
        gm.send_all(message)

        for p in gm.players:
            assert p.write_message == message

    def test_receive_move_valid(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        assert gm.receive_move(player1, 4, 2) == True

        assert gm.board.export_board() == [
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 1, 1, 0, 0, 0),
            (0, 0, 0, 2, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
        ]

        data_string = '{"board": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], "finished": false, "started": true, "turn": 2, "turns": 1}'
        for p in gm.players:
            assert p.write_message == data_string

    def test_receive_move_invalid(self):
        gm = BoardGameMaster(1)

        player1 = _player()
        player2 = _player()
        gm.add_player(player1)
        gm.add_player(player2)

        assert gm.receive_move(player1, 0, 0) == False

        assert gm.board.export_board() == [
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 2, 0, 0, 0),
            (0, 0, 0, 2, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
        ]

        data_string = '{"board": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], "finished": false, "started": true, "turn": 1, "turns": 1}'
        for p in gm.players:
            assert p.write_message == data_string
