import os
import json

from inventory import ItemSpec

class Exhaustible(ItemSpec):

    def __init__(self, filename: str = ""):
        super().__init__(filename)
        self.__get_resource(filename = filename)
        self.__get_stockpile()
        self.__exhaust_one()

    def __get_resource(self, filename: str = "") -> None:
        name, ext = filename.split("/")[-1].split(".")
        self.name = name

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

    def __exhaust_one(self) -> None:
        self.level -= 1
        with open(self.path, "w") as fh:
            json.dump(
                {"level": self.level},
                fh
            )

class Inexhaustible:

    pass
