import os
import re
import sys
import json
import argparse
import importlib
import shutil
import sqlite3

from rich.table import Table
from rich.console import Console
from collections import namedtuple

# TODO: Add configuration to environment variable stack?
from .Config import *

from .Item import ItemSpec
from .Item import FixtureSpec
from .Item import BoxSpec
from .Item import OutOfError
from .Item import IsFixture
from .Item import Factory

from .Validation import Validator

PATH = f'{Config.values["INV_PATH"]}/{Config.values["INV_REGISTRY"]}'

sys.path.append(
  [
    os.path.expanduser(os.getcwd()),
    os.path.expanduser(f'{Config.values["INV_PATH"]}')
  ]
)

MAX_VOLUME = 10

class Acquire:

    def __init__(self, filename, quantity: int = 1):
        self.filename = filename
        self.item = filename
        if quantity == "":
            quantity = 1
        self.quantity = int(quantity)
        if not Validator.validate(filename):
            exit()
        self.locate(filename)
        self.move()
        self.add()

    def is_box(self, item) -> bool:
        self.box = "BoxSpec" in dir(item)

    def locate(self, filename: str = "") -> None:
        self.name, self.ext = self.filename.split("/")[-1].split(".")
        self.name = re.search(r"[a-zA-Z]+", self.name).group(0)
        self.box = Validator.is_box(self.name)
        self.filename = f"{self.name}.{self.ext}"

    def move(self):
        try:
            path = os.path.expanduser(
                f'{Config.values["INV_PATH"]}/{self.filename}'
            )
            if not self.box:
                try:
                    shutil.copy(self.filename, path)
                except:
                    # This operation attempts to move the file
                    # based on real file name; however, if this
                    # fails it might be OK
                    pass
                obj = importlib.import_module(self.name)
                if "ItemSpec" in dir(obj):
                    # Remove only the physically present copy
                    os.remove(f"./{self.item}")
        except Exception as e:
            print(f"Couldn't acquire {self.name}")
            exit()

    def add(self):
        item = self.filename.replace(".py", "")
        item_volume = list.is_consumable(item).VOLUME * self.quantity
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
        self.path = os.path.expanduser(
            f'{Config.values["INV_PATH"]}'
        )
        self.conn = sqlite3.connect(
            os.path.expanduser(PATH)
        )
        self.__create_sql_table()
        if os.path.exists(f"{self.path}/.registry"):
            self.__convert_json_file()
            os.unlink(f"{self.path}/.registry")

    # Representation
    def __str__(self) -> str:
        return json.dumps(self.inventory)

    # Create inventory SQL table (DEPRECATE AS SOON AS IS PRACTICAL)
    def __create_sql_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS items (
                    name TEXT,
                    filename TEXT,
                    quantity REAL,
                    weight REAL,
                    consumable INTEGER,
                    volume REAL GENERATED ALWAYS AS (weight * quantity) STORED
                );
            """
        )

    # Convert legacy JSON file
    def __convert_json_file(self):
        with open(os.path.expanduser(
                f'{Config.values["INV_PATH"]}/.registry'
            ), "r") as fh:
            data = json.load(fh)
        cursor = self.conn.cursor()
        for item in data:
            self.__add_table_entry(
                name = item,
                filename = data[item]["filename"],
                quantity = data[item]["quantity"],
                weight = data[item]["volume"],
                consumable = 1 if 'consumable' in data[item] else 0
            )

    def __add_table_entry(
        self,
        name: str = "",
        filename: str = "",
        quantity: float = 1.0,
        weight: float = 0.0,
        consumable: int = 1
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                INSERT INTO items(name, filename, quantity, weight, consumable)
                VALUES(?, ?, ?, ?, ?);
            """,
            (name, filename, quantity, weight, consumable)
        )
        self.conn.commit()


    # Delete table entries by name, one by one
    def __delete_table_entry(self, name: str = "", filename: str = ""):
        self.remove(item = name)
        cursor = self.conn.cursor()
        cursor.execute(
            """
                DELETE FROM items WHERE name = ?
            """,
            (entry,)
        )

    # Add/remove items

    def total_volume(self) -> int:
        total_volume = 0
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT volume FROM items;
            """
        )
        for (volume,) in cursor.fetchall():
            total_volume += volume
        return total_volume

    def add(self, item: str, number: int = 1) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
                UPDATE items
                SET quantity = quantity + {number}
                WHERE name = ?;
            """,
            (item,)
        )
        if cursor.rowcount != 1:
            self.__add_table_entry(
                name = item,
                filename = f"{item}.py",
                quantity = number
            )

    def remove(self, item: str, number: int = -1) -> None:
        self.add(item = item, number = number)

    # Automatically remove empty or negative quantity items

    def empties(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT name, filename FROM items WHERE quantity <= 0.0
            """
        )
        for name, filename in cursor.fetchall():
            self.__delete_table_entry(name, filename)

    # Completely removes all items in .inv not listed in the .registry file

    def cleanup_items(self) -> None:
        tempdict = {}
        path = os.path.expanduser("~/.inv/")
        for item in os.listdir(path):
            if ".py" in item:
                tempdict.update({item: "null"})
            for element in self.inventory:
                if f"{element}.py" in item:
                    tempdict.pop(item)
        for item in tempdict:
            os.remove(os.path.expanduser(f"~/.inv/{item}"))

    # Create a nice(r) display

    def display(self):
        table = Table(title=f"{os.getenv('LOGNAME')}'s inventory")
        # Remove all entries without corresponding files
        # self.cleanup_items()
        table.add_column("Item name")
        table.add_column("Item count")
        table.add_column("Item file")
        table.add_column("Consumable")
        table.add_column("Volume")

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, filename, quantity, consumable, volume FROM items
        """)

        for name, filename, quantity, consumable, volume in cursor.fetchall():
            table.add_row(
                str(name),
                str(quantity),
                str(filename),
                str(consumable),
                str(volume)
            )

        console = Console()
        print("")
        console.print(table)
        print(f"Your current total volume limit is: {self.total_volume()}/{MAX_VOLUME}\n")

    # Returns a boolean whether the item object is a consumable

    def is_consumable(self, item: str) -> list:

        try:
            item_file = importlib.import_module(f"{item}")
        except ModuleNotFoundError:
            exit()
        try:
            instance = getattr(item_file, item)()
        except:
            print(f"{item} doesn't seem to be a valid object.")
            exit()
        return instance

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

    def trash(self, item: str, quantity: int = 1) -> None:
        """ Removes item from the list; tied to the "remove" .bashrc alias """
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1
        try:
            list.add(item, 0 - int(quantity))
        except:
            pass

    def drop(self, item: str = "", quantity: int = 1) -> None:
        """ Drops item copy in current directory; removes from inventory """
        try:
            if not item in self.list:
                raise OutOfError(item)
            # Convert the quantity to an integer if not already one
            quantity = int(quantity)
            # Test if the number being dropped is more than we have
            # and limit the drops to only the quantity that we actually
            # can drop
            if quantity > self.list[item]["quantity"]:
                quantity = self.list[item]["quantity"]
        except OutOfError:
            print(f"It doesn't look like you have any {item}.")
            exit()
        except ValueError:
            quantity = 1
        try:
            for _ in range(quantity):
                Factory(item)
            list.add(item, 0 - int(quantity))
        except:
            pass

    def use(self, item: str):

        # Set up properties and potential kwargs
        box = False
        fixture = False

        # Verify that item is in path or inventory
        try:
            item_file = importlib.import_module(f"{item}")
        except ModuleNotFoundError:
            print(f"You don't seem to have any {item}.")
            exit()

        # Reflect the class
        try:
            instance = getattr(item_file, item)()
        except:
            print(f"{item} doesn't seem to be a valid object.")
            exit()

        # Test type of item; remove if ItemSpec
        try:
            box = self.is_box(item_file)
            fixture = self.is_fixture(item_file)
            number = self.list[item]["quantity"]
#             if fixture or box:
#                 raise IsFixture(item)

            # Only decrease quantity if item is consumable
            if instance.consumable:
                list.remove(item)
            if number <= 0:
                raise OutOfError(item)
        except (KeyError, OutOfError) as e:
            print(f"You have no {item} remaining!")
            exit()
        except IsFixture: pass

        # Return the result or inbuilt use method
        if type(instance).__str__ is not object.__str__:
            instance.use(**instance.actions)
        else:
            return instance.use(**instance.actions)

# Create instances to use as shorthand
# I thought this was a bad idea, but this
# is actually how the random module works

# https://github.com/python/cpython/blob/main/Lib/random.py

list = List()
items = Items(list)
