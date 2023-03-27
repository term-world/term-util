import os
import importlib

from datetime import datetime
from inventory import Validator
from .packager import Package
from .item import Item

from couchsurf import Connection
from couchsurf import request

class Listing:

    def __init__(self, files: any = ""):
        # TODO: Is valid discovers validity, but doesn't
        #       tell us anything about the name?
        if self.is_valid(files):
            print("[MARKETPLACE] Passed validation...")
            self.author = os.getlogin()
            self.date = datetime.now().timestamp()
            # TODO: Suggest defaults based on file names and precalculated
            #       values for name and author, for example.
            self.name = input(f"[MARKETPLACE] Name of package to list: ")
            self.lib_name = self.name.lower()
            self.author = input(f"[MARKETPLACE] Author name({self.author}): ") or self.author

    def serialize(self) -> dict:
        obj = importlib.import_module(self.name)
        # Serializes the catalog record
        return {
            "lib_name": self.name.lower(), # We need to "sanitize this...later
            "nice_name": self.name,
            "owners": [self.author],
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

    # TODO: Process catalog status which reveals one of two outcomes
    #       1. Catalog record exists, only send version and update catalog versions
    #       2. No catalog exists, send catalog record, send version, and update catalog versions
    #       (The second and third seem like reusable functions.)

    # TODO: Give my bad functions default values

    def make_library(self,conn,ver_uuid):
            conn.request.put(
                doc_id=conn.request.get_new_id(),
                doc={
                    "lib_name": self.lib_name,
                    "nice_name": self.name,
                    "type": "library",
                    "owners": [self.author],
                    "description": getattr(self.name,"use").__doc__,
                    "versions": {"v1": ver_uuid}
                }
            )
            print(f"[MARKETPLACE][{self.name}]Library added to Marketplace")

    def make_version(self,conn,matches,version,ver_uuid):
            conn.request.put(
                doc_id=ver_uuid,
                doc={
                    "package": matches["docs"],
                    "type": "version",
                    "author":self.author,
                    "date":self.date,
                    "version":f"v{version}",
                },
                attachment= f"{self.name}.pyz"
            )
            print(f"[MARKETPLACE][{self.name}][{version}]Document Uploaded to Marketplace")

    def is_version(self) -> str:
        conn = Connection("marketplace")
        conn.request.get("items")

    def pack(self):
        pack = Package(name = self.name, files = f"{self.name}.py")
        pack.make()

    def build(self) -> dict:
        conn = Connection("marketplace")
        matches = conn.request.query(
            lib_name={"op":"EQUALS", "arg": self.lib_name},
            owners={"op":"GREATER THAN", "arg": self.author}
        )
        ver_uuid = conn.request.get_new_id()

        if not matches:
            version = 1
            self.make_library(conn,ver_uuid)
            # TODO: create new function to clean up the nice name and create a library name that is only lowercase letters
        else:
            for x in range(len(matches["docs"])):
                if self.lib_name == matches["docs"][x]["lib_name"]:
                    version = len(matches["docs"][x]["versions"]) + 1
            
        self.make_version(conn,matches,version,ver_uuid)
        
    def list(self) -> None:
        pass
