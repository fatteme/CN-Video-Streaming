import traceback
from uuid import uuid4
import enum


class Ticket:
    def __init__(self, user, text):
        self.id = str(uuid4())
        self.user = user
        self.assignee = None
        self.text = text
        self.reply = None
        self.state = TicketState.NEW.value

    @staticmethod
    def from_tuple(t):
        try:
            print(t)
            ticket = Ticket(t[1], t[3])
            ticket.id = t[0]
            ticket.assignee = t[2]
            ticket.reply = t[4]
            ticket.state = t[5]
            return ticket
        except:
            traceback.print_exc()
            return None

class TicketState(enum.Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

    @staticmethod
    def is_valid(state):
        for s in TicketState:
            if s.value == state:
                return True
        return False