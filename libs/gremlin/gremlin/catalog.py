from couchsurf import Connection

class Entry:

    def __init__(self, name: str = "", **kwargs):
        self.conn = Connection("relics")
        self.data = self.__query(name = name)
        if len(self.data) > 1:
            print("Whoa, whoa! Too much magic is none at all!")
        if not self.data:
            self.__register(name = name, **kwargs)
            self.data = self.__query(name=name)
    
    def __query(self, **kwargs):
        terms = {
            "type": {"op": "EQUALS", "arg": "NPC"}
        }
        for arg in kwargs:
            terms.update({
                arg:{"op": "LIKE", "arg": kwargs[arg]}
            })
        return self.__run(terms)
    
    def __run(self, terms: dict = {}):
        result = self.conn.request.query(
            **terms
        )
        try:
            return result["docs"]
        except KeyError:
            pass

    def __register(self, **kwargs):
        data = {
            "type": "NPC"
        }
        for prop in kwargs:
            data.update({
                prop: kwargs[prop]
            })
        if not "stats" in kwargs:
            data.update({
                "stats": self.STATS
            })
        if "_id" in data:
            id = data["_id"]
            del data["_id"]
        else:
            id = self.conn.request.get_new_id()
        self.conn.request.put(
            doc_id = id,
            doc = data
        )
    
    def update(self, npc: object):
        data = {
            "_id": npc._id,
            "_rev": npc._rev
        }
        for prop in npc.__dict__:
            if not prop.startswith("_"):
                data[prop] = npc.__dict__[prop]
        self.__register(**data)
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value