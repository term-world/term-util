from couchsurf import Connection

from .record import Library

class Query:

    conn = Connection("marketplace")

    def __init__(self, **kwargs):
        terms = {
            "type":{"op":"EQUALS", "arg":"library"}
        }
        for arg in kwargs:
            op = "GREATER THAN"
            if not type(kwargs[arg]) == list:
                op = "LIKE"
            terms.update({
                arg:{"op":op, "arg":kwargs[arg]}
            })
        self.result = Result(self.__run(terms))

    def __run(self, terms: dict = {}):
        result = self.conn.request.query(
            **terms
        )
        return result["docs"]

class Result:

    def __init__(self, data: any = ""):
        self.data = data
        self.list()

    def list(self) -> None:
        print(f"Found {len(self.data)} results.", end = "\n")
        for entry in self.data:
            entry = Library(**entry)
            print(f"  * {entry.name}", end = "\n")

    def enumerate(self) -> dict:
        for entry in self.data:
            yield entry
