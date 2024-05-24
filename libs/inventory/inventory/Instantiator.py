import importlib

class Instance:

    def __init__(self, item: str = ""):
        """ Instantiate object to access runnable properties """
        try:
            self.module = importlib.import_module(f"{item}")
            self.uninst = getattr(self.module, item)
            self.object = self.uninst()
            self.serial = self.uninst.dillable(self.uninst)
        except ModuleNotFoundError:
            print(f"It seems you don't have any {item}.")
            exit()
        except Exception as e:
            print(e)
            print(f"{item} doesn't seem to be a valid object.")
            exit()
