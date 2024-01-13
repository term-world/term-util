import os
import re
import sys
import dill
import json
import importlib
import shutil
import sqlite3
import pennant

from rich.table import Table
from rich.console import Console

# TODO: Add configuration to environment variable stack?
from .Config import *
from .Equipment import *

from .Item import *

from .Validation import Validator
from .Instantiator import Instance

PATH = f'{Config.values["INV_PATH"]}/{Config.values["INV_REGISTRY"]}'
WORLD = os.getenv("WORLD_NAME")

sys.path.append(
  [
    os.path.expanduser(os.getcwd()),
    os.path.expanduser(f'{Config.values["INV_PATH"]}')
  ]
)

MAX_VOLUME = 10

class Acquire:

    def __init__(self, filename, quantity: int = 1):
        """ Constructor """
        self.filename = filename
        self.item = filename
        if quantity == "":
            quantity = 1
        self.quantity = int(quantity)
        if not Validator.validate(filename):
            sys.exit()
        self.locate(filename)
        self.move()
        self.add()

    def is_box(self, item) -> bool:
        """ Checks if item is a box type """
        self.box = "BoxSpec" in dir(item)

    def is_relic(self, item) -> bool:
        self.relic = "RelicSpec" in dir(item)

    def locate(self, filename: str = "") -> None:
        """ Locates item file in current working directory """
        # TODO: Revise method to look in directory and prompt if there
        #       are multiple similarly-named items.
        self.name, self.ext = self.filename.split("/")[-1].split(".")
        self.name = re.search(r"[a-zA-Z]+", self.name).group(0)
        self.box = Validator.is_box(self.name)
        self.filename = f"{self.name}" # Removed {self.ext}; do we need it?

    # TODO: This is how we dill it </MontelJordan>
    def move(self):
        """ Move the file acquired to the inventory directory """
        try:
            path = os.path.expanduser(
                f'{Config.values["INV_PATH"]}/{self.filename}'
            )
            if not self.box:
                instance = Instance(self.name)
                try:
                    with open(f"{path}","wb") as fh:
                        # TODO: Class inheritance not found?
                        dill.dump(instance.serial, fh)
                    #shutil.copy(self.filename, path)
                except Exception as e:
                    # This operation attempts to move the file
                    # based on real file name; however, if this
                    # fails it might be OK
                    pass
                if "ItemSpec" in dir(instance) or "RelicSpec" in dir(instance):
                    # Remove only the physically present copy
                    os.remove(f"./{self.item}")
        except Exception as e:
            # TODO: Differentiate levels of inacquisition. For
            #       example, use different exceptions defensively.
            print(f"Couldn't acquire {self.name}")
            sys.exit()

    def add(self):
        """ Add the item acquired to the database """
        # TODO: There's a better way to do this than remove from a string.
        item = self.filename.replace(".py", "")
        instance = Instance(item)
        item_volume = instance.get_property("VOLUME") * self.quantity
        current_volume = registry.total_volume() + item_volume
        if MAX_VOLUME >= current_volume:
            try:
                registry.add(self.name, self.quantity)
            except Exception as e:
                print(f"Couldn't acquire {self.name}")
                sys.exit()
        else:
            print(f"Couldn't acquire {self.quantity} {self.name}: Max Volume exceeded")
            sys.exit()
    # TODO: Add resistance for certain magical items or level needs?

