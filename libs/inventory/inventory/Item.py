import os
import re
import sys
import gitit
import string
import inspect

from glob import glob
from importlib import util

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
        #if self.consumable:
        #    os.remove(
        #        self.file
        #    )

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

    def __init__(self, name, path: str = "", fixture: bool = False, template: str = "", **kwargs):
        """ Creates items from templates """
        self.path = path
        self.name = self.clean(name)
        self.template = self.load_template(template)
        self.item_type = FixtureSpec if fixture else ItemSpec

        # Load source locally, and handle based on template contents
        source = inspect.getsource(self.template)
        item_import = ""
        if not "from inventory.Item import" in source:
            item_import = f"from inventory.Item import {self.item_type.__name__}"
        # Based on the above, assemble the source

        self.file = '\n\n'.join([
            item_import,
            source
        ])
        self.props = kwargs
        self.make()

    def load_template(self, template: str = ""):
        if not template:
            return Template
        filepath = os.path.dirname(template)
        template = os.path.basename(template)
        if not filepath:
            filepath = os.path.expanduser(
                Config.values["INV_PATH"]
            )
        spec = util.spec_from_file_location(
            template,
            f"{filepath}/{template}"
        )
        mod = util.module_from_spec(spec)
        return mod

    def clean(self, filename: str = "") -> str:
      punc = ''.join(
        [ch for ch in string.punctuation if not ch == "_"] + [" "]
      )
      return ''.join(
        [ch for ch in filename if ch not in punc]
      )

    @staticmethod
    def rename(filename: str = "", count: int = 0) -> str:
        files = glob("*.py")
        names = [name.split(".py")[0] for name in files]
        temp_name = filename
        while temp_name in names:
            if count > 0:
                temp_name = f"{filename}{count}"
            count += 1
        return temp_name

    def make(self):
        final_name = self.rename(self.name)
        self.file = re.sub(
            f"{self.template.__package__}\([a-zA-Z0-9_]+\)",
            f"{final_name}({self.item_type.__name__})",
            self.file,
            1
        )
        if self.item_type == FixtureSpec:
            self.file = self.file.replace(
                "__file__",
                ""
            )
        filepath = os.path.join(
            self.path,
            f"{final_name}.py"
        )
        with open(filepath, "w") as fh:
            fh.write(self.file)

class OutOfError(Exception):

    def __init__(self, item:str, *args):
        super().__init__(args)

class IsFixture(Exception):

    def __init__(self, item:str, *args):
        super().__init__(args)
