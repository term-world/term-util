import os
import importlib

from datetime import datetime
from inventory import Validator
from .packager import Package

from couchsurf import Connection

class Listing:

    def __init__(self, files: any = ""):
        if self.is_valid(files):
            print("[MARKETPLACE] Passed validation...")
            self.author = os.getlogin()
            self.date = datetime.now().timestamp()
            # TODO: Suggest defaults based on file names and precalculated
            #       values for name and author, for example.
            self.name = input("[MARKETPLACE] Name of package to list: ")

    def serialize(self) -> dict:
        obj = importlib.import_module(self.name)
        # Serializes the catalog record
        return {
            "package": self.name,
            "author": self.author
            "description": getattr(obj, self.name)().use.__doc__
        }

    def is_valid(self, files: any = "") -> bool:
        if os.path.isfile(files):
            files = [files]
        elif os.path.isdir(files):
            for parent, dirs, files in os.walk(files):
                files = files
        for file in files:
            # Only 1 file has to validate for the package
            # to be potentially valid
            if Validator.validate(file):
                return True
        return False

    def is_version(self) -> str:
        conn = Connection("marketplace")
        conn.request.get("items")

    def pack(self):
        pack = Package(name = self.name, files = f"{self.name}.py")
        pack.make()

    def build(self) -> dict:
        print(self.serialize())

    def list(self) -> None:
        pass
