import json
import math

from time import sleep
from .types import Inexhaustible

from rich.console import Console
from rich.spinner import SPINNERS

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

class Water(Inexhaustible):

    # TODO: Make a couple of pipe opportunities available?
    flow_rate = 0
    pipe_radius = 0
    pipe_length = 100

    wave = {
        "interval": 200,
        "frames": ["🌊  "," 🌊 ", "  🌊"]
    }

    SPINNERS.update({"water": wave})

    def __init__(self):
        super().__init__()
        self.__calc_flow()

    def __has_water(self) -> bool:
        with open("/world/reservoir", "r") as water_level:
            data = json.load(water_level)
        if data["level"] < self.flow_rate:
            print("""
                You may ask yourself "well, how did I get here?"
                And you may ask yourself "how do I work this?"
                And you may ask yourself "where did all the water go?"
                And You may ask yourself "My God! What have I done?"
            """)
            return False
        self.data = data
        return True

    def __calc_flow(self):
        if not self.__has_water():
            exit()
        # Assumes 1 foot "drop" over run of the pipe
        coeff = 1.318 * 120
        velocity = coeff * (1 / self.pipe_radius) ** 0.63
        velocity *= (1 / self.pipe_length ** 0.54)
        # Convert velocity to flow rate
        self.flow_rate = (math.pi * self.pipe_radius ** 2) * velocity
        # Multiply by common efficiency averages
        self.power = (self.pipe_length * self.flow_rate * (.18 * .50)) / 1000
        with CONSOLE.status("Water flowing underground...", spinner = "water"):
            sleep(1)
        # Remove from reservoir?
        self.data["level"] -= self.flow_rate
        with open("/world/reservoir", "w") as water_level:
            json.dump(self.data, water_level)
