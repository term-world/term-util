class Record:

    def __init__(self, data: dict = {}):
        for field in data:
            setattr(self, field, data[field])
