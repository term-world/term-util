from inventory.Item import RelicSpec

class Glove(RelicSpec):

    def __init__(self):
        super().__init__(__file__)
        self.slot = "right"
