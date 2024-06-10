from datetime import datetime


class Tags:
    def __init__(self, name, description, color):
        self.name = name
        self.description = description
        self.color = color
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return self.__dict__
