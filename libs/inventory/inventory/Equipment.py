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
    def verify_valid_slot(cursor: sqlite3.Cursor, name: str, slot: str) -> bool:
        if not instance.is_child_of(RelicSpec):
            raise EquipError
        cursor.execute(
            f"""
                SELECT * FROM equipment
                WHERE slot = {slot}
            """
        )
        print(cursor.rowcount)
        return True

    @staticmethod
    def configure(conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        # Create equipment table

        # TODO: Fix uniqueness integrity error -- e.g. "hand"
        #       has only one possible entry!

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS equipment (
                    slot TEXT UNIQUE,
                    side TEXT,
                    name TEXT
                );
            """
        )

        # Set trigger to validate slot assignment on update
        # TODO: Consider moving verify_slot to Validator
        conn.create_function("verify_valid_slot", 2, Equipment.verify_valid_slot)
        cursor.execute(
            """
                CREATE TRIGGER IF NOT EXISTS inv_equipment_validate_slot
                BEFORE UPDATE ON equipment
                WHEN verify_valid_slot(NEW.slot, NEW.side, NEW.name)
                BEGIN
                    INSERT INTO equipment(slot, side, name)
                    VALUES (NEW.slot, NEW.side, NEW.name);
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
    def equip(conn: sqlite3.Connection, name: str = "") -> bool:
        instance = Instance(name)
        slot = instance.get_property("slot")["location"].value
        side = Equipment.choose_equip_side(
            sides = instance.get_property("slot")["side"]
        )
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                    INSERT INTO equipment(slot, side, name)
                    VALUES(?, ?, ?)
                """,
                (slot, side, name)
            )
            conn.commit()
        except sqlite3.IntegrityError as err:
            print(err)
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
