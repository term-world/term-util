import json
import os
import getpass
from datetime import datetime
import time

class UserLog:

    def log_user(wind = 0, solar = 0, coal = 0, oil = 0, nuclear = 0, natural_gas = 0):
        path = os.path.dirname(__file__)
        with open(f"{path}/log.json", "r") as fh:
            log = json.load(fh)

            name = getpass.getuser()
            now = datetime.now().timestamp()

            entry = {
                "user": name,
                "time": now,
                "wind": wind,
                "solar": solar,
                "coal": coal,
                "oil": oil,
                "nuclear": nuclear,
                "natural_gas": natural_gas
            }

            log.append(entry)
        
        with open(f"{path}/log.json", "w") as fh:
            json.dump(log, fh)