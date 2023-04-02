import json
import math

from time import sleep
from .types import Inexhaustible

def Singleton(cls):
    def getinstances():
        return cls()._Inexhaustible__generation()
    return getinstances

@Singleton
class Wind(Inexhaustible):

    def __init__(self):
        self.blade_num = 0
        self.blade_size = 0
        super().__init__()

    def __calc_velocity(self):
        m_per_second = (2 * math.pi * self.blade_size) / 20

@Singleton
class Solar(Inexhaustible):

    def __init__(self, wattage: int = 0):
        super().__init__()
