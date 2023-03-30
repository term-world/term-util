from couchsurf import Connection

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
        self.result = self.__run(terms)

    def __run(self, terms: dict = {}):
        result = self.conn.request.query(
            **terms
        )
        if len(result["docs"]) == 1:
            return result["docs"][0]
        return result["docs"]
