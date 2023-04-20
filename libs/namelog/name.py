import getpass



def load_file(UserHistory: str = "") -> dict:
    """ Loads a file by name """
    with open(UserHistory) as fh:
        return json.load(fh)

def save_file(UserHistory: str = "", User: dict = {}) -> None:
    """ Saves data to a file by name """
    with open(UserHistory, "w") as fh:
        json.dump(User)


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
