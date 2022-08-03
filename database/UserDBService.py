from matplotlib import use
from models.user.Admin import Admin
from models.user.EndUser import EndUser
from mysql import connector
from Utils import encrypt


class UserDBService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            # password=config["password"],
            database=config["database"]
            )
        self.table = "User"

    def create_user(self, user):
        query = f"INSERT INTO {self.table} (username, password, strikes, is_admin, is_approved) Values (%s, %s, %s, %s, %s)"
        if isinstance(user, Admin):
            values = (user.username, encrypt(user.password), 0, 1, user.is_approved)
        elif isinstance(user, EndUser):
            values = (user.username, encrypt(user.password), user.strikes, 0, user.is_approved)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record inserted.")

    def update_user(self, user):
        query = f"UPDATE {self.table} SET password = %s, strikes = %s, is_approved = %s WHERE username = %s"
        if isinstance(user, Admin):
            values = (encrypt(user.password), 0, user.is_approved, user.username)
        elif isinstance(user, EndUser):
            values = (encrypt(user.password), user.strikes, user.is_approved, user.username)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record(s) affected")

    def get_user(self, username):
        query = f"SELECT * from {self.table} WHERE username = %s"
        values = (username,)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        is_admin = result[3]
        if is_admin:
            return Admin(result[0], result[1], result[4])
        else:
            return EndUser(*result)