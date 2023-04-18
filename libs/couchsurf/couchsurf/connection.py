import os

from .request import Request

class Connection:

    DB = {
        "HOST": os.getenv("DB_HOST"),
        "USER": os.getenv("DB_USER"),
        "PASS": os.getenv("DB_PASS")
    }

    HEADERS = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'referer': f'https://{DB["HOST"]}'
    }

    def __init__(self, db_name: str = ""):
        try:
            db_name = str(db_name)
            if not db_name:
                raise
        except:
            print("Couchsurf: Invalid or empty database name in connection.")
            return
        self.DB["NAME"] = db_name
        self.request = Request(self.DB, self.HEADERS)
