import os
import json

class Exhaustible:

    def __init__(self):
        self.level = 0
        self.capacity = 0

    def load_file(self, filename: str = ""):
        self.create_file(filename)
        with open(filename, "r") as fh:
            data = json.load(fh)
        self.level = data["level"]
        self.capacity = data["capacity"]

    def create_file(self, filename: str = "") -> bool:
        data = {
            "level": 5000,
            "capacity": 5000
        }
        if not os.path.isfile(filename):
            with open(filename, "w") as fh:
                json.dump(data, fh)
                return True
        return False

    def update_file(self, filename: str = "", usage: int = 0):
        self.level -= usage
        with open(filename, "w") as fh:
            json.dump(
                self.__dict__,
                fh
            )

class Inexhaustible:

    pass
