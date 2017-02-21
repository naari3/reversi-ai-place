import json
from functools import wraps

class ReversiStatus(object):
    """docstring for ReversiStatus"""

    def __init__(self):
        super(ReversiStatus, self).__init__()
        self.turns = 0 # 合計ターン数
        self.turn = 0 # 先攻/後攻 (1/2)
        self.started = False
        self.finished = False

    def after_start_method(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if self.started and not self.finished:
                f(self, *args, **kwargs)
            else:
                raise Exception("not in progress")
        return wrapper

    def after_finish_method(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if not self.started and self.finished:
                f(self, *args, **kwargs)
            else:
                raise Exception("in progress")
        return wrapper

    def start(self):
        self.turn = 1
        self.turns = 1
        self.started = True

    @after_start_method
    def progress_turn(self):
        if self.turn == 1:
            self.turn += 1
        elif self.turn == 2:
            self.turn = 1
            self.turns += 1
        else:
            pass

    def export_status(self):
        data = {
            'turns': self.turns,
            'turn': self.turn,
            'started': self.started,
            'finished': self.finished,
        }

        return data
