import os
import sys
import enum
import inspect
import pennant
import narrator
import sqlite3

from typing import Any
from arglite import parser as cliarg

from .Item import RelicSpec
from .Instantiator import Instance

class Equipment:

    # TODO: There are a lot of duplicated methods testing
    #       types, et al. We need to remove/conslidate them.

    def choose_equip_side(sides) -> str:
        if type(sides) == RelicSpec.Slots:
            return sides.value
        if type(sides) == list and len(sides) == 1:
            return sides[-1].value
        q = narrator.Question({
            "question": "Equip to which side?\n",
            "responses": [
                {"choice": side.value, "outcome": side.value} for side in sides
            ]
        })
        return q.ask()

    # TODO: Seems to belong in Validator, tho.
    @staticmethod
    def verify_valid_slot(name: str = "", slot: Any = "") -> bool:
        # Jump the queue if unequipping!
        if inspect.stack()[1].function == "unequip":
            return True
        instance = Instance(name)
        slots = instance.get_property("slot")["location"]
        if type(slots) == RelicSpec.Slots:
            slots = [slots]
        for slot in slots:
            if slot not in RelicSpec.Slots: return False
        return True

    @staticmethod
    def configure(conn: sqlite3.Connection) -> None:
        """ Configure table on first-time run """
        cursor = conn.cursor()

        # Create equipment table
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS equipment (
                    slot TEXT UNIQUE,
                    side TEXT,
                    name TEXT
                );
            """
        )

        cursor.execute(
            """
                SELECT * FROM equipment;
            """
        )

        if len(cursor.fetchall()) < 1:
            for slot in RelicSpec.Slots:
                cursor.execute(
                    """
                        INSERT INTO equipment(slot) VALUES(?);
                    """,
                    (slot.value,)
                )
            conn.commit()

        # Set trigger to validate slot assignment on update
        conn.create_function("verify_valid_slot", 2, Equipment.verify_valid_slot)

        with pennant.FEATURE_FLAG_CODE(cliarg.optional.debug):
            sqlite3.enable_callback_tracebacks(True)

        cursor.execute(
            """
                CREATE TRIGGER IF NOT EXISTS inv_equipment_validate_slot
                BEFORE UPDATE ON equipment
                WHEN verify_valid_slot(NEW.name, NEW.slot)
                BEGIN
                    UPDATE equipment
                    SET name = NEW.name
                    WHERE slot = NEW.slot;
                END;
            """
        )

        # Set trigger to prevent additional slot creation
        cursor.execute(
            """
                CREATE TRIGGER IF NOT EXISTS inv_equipment_limit_slots
                BEFORE INSERT ON equipment
                BEGIN
                    SELECT raise(ABORT, "Sike!");
                END;
            """
        )

    @staticmethod
    def discover(cursor: sqlite3.Cursor, name: str = "") -> str:
        cursor.execute(
            """
                SELECT * FROM equipment WHERE name = ?
            """,
            (name,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

    @staticmethod
    def equip(conn: sqlite3.Connection, name: str = "") -> bool:
        instance = Instance(name)
        slot = Equipment.choose_equip_side(
            instance.get_property("slot")["location"]
        )
        print(slot)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                    UPDATE equipment
                    SET name = ?
                    WHERE slot = ?
                """,
                (name, slot, )
            )
            conn.commit()
        except sqlite3.IntegrityError as err:
            print("Invalid slot for item!")
            sys.exit()
        return bool(cursor.rowcount)

    @staticmethod
    def unequip(conn: sqlite3.Connection, name: str = "") -> bool:
        instance = Instance(name)
        # TODO: Fix for multi-slot cases (iteratives).
        slots = instance.get_property("slot")["location"]
        if type(slots) == RelicSpec.Slots:
            slots = [slots]
        cursor = conn.cursor()
        for slot in slots:
            cursor.execute(
                """
                    UPDATE equipment
                    SET name = ""
                    WHERE name = ? AND slot = ?
                """,
                (name, slot.value, )
            )
            if cursor.rowcount == 1:
                conn.commit()

    @staticmethod
    def show(cursor: sqlite3.Cursor):
        cursor.execute(
            """
                SELECT slot, name FROM equipment;
            """
        )
        return cursor.fetchall()

class EquipError(Exception):

    def __init__(self, item:str, *args):
        super().__init__(args)
        print("Can't equip {item}.")
        sys.exit()

class InvalidSlotError(Exception):

    def __init__(self, *args):
        super().__init__(args)
        print("Not an equippable slot.")
        sys.exit()
