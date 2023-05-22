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

    def __review_slots(self) -> dict:
        for slot in self.equipped:
            try:
                yield {
                    slot: list(self.equipped[slot].values())
                }
            except (TypeError, AttributeError):
                yield {slot: [self.equipped[slot]]}
    
    def __update_equipped(self) -> None:
        with open(self.EQUIPMENT_FILE, "w") as fh:
            json.dump(self.equipped, fh)

    def equip(self, item: str = "") -> None:
        name = item.split(".")[0]
        item_file = import_module(name)
        obj = getattr(item_file, item)()
        if "RelicSpec" not in dir(obj):
            raise EquipError(item)
        if self.__verify_slot(slot = obj.slot):
            try:
                if obj.slot in ["hand", "leg", "foot"]:
                    side = self.__determine_sidedness()
                    self.equipped[obj.slot][side] = name 
                else:
                    self.equipped[obj.slot] = name 
            except KeyError:
                raise InvalidSlotError
            self.__update_equipped()

    def unequip(self, item: str = "") -> None:
        for slot in self.__review_slots():
            loc = next(iter(slot.keys()))
            if item in slot[loc]:
                if type(self.equipped[loc]) == dict:
                    sub_slot = list(
                        self.equipped[loc].keys()
                    )[list(
                        self.equipped[loc].values()
                    ).index(item)]
                    self.equipped[loc][sub_slot] = None
                else:
                    self.equipped[loc] = None
        self.__update_equipped()

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