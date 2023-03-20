import os
import importlib

from datetime import datetime
from inventory import Validator
from .packager import Package

from couchsurf import Connection
from couchsurf import request

class Listing:

    """ Require:
        * author
        * date
        * version
        * description
    """

    def __init__(self, files: any = ""):
        if self.is_valid(files):
            print("[MARKETPLACE] Passed validation...")
            self.author = os.getlogin()
            self.date = datetime.now().timestamp()
            self.name = str(input("[MARKETPLACE] Enter Name of Package: "))

    def serialize(self) -> dict:
        obj = importlib.import_module(self.name)
        return {
            "Author": self.author,
            "Date": self.date,
            "Version": "v0.1.0",
            "Description": getattr(obj, self.name)().use.__doc__
        }

    def is_valid(self, files: any = "") -> bool:
        if os.path.isfile(files):
            files = [files]
        elif os.path.isdir(files):
            for parent, dirs, files in os.walk(files):
                files = files
        for file in files:
            # TODO: Convert Acquire.validate to bool?
            #       This fixes the issue that only _one_ of the
            #       files has to actually work -- and it tells us
            #       which file to add the code to.
            if Validator.validate(file):
                return True
        # TODO: Remains valid for now (for testing)
        return False

    def is_version(self) -> str:
        conn = Connection("marketplace")
        conn.request.get("listings")

    def pack(self):
        pack = Package(name = self.name, files = f"{self.name}.py")
        pack.make()

    def build(self) -> dict:
        conn = Connection("marketplace")

        for x in conn.request.view("items")["rows"]:
            if self.name.lower() == x["key"].lower():
                location = len(x["value"]["versions"])
                v_number = f"v{location+1}"
                # creates the new objects id to the exisiting library using the existing librarys id
                break

        if not location:
            pass
            #if the library does not exist, create a new library with new library id

        """Creates the new object json and adds to CouchDB."""
        uuid = conn.request.get("_uuids")["uuids"][location] #asks for an id that doesnt exist?
        result = conn.request.put(doc_id=uuid, doc={"date":self.date,"version":v_number}, attachment= f"{self.name}.pyz")
        print(f"[MARKETPLACE][{result}]Document Uploaded to Marketplace")

            

            
    def list(self) -> None:
        pass
