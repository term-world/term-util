import os
import re
import sys
import gitit
import inspect

from .Config import *
from .Template import Template

sys.path.append(
    os.path.expanduser(f'{Config.values["INV_PATH"]}')
)

class ItemSpec:

    def __init__(self, filename: str = ""):
        self.file = filename
        self.actions = {}
        arg_pairs = self.pairs(sys.argv)
        for arg, val in arg_pairs:
            if re.match(r"^-{1,2}", arg):
                arg = arg.replace("-","")
                self.actions[arg] = val
        self.consumable = True
        self.VOLUME = 1
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

    def __init__(self):
        super().__init__()
        self.consumable = False
        self.VOLUME = 3

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

    def __init__(self, name, path: str = "", fixture: bool = False, **kwargs):
        self.name = name.title().replace(" ","")
        self.path = path
        self.item_type = FixtureSpec if fixture else ItemSpec
        self.file = '\n\n'.join([
            f"from inventory.Item import {self.item_type.__name__}",
            inspect.getsource(Template)
        ])
        self.props = kwargs
        self.make()

    def make(self):
        self.file = self.file.replace(
            "Template",
            f"{self.name}({self.item_type.__name__})"
        )
        if self.item_type == FixtureSpec:
            self.file = self.file.replace(
                "__file__",
                ""
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
