import os
import sys
import narrator
import sqlite3

from enum import Enum

from .Item import RelicSpec
from .Instantiator import Instance

class Equipment:

    @staticmethod
    def verify_slot(filename: str = "", slot: str = "") -> bool:
        instance = Instance(filename)
        if not instance.is_child_of(RelicSpec):
            raise EquipError
        if not instance.get_property("slot") == slot:
            raise InvalidSlotError
        return True

    @staticmethod
    def configure(conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        # Create equipment table
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS equipment (
                    slot TEXT UNIQUE,
                    filename TEXT
                );
            """
        )

        # Create standard slots as rows without values
        # TODO: Implement ENUM

        # Set trigger to validate slot assignment on update
        # TODO: Consider moving verify_slot to Validator
        conn.create_function("verify_slot", 2, Equipment.verify_slot)
        cursor.execute(
            """
                CREATE TRIGGER IF NOT EXISTS inv_equipment_validate_slot
                BEFORE UPDATE ON equipment
                WHEN verify_slot(NEW.filename, NEW.slot)
                BEGIN
                    INSERT INTO equipment(slot, filename)
                    VALUES (NEW.slot, NEW.filename);
                END;
            """
        )

        # Set trigger to prevent additional slot creation
        # TODO: Reenable when finished with table creation
        #cursor.execute(
        #    """
        #        CREATE TRIGGER inv_equipment_limit_slots
        #        BEFORE INSERT ON equipment
        #        BEGIN
        #            SELECT raise(ABORT, "Sike!");
        #        END;
        #    """
        #)

    @staticmethod
    def equip(cursor: sqlite3.Cursor, filename: str = "", slot: str = "") -> bool:
        try:
            cursor.execute(
                """
                    INSERT INTO equipment(slot, filename)
                    VALUES(?, ?)
                """,
                (slot, filename)
            )
        except sqlite3.IntegrityError:
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
