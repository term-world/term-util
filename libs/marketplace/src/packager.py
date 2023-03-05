import os
import shutil
import zipapp

class Package:

    def __init__(self, name: str = "", files: any = ""):
        self.files = files
        if type(files) == str:
            self.files = [files]
        self.name = name
        self.single = False
        if len(self.files) < 2:
            self.single = True

    def folder(self, file: str = "") -> None:
        os.makedirs(
            self.name,
            exist_ok = True
        )
        shutil.copy(
            file,
            f"{self.name}/{file}"
        )

    def make(self, options: dict = {}) -> None:
        if not options:
            options = {
                "name": self.name,
                "target": f"{self.name}.pyz",
                "compress": True
            }
        options["main"] = f"{self.name}:{self.name}"
        for file in self.files:
            self.folder(file = file)
            if file.split(".")[0] == self.name:
                with open(f"{self.name}/{file}", "a") as fh:
                    fh.write(f"""if __name__ == '{self.name}':
                        {self.name}().use()""")
        zipapp.create_archive(
            options["name"],
            target = options["target"],
            main = options["main"],
            compressed = options["compress"]
        )
        shutil.rmtree(self.name)
