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
            self.author = input(f"[MARKETPLACE] Author name({self.author}): ") or self.author
            self.pkg_name = self.name.lower()

    def serialize(self) -> dict:
        obj = importlib.import_module(self.name)
        # Serializes the catalog record
        return {
            "pkg_name": self.name.lower(), # We need to "sanitize this...later
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

    def is_version(self) -> str:
        conn = Connection("marketplace")
        conn.request.get("items")

    def pack(self):
        pack = Package(name = self.name, files = f"{self.name}.py")
        pack.make()

    def build(self) -> dict:
        # Connects to DB
        conn = Connection("marketplace")
        # Queries only for pkg_name and author match
        matches = conn.request.query(
            pkg_name={"op":"EQUALS", "arg": self.pkg_name},
            owners={"op":"GREATER THAN", "arg": self.author}
        )

#        for x in conn.request.view("items")["rows"]:
#            if self.name.lower() == x["key"].lower():
#                location = len(x["value"]["versions"])
#                v_number = f"v{location+1}"
                # creates the new objects id to add to the exisiting library for this object
#                break
        version = 1
        if matches:
            print(matches)
            #version = len(matches["values"]["versions"]) + 1
  
        #if the library does not exist, create a new library with new library id
            
        """else:
            #Creates the new object json and adds to existing CouchDB library
            uuid = conn.request.get_new_id()
            result = conn.request.put(
                doc_id=uuid,
                doc={
                    "author":self.author,
                    "date":self.date,
                    "version":version,
                    "package": #TODO: GIVE ME MY PACKAGE
                },
                attachment= f"{self.name}.pyz"
            )
            print(f"[MARKETPLACE][{result}]Document Uploaded to Marketplace")
        """
    def list(self) -> None:
        pass
