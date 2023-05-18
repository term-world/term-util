import os
import openai

from .catalog import Entry

class NPC:

    def __init__(self, name: str = "", **kwargs):
        self.__entry = Entry(name = name, **kwargs)
        self.__stats(*self.__entry.data)

    def __stats(self, data: dict = {}, **kwargs):
        for prop in kwargs:
            data.update({
                prop: kwargs[prop]
            })
        for prop in data:
            setattr(self, prop, data[prop])
    
    def update(self):
        self.__entry.update(self)