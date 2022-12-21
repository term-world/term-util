import os
import sys
import json
import argparse

from rich.table import Table
from rich.console import Console
from collections import namedtuple

from .Config import *

from .Item import ItemSpec
from .Item import FixtureSpec
from .Item import BoxSpec
from .Item import OutOfError
from .Item import IsFixture

PATH = f'{Config.values["INV_PATH"]}/{Config.values["INV_REGISTRY"]}'

sys.path.append(
  [
    os.path.expanduser(os.getcwd()),
    os.path.expanduser(f'{Config.values["INV_PATH"]}')
  ]
)

MAX_VOLUME = 10

class Acquire:

    import shutil
    import importlib

    def __init__(self, filename, quantity: int = 1):
        self.filename = filename
        if quantity == "":
            quantity = 1
        self.quantity = int(quantity)
        self.validate()
        self.move()
        self.add()

    def is_box(self, item) -> bool:
        self.box = "BoxSpec" in dir(item)

    def validate(self):
        import importlib
        try:
            self.name, self.ext = self.filename.split(".")
            if not self.ext == "py":
                raise
            obj = importlib.import_module(self.name)
            getattr(obj, self.name)().use
            self.is_box(obj)
        except Exception as e:
            print("Not a valid item file")
            exit()

    def move(self):
        import shutil
        try:
            path = os.path.expanduser(
                f'{Config.values["INV_PATH"]}/{self.filename}'
            )
            if not self.box:
                shutil.copy(self.filename, path)
        except Exception as e:
            print(f"Couldn't acquire {self.name}")
            exit()
            
    def add(self):
        item = self.filename.replace(".py", "")
        
        item_volume = list.determine_consumable(item).VOLUME * self.quantity
        
#         item_volume = getattr(self.filename, item)()
        
        current_volume = list.total_volume() + item_volume
        if MAX_VOLUME >= current_volume:
            try:
                list.add(self.name, self.quantity)
            except Exception as e:
                print(f"Couldn't acquire {self.name}")
                exit()
        else:
            print(f"Couldn't acquire {self.quantity} {self.name}: Max Volume exceeded")
            exit()

class List:

    # File operations
    
    def __init__(self):
        self.inventory = {}
        self.path = os.path.expanduser(f'{Config.values["INV_PATH"]}')
        try:
            fh = open(
                os.path.expanduser(PATH),
                "r+"
              )
            self.inventory = json.load(fh)
            fh.close()
        except: pass

    def write(self) -> None:
        self.empties()
        with open(
            os.path.expanduser(PATH),
            "w"
        ) as fh:
            json.dump(self.inventory, fh)

    # Representation

    def __str__(self) -> str:
        return json.dumps(self.inventory)

    # Add/remove items
    
    def total_volume(self):
        
        total_volume = 0
        for item in self.inventory:
            if os.path.exists(f"{self.path}/{item}.py"): 
                total_volume += int(self.inventory[item]["volume"]) * int(self.inventory[item]["quantity"])
        return total_volume
        

    def add(self, item: str, number: int = 1) -> None:
        
        if item in self.inventory:
            self.inventory[item]["quantity"] += number
            # self.inventory[item]["volume"] += volume
        else:
            self.inventory[item] = {
                "quantity": number,
                "filename": f"{item}.py",
                "volume": f"{self.determine_consumable(item).VOLUME}"
            }
        self.write()

    def remove(self, item: str, number: int = -1) -> None:
        self.add(item, number)

    # Automatically remove empty or negative quantity items

    def empties(self) -> None:
        deletes = []
        for item in self.inventory:
            if self.inventory[item]["quantity"] <= 0:
                deletes.append(item)
            if not os.path.exists(f"{self.path}/{item}.py"): # added this to delete any items in the json file that does not have the associated .py file in .inv
                deletes.append(item)
        for item in deletes:
            del self.inventory[item]

    # Completely removes all items in .inv not listed in the .registry file       
            
    def nukeItems(self) -> None:
        tempdict = {}
        path = os.path.expanduser("~/.inv/")
        for item in os.listdir(path):
            if ".py" in item:
                tempdict.update({item: "null"})
            for element in self.inventory:
                if f"{element}.py" in item:
                    tempdict.pop(item)
        for item in tempdict:
            os.remove(os.path.expanduser(f"~/.inv/{item}")) # chose to use ~/.inv/ as the filepath to delete extraneous items
    # Create a nice(r) display

    def display(self):
        table = Table(title=f"{os.getenv('LOGNAME')}'s inventory")
        self.write() # This will make sure it loads in the proper file before adding columns. Also removes extra table items that don't exist in .inv from the .registry file.
        self.nukeItems() # This removes any .py files from .inv that is not listed in the .registry file
        table.add_column("Item name")
        table.add_column("Item count")
        table.add_column("Item file")
        table.add_column("Consumable")
        table.add_column("Volume")
        
        for item in self.inventory:
            table.add_row(
                item,
                str(self.inventory[item]["quantity"]),
                self.inventory[item]["filename"],
                str(self.determine_consumable(item).consumable),
                str(self.determine_consumable(item).VOLUME * self.inventory[item]["quantity"])
            )

        console = Console()
        print("")
        console.print(table)
        print(f"Your current total volume limit is: {self.total_volume()}/{MAX_VOLUME}\n")
    # Returns a boolean whether the item object is a consumable
    
    def determine_consumable(self, item: str) -> list:
    
        from importlib import import_module   
        try:
            item_file = import_module(f"{item}")
        except ModuleNotFoundError:
          #print(f"You don't seem to have any {item}.")
            return
        try:
            instance = getattr(item_file, item)()
        except:
            print(f"{item} doesn't seem to be a valid object.")
            return 
        return instance

