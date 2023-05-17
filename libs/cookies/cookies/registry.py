import os
import json

from .cookie import Cookie

FILENAME = os.path.expanduser("~/.cookies")

def load_cookies(filename = "") -> dict:
    with open(filename, "r") as fh:
        return json.load(fh)

def register(cookie: Cookie = Cookie()):
    cookies = load_cookies(FILENAME)
    cookies.update(str(cookie))
    with open(FILENAME, "w") as fh:
        json.dump(cookies, fh)

def fetch(kind: str = "") -> dict:
    cookies = load_cookies(FILENAME)
    try:
        return cookies[kind]
    except KeyError:
        return {}