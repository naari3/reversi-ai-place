# -*- coding: utf-8 -*-
class NoPutablePlaceError(BaseException):

    def __init__(self):
        pass

    def __str__(self):
        return("You can'n put piece anywhere")
