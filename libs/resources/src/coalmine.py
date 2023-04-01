import json

from resources import Exhaustible

def mine() -> int:
    res = Exhaustible()
    res.load_file("/world/coalmine")
    if can_mine(res):
        res.update_file("/world/coalmine")
        return 100
    return 0

def can_mine(data) -> bool:
    if data["level"] - 100 > 0:
        return True
    return False
