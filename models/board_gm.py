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
        self.status.started = True

    def send_all(self, arg):
        pass

    def receive_move(self, player, x, y):
        pass
