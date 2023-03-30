import os
import re
import importlib

from datetime import datetime
from inventory import Validator
from collections import namedtuple

from couchsurf import Connection

from .packager import Package
from .record import Record, Library, Version

class Listing:

    conn = Connection("marketplace")

    def __init__(self, files: any = ""):
        if self.is_valid(files = files):
            self.library = self.make_library()
            self.version_id = self.conn.request.get_new_id()

    def is_valid(self, files: any = "") -> bool:
        if os.path.isfile(files):
            files = [files]
        elif os.path.isdir(files):
            for parent, dirs, files in os.walk(files):
                files = files
        for file in files:
            if Validator.validate(file):
                self.name, self.ext = file.split(".")
                if self.ext:
                    self.ext = f".{self.ext}"
                return True
        return False

    # TODO: Process catalog status which reveals one of two outcomes
    #       1. Catalog record exists, only send version and update catalog versions
    #       2. No catalog exists, send catalog record, send version, and update catalog versions
    #       (The second and third seem like reusable functions.)

    def make_library(self,version,ver_uuid,ver_dict,owners):
        self.conn.request.put(
            doc_id=self.conn.request.get_new_id(),
            doc={
                "lib_name": self.lib_name,
                "nice_name": self.name,
                "type": "library",
                "owners": owners,
                "description": getattr(self.file_class,"use").__doc__,
                "versions": ver_dict.update({f"v{version}": ver_uuid})
            })
    def make_db_entry(self, data: any, **kwargs) -> None:
        if "attachment" in kwargs:
            self.pack()
            self.conn.request.put(
                doc_id = data._id,
                doc = data.__dict__,
                attachment = f"{self.name}{self.ext}"
            )
        else:
            self.conn.request.put(
                doc_id = data._id,
                doc = data.__dict__
            )

    def make_library(self) -> Library:
        library = Library(
            name = self.name
        )
        return library

    def make_version(self) -> Version:
        version = Version(
            library = self.library
        )
        version._id = self.version_id
        return version

    def pack(self):
        pack = Package(
            files = f"{self.name}{self.ext}",
            name = self.library.lib_name
        )
        pack.make()

    def build(self) -> dict:
        """ Builds the item in the DB; probably needs better name? """
        # Find any matches in the database
        matches = self.conn.request.query(
            lib_name = {"op":"EQUALS", "arg": self.library.lib_name},
            owners = {"op":"GREATER THAN", "arg": self.library.owners}
        )
        # If there are matches, set self.library to the data
        if matches["docs"]:
            # TODO: Still need a high-confidence way to tell if this is 
            #       the library we're looking for?
            self.library = Library(**matches["docs"][0])
            self.versions = len(self.library.versions)
        else:
            # If no matches, we can assume this is a new library
            self.library._id = self.conn.request.get_new_id()
        # Make a new version
        self.version = self.make_version()
        # Update library with new version?
        self.library.add_version(
            v_no = self.version.version,
            v_id = self.version._id
        )
        # Put entries in database
        self.make_db_entry(self.library)
        self.make_db_entry(self.version, attachment = self.name)
