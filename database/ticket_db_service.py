from unicodedata import name
from mysql import connector
from models.user.end_user import EndUser
from uuid import uuid4

from models.video.ticket import Ticket

class TicketDBService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            # password=config["password"],
            database=config["database"]
            )
        self.table = "ticket"

    def create_ticket(self, ticket: Ticket):
        query = f"INSERT INTO {self.table} (id, user, assignee, text) Values (%s, %s, %s, %s)"
        values = ticket.id, ticket.user, ticket.assignee, ticket.text

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record inserted.")

    def update_ticket(self, id, update_dict: dict):
        query = f"UPDATE {self.table} SET"
        for attr in update_dict:
            query += f" {attr} = %s,"
        query = query[:-1] + " WHERE id = %s"

        values = tuple(list(update_dict.values()) + [id])

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record(s) affected")

    def get_ticket(self, id):
        query = f"SELECT * from {self.table} WHERE id = %s"
        values = (id,)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        return Ticket.from_tuple(result)

    def get_all_open_tickets(self):
        query = f"SELECT * from {self.table} WHERE NOT state = 'CLOSED'"
        values = tuple()

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        for result in results:
            yield Ticket.from_tuple(result)

    def get_all_user_tickets(self, username):
        query = f"SELECT * from {self.table} WHERE user = %s"
        values = (username, )

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        for result in results:
            yield Ticket.from_tuple(result)
