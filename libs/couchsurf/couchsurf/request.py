import os
import json
import base64
import pickle
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

    def get_new_id(self) -> str:
        """ Retrieves a single unassigned UUID """
        uuids = self.get("_uuids")
        return uuids["uuids"][-1]

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
        result = self.post(query, "_find")
        return result

    def download(self, endpoint: str = "") -> bytes:
        filebytes = []
        response = requests.get(
            f'http://{self.auth}/{self.name}/{endpoint}',
            headers = self.headers,
            stream = True
        )
        for chunk in response.iter_content(chunk_size = 1024):
            if chunk:
                filebytes.append(chunk)
        return b''.join(filebytes)

    def put(self, doc_id: str = "", doc: dict = {}, **kwargs) -> dict:
        request_uri = f'http://{self.auth}/{self.name}/{doc_id}'
        response = requests.put(
            request_uri,
            headers = self.headers,
            data = json.dumps(doc)
        )
        confirmation = json.loads(response.text)
        if "attachment" in kwargs:
            # Check if attachment is a file, if so: read
            if os.path.isfile(kwargs["attachment"]):
                with open(kwargs["attachment"], 'rb') as fh:
                    data = fh.read()
                self.headers["Content-Type"] = "application/zip"
            else:
                # If the attachment is a bytes-like object, upload
                try:
                    if not type(kwargs["attachment"]) == bytes:
                        raise
                    if "name" not in kwargs:
                        print("Please provide a name parameter!")
                        exit()
                    data = kwargs["attachment"]
                    kwargs["attachment"] = kwargs["name"]
                except Exception as e:
                    print("Must be bytes-like or a file!")
                    exit()
                self.headers["Content-Type"] = "application/octet-stream"
            request_uri += f'/{kwargs["attachment"]}'
            self.headers["If-Match"] = confirmation["rev"]
            response = requests.put(
                request_uri,
                headers = self.headers,
                data = data
            )
            confirmation = json.loads(response.text)
        return confirmation

    def post(self, doc: str = "", op: str = "") -> dict:
        response = requests.post(
            f'http://{self.auth}/{self.name}/{op}',
            headers=self.headers,
            data=json.dumps(doc)
        )
        confirmation = json.loads(response.text)
        return confirmation
