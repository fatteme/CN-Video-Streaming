from models.user.Admin import Admin
from models.user.EndUser import EndUser
from mysql import connector
from Utils import encrypt


class UserService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            # password=config["password"],
            database=config["database"]
            )
        self.table = "User"

    def create_user(self, user):
        query = f"INSERT INTO {self.table} (username, password, strikes, is_admin) Values (%s, %s, 0, %s)"
        if isinstance(user, Admin):
            values = (user.username, encrypt(user.password), 1)
        elif isinstance(user, EndUser):
            values = (user.username, encrypt(user.password), 0)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record inserted.")

    def update_user(self, user):
        query = f"UPDATE {self.table} SET password = %s, strikes = %s WHERE username = %s"
        if isinstance(user, Admin):
            values = (encrypt(user.password), 0, user.username)
        elif isinstance(user, EndUser):
            values = (encrypt(user.password), user.strikes, user.username)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record(s) affected")
