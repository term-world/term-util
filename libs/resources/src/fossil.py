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
        self.unit = "barrel"
        self.energy = 1667
        super().__init__(__file__)

    def __str__(self) -> str:
        return f"What else do you want? It's a {self.unit} of {self.name.lower()}."

@Singleton
class Coal(Exhaustible):

    def __init__(self):
        self.draw = 7
        self.unit = "short ton"
        self.energy = 5549
        super().__init__(__file__)

    def __str__(self) -> str:
        return f"I love the smell of a good {self.unit} of burning {self.name.lower()}."
