import json
import requests

from .connection import *

class Request:

    def __init__(self, connection: Connection = Connection()):
        self.host = connection.CONFIG["DB_HOST"]
        self.user = connection.CONFIG["DB_USER"]
        self.passwd = connection.CONFIG["DB_PASS"]
        self.headers = connection.HEADERS
        self.auth = f"{self.user}:{self.passwd}@{self.host}"

    def get(self, db_name: str = "", view_path: str = "", **kwargs) -> dict:
        params = None
        if kwargs:
            params = {
                "keys": json.dumps([value for value in kwargs.values()])
            }
        response = requests.get(
            f'http://{self.auth}/{db_name}/_design/latest/_view/{view_path}',
            headers = self.headers,
            params = params
        )
        return json.loads(response.text)

    def query(self, **kwargs):
        """
            Example:
            couchsurf.query_request(
                scope={"op":"EQUALS", "arg":"global"},
                flag ={"op":"EQUALS", "arg":"active"}
            )
        """
        operators = {
            "LESS THAN": "$lt",
            "GREATER THAN": "$gt",
            "EQUALS":"$eq",
            "LIKE": "$regex"
        }
        for param in kwargs:
            op = kwargs[param]["op"]
            arg = kwargs[param]["arg"]
            if op == "LIKE": arg = f"(*UTF8)(?i){arg}"
            kwargs[param] = {
                operators[op]:f"{arg}"
            }
        query = {
            "selector":kwargs
        }
        result = __post(query, "_find")
        return result

    def __post(self, doc: str = "", op: str =""):
        response = requests.post(
            f'https://{self.auth}/{op}',
            headers=self.headers,
            data=json.dumps(doc)
        )
        confirmation = json.loads(response.text)
        return confirmation

    def __put(self,doc_id: str = "", updated_doc: str = ""):
        response = requests.put(
            f'https://{self.auth}/{doc_id}',
            headers=self.headers,
            data=json.dumps(updated_doc)
        )
        confirmation = json.loads(response.text)
        return confirmation
