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

    def has_property(self, prop: str = "") -> bool:
        try:
            getattr(self.object, prop)
            return True
        except:
            pass
        return False

    def get_property(self, prop: str = ""):
        try:
            return getattr(self.object, prop)
        except:
            pass

    def is_child_of(self, item_type) -> bool:
        res_order = self.object.__mro__
        print(item_type in res_order)
