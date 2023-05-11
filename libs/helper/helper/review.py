import os

class Review:

    def __init__(self, filename: str = ""):
        self.code = self.__read_file(filename)

    def __read_file(self, filename: str = "") -> str:
        try:
            with open(filename, "r") as fh:
                return fh.read()
        except:
            print("ERROR: Not a valid file.")
