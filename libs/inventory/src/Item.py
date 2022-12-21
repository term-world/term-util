import os
import re
import sys
import gitit
import inspect
import argparse

from .Config import *
from .Template import Template

sys.path.append(
    os.path.expanduser(f'{Config.values["INV_PATH"]}')
)

class ItemSpec:

    file = None
    actions = { }
    consumable = True
    VOLUME = 1

    def __init__(self, filename: str = ""):
        self.file = filename
        arg_pairs = self.pairs(sys.argv)
        for arg, val in arg_pairs:
            if re.match(r"^-{1,2}", arg):
                arg = arg.replace("-","")
                self.actions[arg] = val
        self.vars()

    def pairs(self, args: list = []):
        return [args[i*2:(i*2)+2] for i in range(len(args)-2)]

    def vars(self) -> None:
        for arg in self.actions:
            setattr(self, arg, self.actions[arg])

    def use(self, **kwargs) -> None:
        print(f"You try the {self.__module__}, but it doesn't do anything.")
        if ItemSpec.consumable:
            os.remove(
                self.file
            )

class FixtureSpec(ItemSpec):

    consumable = False
    VOLUME = 3
    
    def __init__(self):
        super().__init__()

class BoxSpec(ItemSpec):

    consumable = True
    VOLUME = 2

    def __init__(self, filename: str = ""):
        super().__init__(filename)

    def use(self, **kwargs) -> None:
        if kwargs["action"] == "pack":
            return
        if kwargs["action"] == "unpack":
            items = kwargs["items"].split(",")
            for item in items:
                gitit.get(file_name=item.strip())
            os.remove(
                self.file
            )

class Factory:

    def __init__(self, name, path: str = ""):
        self.name = name.title().replace(" ","")
        self.path = path
        self.file = '\n\n'.join([
            "from inventory.Item import ItemSpec",
            inspect.getsource(Template)
        ])
        self.make()

    def make(self):
        self.file = self.file.replace(
            "Template",
            f"{self.name}(ItemSpec)"
        )
        filepath = os.path.join(self.path, f"{self.name}.py")
        with open(filepath, "w") as fh:
            fh.write(self.file)

class OutOfError(Exception):

    def __init__(self, item:str, *args):
        super().__init__(args)

class IsFixture(Exception):

    def __init__(self, item:str, *args):
        super().__init__(args)
