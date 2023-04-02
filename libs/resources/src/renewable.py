import json
import math

from time import sleep
from .types import Inexhaustible

class Wind(Inexhaustible):

    blade_size = 0

    def __init__(self):
        super().__init__()
        if self.blade_size > 115:
            print("Blade size too long!")
            exit()
        self.__calc_velocity()

    def __calc_velocity(self):
        sweep_area = math.pi * self.blade_size ** 2
        self.power = (.5 * 1.23 * self.CLIMATE.wind_speed ** 3 * sweep_area) / 1000
        self.generation(type = "Wind")
        sleep(1)

class Solar(Inexhaustible):

    def __init__(self):
        super().__init__()
        self.__calc_wattage()
    
    def __calc_wattage(self):
        self.power = (self.wattage * .016) / 1000
        self.generation(type = "Solar")
        sleep(1)