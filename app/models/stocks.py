from datetime import datetime


class Stocks:
    def __init__(self, name, description, qty):
        self.name = name
        self.description = description
        self.qty = qty
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return self.__dict__
