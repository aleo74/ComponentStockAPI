from datetime import datetime


class Stocks:
    def __init__(self, name, description, qty, imgLink, tags):
        self.name = name
        self.description = description
        self.qty = qty
        self.image_link = imgLink
        self.tags = tags
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return self.__dict__
