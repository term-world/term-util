from inventory import FixtureSpec

class Test(FixtureSpec):

    def __str__(self) -> str:
        return "Test complete!"

    def use(self):
        print(self.__str__())
