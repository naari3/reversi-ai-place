# -*- config: utf-8 -*-
import sys
from models import ReversiStatus

import pytest

sys.path.append('..')


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

    def test_start(self):
        status = ReversiStatus()
        status.start()
        data = status.export_status()

        started_data = {
            'turns': 1,
            'turn': 1,
            'started': True,
            'finished': False,
        }
        assert data == started_data

    def test_finish_valid(self):
        status = ReversiStatus()
        status.start()
        status.finish()
        data = status.export_status()

        started_data = {
            'turns': 1,
            'turn': 1,
            'started': True,
            'finished': True,
        }
        assert data == started_data

    def test_finish_invalid(self):
        status = ReversiStatus()
        with pytest.raises(Exception):
            status.finish()

    def test_after_start_method(self):
        status = ReversiStatus()
        status.start()
        status.progress_turn()

    def test_after_start_method_exception(self):
        status = ReversiStatus()
        with pytest.raises(Exception):
            status.progress_turn()

    def test_progress_turn(self):
        status = ReversiStatus()
        status.start()
        status.progress_turn()
        assert status.turn == 2
        assert status.turns == 1

        status.progress_turn()
        assert status.turn == 1
        assert status.turns == 2
