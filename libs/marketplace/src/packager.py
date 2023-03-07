import os
import base64
import shutil
import zipapp

from hashlib import sha256

class Package:

    def __init__(self, name: str = "", files: any = ""):
        """ Constructor """
        self.files = files
        if type(files) == str:
            self.files = [files]
        self.name = name

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
            fh.write(f"""if __name__ == "{self.name}":
                {self.name}().use()""")

    def checksum(self) -> str:
        with open(f"{self.name}.pyz", "rb") as fh:
            data = base64.b64encode(
                fh.read()
            )
        return sha256(data).hexdigest()

    def make(self, options: dict = {}) -> str:
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
        return self.checksum()
