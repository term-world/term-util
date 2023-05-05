import os

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

from base64 import b64decode

class Verify:

    def __init__(self, data: str = "", signature: bytes = b""):
        self.digest = SHA256.new()
        self.digest.update(data.encode('utf-8'))
        self.signature = bytes.fromhex(signature)
        self.__load_public_key()

    def __bool__(self) -> bool:
        verification = PKCS1_v1_5.new(self.public_key)
        return verification.verify(self.digest, self.signature)

    def __load_public_key(self):
        # TODO: What if user calls it something else?
        path = os.path.expanduser("~/.ssh/id_rsa.pub")
        with open(path, "r") as key:
            self.public_key = RSA.importKey(key.read())
