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

    def game_start(self):
        self.status.start()

    def send_all(self, message):
        for p in self.players:
            p.write_message(message)

    def receive_move(self, player, x, y):
        ind = self.players.index(player) + 1
        place = x + y * 8
        reverse_num = 0

        try:
            reverse_num = self.board.put_piece(place, ind)
            self.status.progress_turn()
        except Exception as e:
            if isinstance(e, AssertionError):
                print("invalid move")
            else:
                raise e

        game_data = {
            'board': self.board.export_board(),
            **self.status.export_status()
        }
        data_message = json.dumps(
            game_data, sort_keys=True, ensure_ascii=False)
        self.send_all(data_message)
        return bool(reverse_num)
