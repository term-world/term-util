import json
import hashlib
import urllib

from block import Block

class Chain:

    def __init__(self):
        """ Constructor """
        # If new chain
        self.chain = []
        self.nodes = set()
        # Transactions
        self.txns = []
        # Genesis block
        self.make_block(prev_hash = '1')
        # TODO: Load chain from RocksDB?
        #       This requires a Merkle Tree.

    def make_block(self, prev_hash: str = None) -> Block:
        # Make the block
        block = Block()
        block.index = len(self.chain) + 1
        if not prev_hash:
            prev_hash = self.calc_hash(self.prev_block())
        block.prev_hash = prev_hash
        # Append block to the chain
        self.chain.append(block)
        # Clear the pending transactions list
        self.txns.clear()
        return block

    def prev_block(self):
        """ Returns the latest block in the chain """
        return self.chain[-1]

    @staticmethod
    def calc_hash(block: Block = Block()) -> str:
        hash_string = json.dumps(str(block), sort_keys = True).encode()
        return hashlib.sha256(hash_string).hexdigest()
