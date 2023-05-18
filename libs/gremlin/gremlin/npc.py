import os
import openai

from couchsurf import Connection

class NPC:
    
    API = {
        "key": os.getenv("OPEN_AI_KEY"),
        "org": os.getenv("OPEN_AI_ORG")
    }

    HEALTH = 1
    ATTACK = 0
    DEFEND = 0

    def __init__(self, name: str = ""):
        self.conn = Connection("npcs")
        self.__query(name = name)
    
    def __query(self, **kwargs):
        terms = {
            "type": {"op": "EQUALS", "arg": "npc"}
        }
        for arg in kwargs:
            terms.update({
                arg:{"op": "LIKE", "arg": kwargs[arg]}
            })
        self.__run(terms)
    
    def __run(self, terms: dict = {}):
        result = self.conn.request.query(
            **terms
        )
        return result["docs"]

    def __register(self):
        pass
    
    def __unregister(self):
        pass