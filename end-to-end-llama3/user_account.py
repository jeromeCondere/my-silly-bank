import uuid

class User:
    def __init__(self, name, email):
        self.account_id = uuid.uuid4()  # Unique account ID for the user
        self.name = name  # Name of the user

    def __str__(self):
        return f"User(account_id={self.account_id}, name={self.name})"
