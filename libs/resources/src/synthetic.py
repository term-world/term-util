import json

from .types import Exhaustible

def Singleton(cls):
    def getinstances():
        return cls()._Exhaustible__payload
    return getinstances

@Singleton
class Nuclear(Exhaustible):

    def __init__(self):
        self.draw = 7
        self.unit = "cubic_feet"
        self.value = 3772
        super().__init__(__file__)

    def __str__(self) -> str:
        return f"""Congratulations. You made {self.draw} {self.unit} of {self.name.lower()} waste.
At least it has a kind-of attractive green glow."""
