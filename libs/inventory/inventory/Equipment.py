import os
import sys
import enum
import narrator
import sqlite3

from .Item import RelicSpec
from .Instantiator import Instance

class Equipment:

    # TODO: There are a lot of duplicated methods testing
    #       types, et al. We need to remove/conslidate them.

    def choose_equip_side(sides: list = []) -> str:
        """ Deprecated, or at least out of current use (RETAIN) """
        if type(sides) == str or len(sides) == 1:
            return [sides][-1]
        q = narrator.Question({
            "question": "Equip to which side?\n",
            "responses": [
                {"choice": side.value, "outcome": side.value} for side in sides
            ]
        })
        return q.ask()

    # TODO: Seems to belong in Validator, tho.
    @staticmethod
    def verify_valid_slot(name: str = "", slot: str = "") -> bool:
        instance = Instance(name)
        return instance.get_property("slot")["location"] in RelicSpec.Slots

    @staticmethod
    def configure(conn: sqlite3.Connection) -> None:
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
        # TODO: Reenable when finished with table creation
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
        slot = instance.get_property("slot")["location"].value
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
