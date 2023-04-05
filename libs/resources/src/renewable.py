import json
import math

from time import sleep
from .types import Inexhaustible

from rich.console import Console

CONSOLE = Console()

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
        with CONSOLE.status("Generating wind power...", spinner = "earth"):
            sleep(1 + self.blade_size / 100)

class Solar(Inexhaustible):

    wattage = 0

    def __init__(self):
        super().__init__()
        if self.wattage not in [250, 300, 350, 400]:
            print("Panel not in approved sizes.")
            exit()
        self.__calc_wattage()

    def __calc_wattage(self):
        if not self.CLIMATE.sunny:
            self.wattage = 0
        self.power = (self.wattage * .016) / 1000
        self.generation(type = "Solar")
        with CONSOLE.status("Generating solar power...", spinner = "moon"):
            sleep(1)
