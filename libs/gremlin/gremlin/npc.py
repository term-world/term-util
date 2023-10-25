import os
import openai

from .catalog import Entry # from catalog import class Entry
from helper import Helper # if i wanted to import Helper class

class NPC: # use NPC as a super class for other characters?

    def __init__(self, name: str = "", **kwargs): 
    ''' intializes the attribites (variables) of object NPC '''
        # **kwargs is used when you're unsure about the number of arguments to pass in function
        # using **kwargs creates a dictionary of arguments
        self.__entry = Entry(name = name, **kwargs) 
        # creates attribute called __entry, assigns value of class Entry
        self.__stats(*self.__entry.data)
        # creates attribute called __stats

    def __stats(self, data: dict = {}, **kwargs):
    ''' stats method, take dictionary called 'data' as parameter  '''
        for prop in kwargs: # for property in dictionary (?) '**kwargs'
            data.update({ 
                prop: kwargs[prop]
            }) 
        for prop in data: # for property in dictionary 'data'
            setattr(self, prop, data[prop]) 
            # sets property attribute object NPC to value property in dictionary 'data'
    
    def update(self):
        self.__entry.update(self) # update entry for NPC object
