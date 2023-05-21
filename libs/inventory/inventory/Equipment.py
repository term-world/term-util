import os
import json
import narrator

from importlib import import_module

from .Config import Config
from .Inventory import *

class Equipment:

    EQUIPMENT_FILE = os.path.expanduser(
        f"{Config.values['INV_PATH']}/equipped.json"
    )

    EQUIPMENT_LOCS = {
        "head": None,
        "neck": None,
        "hand": {
            "left": None,
            "right": None
        },
        "torso": None,
        "leg": {
            "left": None,
            "right": None
        },
        "foot": {
            "left": None,
            "right": None
        }
    }

    def __init__(self):
        self.equipped = {}
        try:
            with open(self.EQUIPMENT_FILE, "r") as fh:
                self.equipped = json.load(fh)
        except FileNotFoundError:
            self.equipped = self.EQUIPMENT_LOCS
            with open(self.EQUIPMENT_FILE, "w") as fh:
                json.dump(self.equipped, fh)

    def __verify_slot(self, slot: str = "") -> bool:
        try:
            return self.equipped[slot] is not None
        except KeyError:
            raise InvalidSlotError
            exit()
        
    def __determine_sidedness(self) -> str:
        q = narrator.Question({
            "question": "Right or Left",
            "responses": [
                {"choice": "right", "outcome": "right"},
                {"choice": "left", "outcome": "left"}
            ]
        })
        return q.ask()

    def equip(self, item: str = "") -> None:
        name = item.split(".")[0]
        item_file = import_module(name)
        obj = getattr(item_file, item)()
        if self.__verify_slot(slot = obj.slot):
            try:
                if obj.slot in ["hand", "leg", "foot"]:
                    side = self.__determine_sidedness()
                    self.equipped[obj.slot][side] = name 
                else:
                    self.equipped[obj.slot] = name 
            except KeyError:
                raise InvalidSlotError
        with open(self.EQUIPMENT_FILE, "w") as fh:
            json.dump(self.equipped, fh)

    def unequip(self, slot) -> None:
        try:
            self.equipped[slot] = None
        except KeyError:
            raise InvalidSlotError

class EquipError(Exception):
    def __init__(self, item:str, *args):
        super().__init__(args)
        print("Can't equip {item}.")
        exit()

class InvalidSlotError(Exception):

    def __init__(self, *args):
        super().__init__(args)
        print("Not an equippable slot.")
        exit()