from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)  # Hachage du mot de passe
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return self.__dict__

    def check_password(self, password):
        print(self.password)
        print(password)
        return check_password_hash(self.password, password)
