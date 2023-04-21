import json
import getpass
from datetime import datetime
import time

class User_Log:

    def now() -> float:
        """Returns a float is the time _right now_"""
        return datetime.now().timestamp()

    #Converts Epoch time to Date format
    local_time = time.ctime(now())


    # variable user _GETS_ the output of the 
    # getpass _module_'s getuser _method_.

    user = getpass.getuser()
    # create users list to add individual users

    users = []



    users.append({"user": user, "time": local_time})


    # save the list as a file


    with open("UserHistory.json", "a") as fh:
        json.dump(users, fh)



"""
def load_file(UserHistory: str = "") -> dict:
    # Loads a file by name
    with open(UserHistory) as fh:
        return json.load(fh)

def save_file(UserHistory: str = "", User: dict = {}) -> None:
    # Saves data to a file by name
    with open(UserHistory, "w") as fh:
        json.dump(User)
"""

"""
def main():

    User_history = {
        "User": user,
        
    }

    user_names = {}
    list = load_file("History/UserHistory.json")
    User = user_names
    for user in user_names:
        dummy = input("Enter text:")
        user = getpass.getuser()
        user_names.append(user)
        print(user)
"""
