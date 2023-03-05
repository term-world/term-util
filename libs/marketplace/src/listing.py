import os
import couchsurf

from inventory import Acquire
from .packager import *

class Listing:

    """ Require:
        * author
        * date
        * version
        * description
    """

    def __init__(filename: str = ""):
        Acquire.validate(filename)
        self.filename = filename

    def is_complete(self, fields: dict = {}) -> bool:
        return False

    def build(self) -> dict:
        pass

    def list(self) -> None:
        pass
