import numpy as np

class ReversiBoard(object):
    """docstring for ReversiBoard"""
    def __init__(self, resume_data=None):
        super(ReversiBoard, self).__init__()
        if resume_data:
            self.board = self.resume_board()
        else:
            self.board = self.create_board()

    def create_board(self):
        a = np.zeros(64, dtype=int)
        a[27] = a[36] = 1
        a[28] = a[35] = 2
        return a

    def resume_board(self, resume_data):
        return create_board()

    def print_board(self):
        print('  a b c d e f g h')
        for i in range(8):
            print(i+1, end=' ')
            print(' '.join('.*o'[j] for j in self.board[i*8:][:8]))
