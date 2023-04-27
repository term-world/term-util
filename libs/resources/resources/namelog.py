import json
import os
import getpass
from datetime import datetime
import time

class UserLog:

    # Get the Power added
    def log_user(wind = 0, solar = 0, coal = 0, oil = 0, nuclear = 0, natural_gas = 0) -> list:
        with open("../../term-util-power-planters/libs/resources/resources/log.json", "r") as fh:
            log = json.load(fh)

            name = getpass.getuser()
            now = time.ctime(datetime.now().timestamp())

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
        
        with open("../../term-util-power-planters/libs/resources/resources/log.json", "w") as fh:
            json.dump(entry, fh)
   
        #energy.append({"user": name, "time": now, "wind": wind, "solar": solar, "coal": coal, "oil": oil, "nuclear": nuclear, "natural_gas": natural_gas})
        #path = os.path.dirname(resources.__file__)