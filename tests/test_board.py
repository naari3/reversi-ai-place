# -*- config: utf-8 -*-
import sys
from models import ReversiBoard

import pytest

sys.path.append('..')


class TestBoard(object):

    def test_valid_moves(self):
        board = ReversiBoard()
        result = board.put_piece(26, 2)
        assert result == 1
        result = board.put_piece(18, 1)
        assert result == 1
        assert all(board.board == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 0, 0, 0, 0, 0,
            0, 0, 2, 1, 2, 0, 0, 0,
            0, 0, 0, 2, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ])

    def test_invalid_moves(self):
        board = ReversiBoard()
        with pytest.raises(Exception):
            board.put_piece(1, 1)

        with pytest.raises(Exception):
            board.put_piece(1, 2)

        assert all(board.board == [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 2, 0, 0, 0,
            0, 0, 0, 2, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ])

    def test_export(self):
        board = ReversiBoard()
        data = board.export_board()
        init_data = [
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 2, 0, 0, 0),
            (0, 0, 0, 2, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
        ]
        assert data == init_data
