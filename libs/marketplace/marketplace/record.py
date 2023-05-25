import re
import getpass

from datetime import datetime

class Record:

    def generate(self, data: dict = {}):
        """ Constructor for generic-propertied files """
        for field in data:
            setattr(self, field, data[field])

class Library(Record):

    def __init__(self, **kwargs):
        kwargs["type"] = "library"
        try:
            kwargs["owners"] = [owner for owner in kwargs["owners"]]
        except KeyError:
            kwargs["owners"] = [getpass.getuser()]
        kwargs["nice_name"] = kwargs["name"]
        kwargs["lib_name"] = re.sub(
            r'[^a-zA-Z0-9]', '', kwargs["name"]
        ).lower()
        kwargs["date"] = datetime.now().timestamp()
        try:
            kwargs["versions"] = kwargs["versions"]
        except KeyError:
            kwargs["versions"] = {}
        kwargs["description"] = ""
        self.generate(kwargs)

    def add_version(self, v_no: str = "", v_id: str = ""):
        self.versions.update({v_no: v_id})

class Version(Record):

    def __init__(self, library: Library, **kwargs):
        kwargs["library"] = library._id
        kwargs["type"] = "version"
        try:
            kwargs["author"]
        except KeyError:
            kwargs["author"] = getpass.getuser()
        kwargs["date"] = datetime.now().timestamp()
        kwargs["version"] = f"v{len(library.versions) + 1}"
        self.generate(kwargs)
