import numpy as np

class ReversiBoard(object):
    """docstring for ReversiBoard"""
    def __init__(self, resume_data=None):
        super(ReversiBoard, self).__init__()
        if resume_data:
            self.board = self.resume_board(resume_data)
        else:
            self.board = self.create_board()

    def create_board(self):
        a = np.zeros(64, dtype=int)
        a[27] = a[36] = 1
        a[28] = a[35] = 2
        return a

    def resume_board(self, resume_data):
        return create_board()

    def put_piece(self, p, w, puton=True, chk=True, other_board=None):
        if isinstance(p, list):
            p = (p[0])+p[1]*8
            if p > 63:
                p = (p[0]-1)+(p[1]-1)*8
        t, x, y = 0, p%8, p//8
        for di, fi in zip([-1, 0, 1], [x, 7, 7-x]):
            for dj, fj in zip([-8, 0, 8], [y, 7, 7-y]):
                if not di == dj == 0:
                    if other_board:
                        b = other_board[p+di+dj::di+dj][:min(fi, fj)]
                    else:
                        b = self.board[p+di+dj::di+dj][:min(fi, fj)]
                    n = (b==3-w).cumprod().sum()
                    if b.size <= n or b[n] != w: n = 0
                    t += n
                    if puton:
                        b[:n] = w
        if puton:
            if other_board:
                if chk: assert(other_board[p] == 0 and t > 0)
                other_board[p] = w
            else:
                if chk: assert(self.board[p] == 0 and t > 0)
                self.board[p] = w
        return t

    def export_board(self):
        data = list(zip(*[iter(self.board.tolist())]*8))
        return data

    def print_board(self):
        print('  a b c d e f g h')
        for i in range(8):
            print(i+1, end=' ')
            print(' '.join('.*o'[j] for j in self.board[i*8:][:8]))
