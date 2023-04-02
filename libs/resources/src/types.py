import os
import json

import requests
from inventory import ItemSpec

from .climate import Climate

CLIMATE = Climate()

class Exhaustible(ItemSpec):

    def __init__(self, filename: str = ""):
        super().__init__(filename)
        self.__get_resource(filename = filename)
        self.__get_stockpile()
        self.__payload = [self] * self.__extract()

    def __get_resource(self, filename: str = "") -> None:
        self.name = self.__class__.__name__.lower()

    def __get_stockpile(self) -> None:
        self.path = f"/world/{self.name}"
        self.__supply_stockpile()
        with open(self.path, "r") as fh:
            data = json.load(fh)
        self.level = data["level"]

    def __supply_stockpile(self) -> None:
        if not os.path.isfile(self.path):
            with open(self.path, "w") as fh:
                json.dump(
                    {"level": 5000},
                    fh
                )

    def __exhaust(self) -> None:
        self.level -= self.draw
        with open(self.path, "w") as fh:
            json.dump(
                {"level": self.level},
                fh
            )

    def __verify_level(self) -> bool:
        if self.level - self.draw <= 0:
            return False
        return True

    def __extract(self) -> int:
        if self.__verify_level():
            self.__exhaust()
            return self.draw
        return 0

class Inexhaustible:

    def __init__(self):
        print(CLIMATE)
