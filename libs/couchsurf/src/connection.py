import os
import re
import json
import requests

class Connection:

    CONFIG = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASS": os.getenv("DB_PASS")
    }

    HEADERS = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'referer': f'https://{CONFIG["DB_HOST"]}'
    }

    AUTH_STRING = f'{CONFIG["DB_USER"]}:{CONFIG["DB_PASS"]}@{CONFIG["DB_HOST"]}'
