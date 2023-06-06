import os
import base64
import shutil
import zipapp

from hashlib import md5
from couchsurf import Connection

class Package:

    def __init__(self, name: str = "", files: any = ""):
        """ Constructor """
        self.files = files
        if type(files) == str:
            self.files = [files]
        self.name = name
        self.pkgfile = f"{self.name}.pyz"

    def folder(self, file: str = "") -> None:
        """ Add all files to folder """
        os.makedirs(
            self.name,
            exist_ok = True
        )
        shutil.copy(
            file,
            f"{self.name}/{file}"
        )

    def entrypoint(self) -> None:
        """ Designates title file as entrypoint """
        with open(f"{self.name}/{self.name}.py", "a") as fh:
            fh.write(f"""
if __name__ == "{self.name}":
    {self.name}().use()""")

    def make(self, options: dict = {}) -> None:
        """ Makes *.pyz file for object """
        if not options:
            options = {
                "name": self.name,
                "target": f"{self.name}.pyz",
                "compress": True,
                "main": f"{self.name}:{self.name}",
                "interpreter": "/usr/bin/python"
            }
        if not os.path.isdir(self.name):
            for file in self.files:
                self.folder(file = file)
        self.entrypoint()
        zipapp.create_archive(
            options["name"],
            target = options["target"],
            main = options["main"],
            compressed = options["compress"],
            interpreter = options["interpreter"]
        )
        if not os.path.isdir(self.name):
            shutil.rmtree(self.name)

    def verify(self, checksum: str = ""):
        # TODO: What happens if no file shows up? ERR!
        pack = self.pkgfile
        with open(pack, "rb") as fh:
            data = fh.read()
        chex = base64.b64decode(
            checksum.split("md5-")[1]
        ).hex()
        if chex != md5(data).hexdigest():
            print(chex)
            print(md5(data).hexdigest())
            print("Downloaded file different from market version! Exiting.")
            #os.unlink(f"{self.name}.pyz")
            exit()

    def retrieve(self, doc_id: str = "") -> None:
        pack = self.files[0]
        conn = Connection("marketplace")
        # TODO: Determine whether or not we need to get the attachment
        #       md5 here, too -- seems...wasteful?
        binary = conn.request.download(f"{doc_id}/{self.pkgfile}")
        checksum = conn.request.get(doc_id)["_attachments"][self.pkgfile]["digest"]
        with open(f"{self.name}.pyz", "wb") as fh:
            fh.write(binary)
        self.verify(checksum)
