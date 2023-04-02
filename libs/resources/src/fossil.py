import json

from .types import Exhaustible

def Singleton(cls):
    def getinstances():
        return cls()._Exhaustible__payload
    return getinstances

@Singleton
class Oil(Exhaustible):

    def __init__(self):
        self.draw = 5
        self.unit = "barrels"
        super().__init__(__file__)

@Singleton
class Coal(Exhaustible):

    def __init__(self):
        self.draw = 7
        self.unit = "cubic feet"
        super().__init__(__file__)
