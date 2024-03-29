import importlib

class Instance:

    def __init__(self, item: str = ""):
        """ Instantiate object to access runnable properties """
        try:
            item_file = importlib.import_module(f"{item}")
            self.instance = getattr(item_file, item)()
        except ModuleNotFoundError:
            print(f"It seems you don't have any {item}.")
            exit()
        except:
            print(f"{item} doesn't seem to be a valid object.")
            exit()

    def has_property(self, prop: str = "") -> bool:
        try:
            getattr(self.instance, prop)
            return True
        except:
            pass
        return False

    def get_property(self, prop: str = ""):
        try:
            return getattr(self.instance, prop)
        except:
            pass

    def is_child_of(self, item_type) -> bool:
        res_order = self.instance.__mro__
        print(item_type in res_order)
