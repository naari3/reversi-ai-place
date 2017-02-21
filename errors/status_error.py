# -*- coding: utf-8 -*-
class BoardStatusError(BaseException):

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return(f'Board is {self.status}.')
