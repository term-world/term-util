import json
from time import time

class Block:

    def __init__(self):
        self.index = None
        self.txns = None
        self.prev_hash = None
        self.timestamp = time()

    def __str__(self) -> str:
        return json.dumps({
            "index": self.index,
            "txns": self.txns,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp
        })
