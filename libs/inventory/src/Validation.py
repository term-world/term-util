import re
import importlib

from .Item import BoxSpec

class Validator:

    @staticmethod
    def validate(filename: str = "") -> bool:
        try:
            name, ext = filename.split("/")[-1].split(".")
            if not ext == "py":
                raise
            obj = importlib.import_module(name)
            getattr(obj, name)().use
        except Exception as e:
            print("Not a valid item file.")
            return False
        return True

    @staticmethod
    def is_box(name: any = "") -> bool:
        obj = importlib.import_module(name)
        return "BoxSpec" in dir(obj)
