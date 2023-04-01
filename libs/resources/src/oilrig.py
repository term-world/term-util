import json

from resources import Exhaustible

def drill() -> int:
    res = Exhaustible()
    res.load_file("/world/oilfield")
    if can_drill(res):
        res.update_file("/world/oilfield")
        return 100
    return 0

def can_drill(data) -> bool:
    if data["level"] - 100 > 0:
        return True
    return False
