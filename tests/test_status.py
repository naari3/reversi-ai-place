# -*- config: utf-8 -*-
import sys
sys.path.append('..')
from models import ReversiStatus

import pytest


class TestStatus(object):

    def test_export(self):
        status = ReversiStatus()
        data = status.export_status()
        init_data = {
            'turns': 0,
            'turn': 0,
            'started': False,
            'finished': False,
        }
        assert data == init_data

    def test_after_start_method(self):
        status = ReversiStatus()
        status.started = True
        status.progress_turn()

    def test_after_start_method_exception(self):
        status = ReversiStatus()
        with pytest.raises(Exception):
            status.progress_turn()

    def test_progress_turn(self):
        status = ReversiStatus()
        status.started = True
        status.progress_turn()
        assert status.turn == 1
        assert status.turns == 0

        status.progress_turn()
        assert status.turn == 0
        assert status.turns == 1
