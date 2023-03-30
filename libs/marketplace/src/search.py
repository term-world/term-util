from couchsurf import Connection

class Query:

    conn = Connection("marketplace")

    def __init__(self, **kwargs):
        terms = {
            "type":{"op":"EQUALS", "arg":"Library"}
        }
        for arg in kwargs:
            terms.update({
                arg:{"op":"LIKE", "arg":kwargs[arg]}
            })
        self.__run(terms)

    def __run(self, terms: dict = {}):
        result = self.conn.request.query(
            **terms
        )
        print(result)
