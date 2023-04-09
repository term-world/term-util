import requests

from .Config import Config

from fake_useragent import UserAgent

ua = UserAgent()

def get(
      raw_path: str = Config.values["URL"],
      file_type: str = "objects",
      file_name: str = ""
    ) -> None:
    raw = requests.get(
      f"{raw_path}/{file_type}/{file_name}",
     headers = {'User-Agent': ua.chrome}
    )
    text = str(raw.text)
    file = open(file_name, "x")
    file.write(text)
    file.close()