class Registry:

    def __init__(self):
        """ Constructor """
        self.inventory = {}
        self.path = os.path.expanduser(
            f'{Config.values["INV_PATH"]}'
        )
        self.conn = sqlite3.connect(
            os.path.expanduser(PATH)
        )
        self.__create_inv_sql_table()
        if os.path.exists(f"{self.path}/.registry"):
            self.__convert_json_file()
            os.unlink(f"{self.path}/.registry")

    def __create_inv_sql_table(self):
        """ Create tables for inventory and other needs based on WORLD_NAME """
        cursor = self.conn.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS items (
                    name TEXT UNIQUE,
                    filename TEXT,
                    quantity REAL,
                    weight REAL,
                    consumable INTEGER,
                    volume REAL GENERATED ALWAYS AS (weight * quantity) STORED
                );
            """
        )
        with pennant.FEATURE_FLAG_CODE(WORLD == "venture"):
            Equipment.configure(conn = self.conn)

    def __convert_json_file(self):
        """ Convert JSON file from earlier versions of topia """
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
                weight = data[item]["volume"]
            )

    def __add_table_entry(
        self,
        name: str = "",
        filename: str = "",
        quantity: float = 1.0,
        weight: float = 0.0
    ):
        """ Add item to table """
        cursor = self.conn.cursor()
        instance = Instance(name)
        cursor.execute(
            """
                INSERT INTO items(name, filename, quantity, weight, consumable)
                VALUES(?, ?, ?, ?, ?);
            """,
            (name,
             filename,
             quantity,
             weight,
             True if instance.get_property("consumable") else False)
        )
        self.conn.commit()

    def __delete_table_entry(self, name: str = "", filename: str = ""):
        """ Delete single entry from table """
        cursor = self.conn.cursor()
        cursor.execute(
            """
                DELETE FROM items WHERE name = ?
            """,
            (name,)
        )
        self.conn.commit()

    def __remove_zero_quantity_items(self) -> None:
        """ Remove items with negative or zero quantity """
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT name, filename FROM items WHERE quantity <= 0.0
            """
        )
        for name, filename in cursor.fetchall():
            self.__delete_table_entry(name, filename)

    def __remove_expended_files(self) -> None:
        """ Remove files from inventory if present, but not in database """
        cursor = self.conn.cursor()
        path = os.path.expanduser(
            Config.values["INV_PATH"]
        )
        files = [item for item in os.listdir(path) if item.endswith(".py")]
        cursor.execute(
            """
                SELECT filename from items;
            """
        )
        items = [file for (file,) in cursor.fetchall()]
        cleanups = set(files) - set(items)
        for file in cleanups:
            os.unlink(f"{path}/{file}")

    def total_volume(self) -> int:
        """ Calculate total volume of inventory """
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
        """ API to add an item to the inventory DB """
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
                UPDATE items
                SET quantity = quantity + {number}
                WHERE name = ?;
            """,
            (item,)
        )
        self.conn.commit()
        if cursor.rowcount != 1:
            self.__add_table_entry(
                name = item,
                filename = f"{item}",
                quantity = number
            )
        self.__remove_zero_quantity_items()
        self.__remove_expended_files()

    def remove(self, item: str, number: int = -1) -> None:
        """ API to remove an item from inventory DB """
        self.add(item = item, number = number)

    def search(self, item: str = "") -> dict:
        """ API to search inventory database """
        # TODO: Expand to allow for multiple item search
        #       using OR logic...er...nah.
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT name, quantity FROM items WHERE name = ? LIMIT 1
            """,
            (item, )
        )
        result = cursor.fetchone()
        if result:
            return {
                "name": result[0],
                "quantity": result[1]
            }
        return {}

    def display(self):
        """ Display contents of inventory to the terminal """
        table = Table(title=f"{os.getenv('LOGNAME')}'s inventory")
        table.add_column("Item name")
        table.add_column("Item count")
        table.add_column("Consumable")
        table.add_column("Volume")
        with pennant.FEATURE_FLAG_CODE(WORLD == "venture"):
            table.add_column("Equippable")
            table.add_column("Durability")
            table.add_column("Equipped")

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, filename, quantity, consumable, volume FROM items
        """)

        path = os.path.expanduser(
            f"{Config.values['INV_PATH']}"
        )

        for name, filename, quantity, consumable, volume in cursor.fetchall():
            data = [str(name), str(quantity), str(bool(consumable)), str(volume)]
            with pennant.FEATURE_FLAG_CODE(WORLD == "venture"):
                with open(f"{path}/{name}", "rb") as fh:
                    instance = dill.load(fh)
                data += [
                    str(True if instance.slot else False),
                    str(instance.durability or "-"),
                    str(Equipment.discover(cursor, name) or "-")                ]
            table.add_row(*data)

        console = Console()
        console.print(table)
        print(f"Your current total volume limit is: {self.total_volume()}/{MAX_VOLUME}\n")

class Items:

    def __init__(self, registry):
        """ Constructor """
        self.inv = registry

    @staticmethod
    def is_fixture(mro: list = []) -> bool:
        """ Returns fixture specification status """
        return "FixtureSpec" in dir(item)

    @staticmethod
    def is_box(mro: list = []) -> bool:
        """ Returns box specification status """
        return "BoxSpec" in dir(item)

    @staticmethod
    def is_relic(mro: list = []) -> bool:
        return "RelicSpec" in dir(item)

    def trash(self, item: str, quantity: int = 1) -> None:
        """ Removes item from the list; tied to the "remove" .bashrc alias """
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1
        try:
            registry.add(item, 0 - int(quantity))
        except:
            pass

    def drop(self, item: str = "", quantity: int = 1) -> None:
        """ Drops item copy in current directory; removes from inventory """
        try:
            result = registry.search(item = item)
            if not result:
                raise OutOfError(item)
        except OutOfError:
            print(f"It doesn't look like you have any {item}.")
            sys.exit()
        except ValueError:
            quantity = 1
        # Convert the quantity to an integer if not already one
        quantity = int(quantity)
        # Test if the number being dropped is more than we have
        # and limit the drops to only the quantity that we have
        if quantity > result["quantity"]:
            quantity = result["quantity"]
        try:
            for _ in range(quantity):
                Factory(item)
            registry.add(item, 0 - int(quantity))
        except:
            pass

    @pennant.FEATURE_FLAG_FUNCTION(WORLD == "venture")
    def equip(self, item: str):
        try:
            result = registry.search(item = item)
            if not result:
                raise OutOfError(item)
            Equipment.equip(registry.conn, item)
        except OutOfError:
            print(f"It doesn't look like you have any {item}.")
            sys.exit()

    @pennant.FEATURE_FLAG_FUNCTION(WORLD == "venture")
    def unequip(self, item: str):
        try:
            result = registry.search(item = item)
            if not result:
                raise OutOfError(item)
            Equipment.unequip(registry.conn, item)
        except OutOfError:
            print(f"It doesn't look like you have any {item}.")
            sys.exit()

    @pennant.FEATURE_FLAG_FUNCTION(WORLD == "venture")
    def equipped(self):
        table = Table(title=f"{os.getenv('LOGNAME')}'s equipment")
        table.add_column("Slot")
        table.add_column("Item")
        for slot, value in Equipment.show(registry.conn.cursor()):
            table.add_row(slot, value)
        console = Console()
        console.print(table)

    @classmethod
    def use(self, item: str = ""):
        """ Uses an item from the inventory """
        # Set up properties and potential kwargs
        box = False
        fixture = False

        # Verify that item is in path or inventory
        try:
            path = os.path.expanduser(
                f"{Config.values['INV_PATH']}/{item}"
            )
            with open(path, "rb") as fh:
                instance = dill.load(fh)
        except ModuleNotFoundError:
            print(f"You don't seem to have any {item}.")
            sys.exit()

        # Test type of item; remove if ItemSpec
        try:
            record = registry.search(item)
            # Retrieves superclasses from MRO; prevents
            # incompatible use cases
            mro = [cls.__name__ for cls in instance.__mro__]
            # Only decrease quantity if item is consumable
            if instance.consumable:
                registry.remove(item)
            if record["quantity"] <= 0:
                raise OutOfError(item)
        except (KeyError, OutOfError) as e:
            print(f"You have no {item} remaining!")
            registry.remove(item = item)
            sys.exit()
        except IsFixture: pass
        # Return the result or inbuilt use method
        if type(instance).__str__ is not object.__str__:
            instance.use(instance, **instance.actions)
        else:
            return instance.use(instance, **instance.actions)

# Create instances to use as shorthand. I thought this was a bad idea,
# but this is actually how the random module works:
# https://github.com/python/cpython/blob/main/Lib/random.py

registry = Registry()
items = Items(registry)
