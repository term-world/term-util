import json
from datetime import datetime

class Cookie:

    def __init__(self, name: str = "", kind = "ad"):
        """ Constructor """
        self.name = name
        self.kind = kind
        self.__triggered = False
        
    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def duration(self):
        return self.__duration

    @property
    def contents(self):
        return self.__contents

    @property
    def triggered(self):
        return self.__triggered

    @duration.setter
    def duration(self, duration: int = 0) -> None:
        """ Sets trigger duration """
        self.__duration = duration
    
    @contents.setter
    def contents(self, contents: any = "") -> None:
        """ Sets content of the cookie """
        self.__contents = contents
    
    @contents.getter
    def contents(self) -> any:
        """ Returns the value of the contents variable """
        return self.__contents
         
    @triggered.setter
    def triggered(self, is_triggered: bool = True) -> None:
        """ Sets the value of the cookie trigger """
        self.__triggered = is_triggered