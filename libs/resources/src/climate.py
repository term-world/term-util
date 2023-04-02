import json
import requests

STATE = json.loads(
    requests.get(
        "https://cdn.githubraw.com/term-world/TNN/main/weather.json"
    ).text
)

class Climate:

    def __init__(self):
        for attribute in STATE:
            setattr(self, attribute, STATE[attribute])

    def __str__(self):
        return str(dir(self))
