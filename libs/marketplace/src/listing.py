import os
import importlib
import re

from datetime import datetime
from inventory import Validator

from .packager import Package
from .item import Item
from .library import Record

from couchsurf import Connection
from couchsurf import request

class Listing:

    def __init__(self, files: any = ""):
        self.name = input(f"[MARKETPLACE] Name of package to list: ")
        if self.is_valid(f"{self.name}.py"):
            print("[MARKETPLACE] Passed validation...")
            self.conn = Connection("marketplace")
            self.author = os.getlogin()
            self.date = datetime.now().timestamp()
            self.lib_name = re.sub(r'[^a-zA-Z0-9]', '', self.name).lower()
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

    def make_library(self,version,ver_uuid,ver_dict,owners):
        self.conn.request.put(
            doc_id=self.conn.request.get_new_id(),
            doc={
                "lib_name": self.lib_name,
                "nice_name": self.name,
                "type": "library",
                "owners": owners,
                "description": getattr(self.name,"use").__doc__,
                "versions": ver_dict.update({f"v{version}": ver_uuid})
            }
        )
        print(f"[MARKETPLACE][{self.name}]Library added to Marketplace!")

    def make_version(self,version,ver_uuid,package):
        self.conn.request.put(
            doc_id=ver_uuid,
            doc={
                "library": package,
                "type": "version",
                "author":self.author,
                "date":self.date,
                "version":f"v{version}",
            },
            attachment= f"{self.name}.pyz"
        )
        print(f"[MARKETPLACE][{self.name}][{version}]Document Uploaded to Marketplace!")

    def is_version(self) -> str:
        self.conn.request.get("items")

    def pack(self):
        pack = Package(name = self.name, files = f"{self.name}.py")
        pack.make()

    def build(self) -> dict:
        matches = self.conn.request.query(
            lib_name={"op":"EQUALS", "arg": self.lib_name},
            owners={"op":"GREATER THAN", "arg": self.author}
        )
        version_uuid = self.conn.request.get_new_id()

        if not matches:
            version_type = 1
            stored_versions_dict = {}
            owners = [self.author]
        else:
            for x in range(len(matches["docs"])):
                record = Record(matches["docs"][x])
                if self.lib_name == record.lib_name:
                    version_type = len(record.versions) + 1
                    package = record._id
                    stored_versions_dict = record.versions
                    owners = record.owners
                    if self.author not in owners:
                        owners.append(self.author)
        
        self.make_library(
            version_type,
            version_uuid,
            stored_versions_dict,
            owners
        )
        self.pack()
        self.make_version(
            version_type,
            version_uuid,
            package
        )
        os.remove(f"{self.name}.pyz")
        

    def list(self) -> None:
        pass
