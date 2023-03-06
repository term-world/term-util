import json
import base64
import requests

class Request:

    def __init__(self, config: dict = {}, headers: dict = {}):
        self.host = config["HOST"]
        self.user = config["USER"]
        self.passwd = config["PASS"]
        self.name = config["NAME"]
        self.auth = f"{self.user}:{self.passwd}@{self.host}"
        self.headers = headers

    def get(self, endpoint: str = "", **kwargs) -> dict:
        params = None
        if kwargs:
            params = {
                "keys": json.dumps([value for value in kwargs.values()])
            }
        if not endpoint.startswith("_"):
            endpoint = f"{self.name}/{endpoint}"
        response = requests.get(
            f'http://{self.auth}/{endpoint}',
            headers = self.headers,
            params = params
        )
        return json.loads(response.text)

    def view(self, view_path: str = "", **kwargs) -> dict:
        params = None
        if kwargs:
            params = {
                "keys": json.dumps([value for value in kwargs.values()])
            }
        response = requests.get(
            f'http://{self.auth}/{self.name}/_design/latest/_view/{view_path}',
            headers = self.headers,
            params = params
        )
        return json.loads(response.text)

    def query(self, **kwargs) -> dict:
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
        result = post(query, "_find")
        return result

    def put(self, doc_id: str = "", doc: dict = {}, **kwargs) -> dict:
        request_uri = f'http://{self.auth}/{self.name}/{doc_id}'
        response = requests.put(
            request_uri,
            headers = self.headers,
            data = json.dumps(updated_doc)
        )
        confirmation = json.loads(response.text)
        if "attachment" in kwargs:
            with open(kwargs["attachment"], 'rb') as fh:
                updated_doc["_attachments"] = {
                    f'{kwargs["attachment"]}': {
                        "data": base64.b64encode(
                            fh.read()
                        ).decode('utf-8')
                    }
                }
            request_uri += f'/{kwargs["attachment"]}'
            self.headers["If-Match"] = confirmation["rev"]
            self.headers["Content-Type"] = "application/zip"
            response = requests.put(
                request_uri,
                headers = self.headers,
                data = json.dumps(updated_doc["_attachments"][kwargs["attachment"]]["data"])
            )
            confirmation = json.loads(response.text)
        return confirmation

    def post(self, doc: str = "", op: str = "") -> dict:
        response = requests.post(
            f'https://{self.auth}/{self.name}/{op}',
            headers=self.headers,
            data=json.dumps(doc)
        )
        confirmation = json.loads(response.text)
        return confirmation
