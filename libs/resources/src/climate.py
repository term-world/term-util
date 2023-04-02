import json
import requests

from datetime import datetime

STATE = json.loads(
    requests.get(
        "https://cdn.githubraw.com/term-world/TNN/main/weather.json"
    ).text
)

class Climate:

    sun = [800, 801]

    def __init__(self):
        self.time = datetime.now().timestamp()
        self.windy = self.__is_windy()
        self.sunny = self.__is_sunny() and not self.__is_night()

    def __is_sunny(self) -> bool:
        for condition in STATE["weather"]:
            if condition["id"] in self.sun:
                return True
        return False

    def __is_night(self) -> bool:
        sunrise = STATE["sys"]["sunrise"]
        sunset = STATE["sys"]["sunset"]
        if sunrise < self.time < sunset:
            return False
        return True

    def __is_windy(self) -> bool:
        if STATE["wind"]["speed"] > 5:
            return True
        return False
