import os
import importlib
import pyminifier
#import couchsurf

from inventory import Acquire

class Listing:

    def __init__(filename: str = ""):
        Acquire.validate(filename)
        self.filename = filename
        self.codeball = self.minify()

    def minify(self):
        with open(self.filename, "r") as fh:
            code = fh.read()
