import os
import random

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

from base64 import b64encode
from getpass import getpass

class Signature:

    def __init__(self, data: str = ""):
        self.digest = SHA256.new()
        self.digest.update(data.encode('utf-8'))
        self.__load_private_key()
        self.__affix_signature()

    def __str__(self) -> str:
        try:
            return self.signature.hex()
        except:
            return "ERROR: NOTHING HAS BEEN SIGNED!"

    def __load_private_key(self):
        # TODO: What if user calls it something else?
        path = os.path.expanduser("~/.ssh/id_rsa")
        with open(path, "r") as key:
            lines = key.readlines()
            self.private_key = RSA.import_key(
                ''.join(lines),
                passphrase = getpass()
            )

    def __affix_signature(self):
        signer = PKCS1_v1_5.new(self.private_key)
        self.signature = signer.sign(self.digest)
