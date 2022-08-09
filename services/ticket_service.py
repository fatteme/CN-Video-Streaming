from numpy import isin
from consts import DB_CONFIG
from database.ticket_db_service import TicketDBService
from models.video.ticket import Ticket, TicketState
from utils import encrypt


class TicketService:
    def __init__(self):
        self.ticket_db_service = TicketDBService(config=DB_CONFIG)

    def create_ticket(self, username, text ,assignee=None):
        ticket = Ticket(username, text)
        if assignee:
            ticket.assignee = assignee
        self.ticket_db_service.create_ticket(ticket)
        return f"Ticket {ticket.id} created successfully!"
    
    def reply_to_ticket(self, ticket_id, reply_text, username):
        ticket = self.ticket_db_service.get_ticket(ticket_id)
        if not ticket:
            return "Invalid ticket id!"
        if ticket.assignee and ticket.assignee != username:
            return "You can't reply to this ticket!"
        if ticket.state == TicketState.CLOSED.value:
            return "The ticket is already closed and can't be modified!"
        self.ticket_db_service.update_ticket(ticket_id, {
            "assignee": username,
            "reply": reply_text
        })
        return "Reply submitted succesfully!"
    
    def set_ticket_state(self, ticket_id, state, user=None):
        ticket = self.ticket_db_service.get_ticket(ticket_id)
        if not ticket:
            return "Invalid ticket id!"
        if user and user != ticket.user and user != "manager":
            return "You are not authorized to change tickets not initially created by you!"
        if not TicketState.is_valid(state):
            return "Not a valid state! Please Choose from one of the following options: (NEW|PENDING|RESOLVED|CLOSED)."
        if ticket.state == TicketState.CLOSED.value:
            return "The ticket is already closed and can't be modified!"
        self.ticket_db_service.update_ticket(ticket_id, {
            "state": state
        })
        return "Ticket state updated succesfully!"

    def get_all_open_tickets(self):
        result = "Ticket ID, User, Assignee, State, text, reply\n"
        for ticket in self.ticket_db_service.get_all_open_tickets():
            result += str(tuple([ticket.id, ticket.user, ticket.assignee, ticket.state, ticket.text, ticket.reply])) + "\n"
        return result
        
    def get_all_user_tickets(self, username):
        result = "Ticket ID, Assignee, State, text, reply\n"
        for ticket in self.ticket_db_service.get_all_user_tickets(username):
            result += str(tuple([ticket.id, ticket.assignee, ticket.state, ticket.text, ticket.reply])) + "\n"
        return result