# Create instances to use as shorthand
# I thought this was a bad idea, but this
# is actually how the random module works

# https://github.com/python/cpython/blob/main/Lib/random.py

class Items:

    def __init__(self, list):
        self.inv = list
        self.list = list.inventory

    def is_fixture(self, item) -> bool:
        return "FixtureSpec" in dir(item)

    def is_box(self, item) -> bool:
        return "BoxSpec" in dir(item)

    def file_exists(self, item) -> bool:
        return os.path.exists(f"{self.inv.path}/{item}.py")
    
    def registry_exists(self, item) -> bool:
        for element in self.list:
            if element == item:
                return True
        return False
            

    # Removes item from the list and is tied to the "remove" alias in .bashrc
    
    def trash(self, item: str, rem_quantity: int = 1):
        if rem_quantity == "":
            rem_quantity = 1
        try:
            list.add(item, 0 - int(rem_quantity))
            list.empties()
        except:
            pass
    
    def use(self, item: str):
        # Import necessary reflection module
        from importlib import import_module

        # Set up properties and potential kwargs
        box = False
        fixture = False

        # Verify that item is in path or inventory
        try:
            item_file = import_module(f"{item}")
        except ModuleNotFoundError:
            print(f"You don't seem to have any {item}.")

        # Reflect the class
        try:
            instance = getattr(item_file, item)()
        except:
            print(f"{item} doesn't seem to be a valid object.")
            return
        
        # Test type of item; remove if ItemSpec
        try:
            box = self.is_box(item_file)
            fixture = self.is_fixture(item_file)
            number = self.list[item]["quantity"]
#             if fixture or box:
#                 raise IsFixture(item)
            
            # only decreases quantity if it is a consumable
            if instance.consumable:
                list.add(item, -1)
            if number <= 0:
                raise OutOfError(item)
        except (KeyError, OutOfError) as e:
            print(f"You have no {item} remaining!")
            return
        except IsFixture as e: pass

        # To or not to remove; that is the question

        # edited so now the item can be used multiple times while still functioning
        if instance.consumable and number <= 0:
            try:
                list.remove(item)
            except: pass

      # File now removes at the Spec level
      # os.remove(
      #  item_file.__file__
      # )

        # Return the result or inbuilt use method
        if type(instance).__str__ is not object.__str__:
            instance.use(**instance.actions)
            # print(f"{instance}")
        else:
            return instance.use(**instance.actions)

# Create instances to use as shorthand
# I thought this was a bad idea, but this
# is actually how the random module works

# https://github.com/python/cpython/blob/main/Lib/random.py

list = List()
items = Items(list)