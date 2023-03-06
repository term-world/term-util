import os

from datetime import datetime
from inventory import Acquire
from packager import Package

from couchsurf import Connection

import os

class Listing:

    """ Require:
        * author
        * date
        * version
        * description
    """

    def __init__(self, files: any = ""):
        if is_valid(files):
            self.author = os.getlogin()
            self.date = datetime.now().timestamp()
            self.name = input("[MARKETPLACE] Name of package to list: ")

    def serialize(self) -> dict:
        return {
            "Author": self.author,
            "Date": self.date,
            "Version": "v0.1.0",
            "Description": "Get this from a docstring?"
        }

    def is_valid(self, files: any = "") -> bool:
        if os.path.isfile(files):
            files = [files]
        elif os.path.isdir(files):
            for parent, dirs, files in os.walk(files)
                files = files
        for file in files:
            # TODO: Convert Acquire.validate to bool?
            #       This fixes the issue that only _one_ of the
            #       files has to actually work -- and it tells us
            #       which file to add the code to.
            pass
        # TODO: Remains valid for now (for testing)
        return True

    def is_version(self) -> str:
        conn = Connection("marketplace")
        conn.request.get("listings")

    def pack(self):
        pass
        #package = Package(
        #    name = self.name,
        #    files = f"{self.name}.{self.ext}"

    def build(self) -> dict:
        print(self.serialize())

    def list(self) -> None:
        pass
