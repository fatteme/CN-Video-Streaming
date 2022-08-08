import cmd
from io import StringIO
from unittest import result
from services.ticket_service import TicketService
from socket import socket
from services.video_service import VideoService
from video_handler import ServerVideo, ClientVideo

from services.user_service import UserService
from consts import OUT_OF_NETWORK_ERROR, SUPERUSER

class ClientCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    NOT_LOGGED_IN = f'You are not logged in!'
    prompt = '(youtube) '

    user_service = UserService()
    ticket_service = TicketService()
    video_service = VideoService()

    video_server = ServerVideo()
    video_client = ClientVideo()

    def do_help(self, arg: str) -> str:
        'help or ?'
        help_output = StringIO()
        super().__setattr__('stdout', help_output)
        super().do_help(arg)
        return help_output.getvalue()

    def do_login(self, arg):
        'login [username] [password]'
        args = parse(arg)
        if len(args) < 2:
            return ClientCommandHandler.INVALID_ARGS
        return ClientCommandHandler.user_service.get_end_user(username=args[0], password=args[1])

    def do_whoami(self, arg):
        'whoami'
        user = self.user_service.user
        return user.username if user else 'No one is logged in'


    def do_logout(self, arg):
        'logout'
        self.user_service.logout()
        return f'logout successfull.'
    
    def do_signup(self, arg):
        'signup [username] [password]'
        args = parse(arg)
        if len(args) < 2:
            return ClientCommandHandler.INVALID_ARGS
        ClientCommandHandler.user_service.create_end_user(args[0], args[1])
        return f'signup successfull. Admin permission is needed.'

    def do_ticket(self, arg):
        'ticket [text]'
        if not self.user_service.user:
            return ClientCommandHandler.NOT_LOGGED_IN
        args = parse(arg)
        result = self.ticket_service.create_ticket(args[0], self.user_service.user.username)
        return result

    def do_set_ticket_state(self, arg):
        'set_ticket_state [ticketid] [state]'
        if not self.user_service.user:
            return ClientCommandHandler.NOT_LOGGED_IN
        args = parse(arg)
        result = self.ticket_service.set_ticket_state(args[0], args[1], self.user_service.user.username)
        return result

    def do_my_tickets(self, arg):
        'my_tickets'
        if not self.user_service.user:
            return ClientCommandHandler.NOT_LOGGED_IN
        args = parse(arg)
        result = self.ticket_service.get_all_user_tickets(self.user_service.user.username)
        return result
    
    def do_upload(self, arg):
        'upload [name]'
        # 'upload [name] [ip] [video_port] embedded in client code
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) != 3:
            return ClientCommandHandler.INVALID_ARGS
        ip, video_port = args[1], int(args[2])
        audio_port = video_port + 1
        video_socket = socket()
        video_socket.connect((ip, video_port))
        audio_socket = socket()
        audio_socket.connect((ip, audio_port))
        self.video_server.receive(name=args[0], username=user.username, video_socket=video_socket, audio_socket=audio_socket)
    
    def do_like(self, arg):
        'like [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.like(args[0])
    
    def do_dislike(self, arg):
        'dislike [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.dislike(args[0])

    def do_video_info(self, arg):
        'video_info [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.get_video(args[0])        

    def do_exit(self, arg):
        'type q to exit'
        return ''

class ProxyCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    prompt = '(turtle) '
    user_service = UserService()
    ticket_service = TicketService()

    def do_help(self, arg: str) -> str:
        'help or ?'
        help_output = StringIO()
        super().__setattr__('stdout', help_output)
        super().do_help(arg)
        return help_output.getvalue()
    
    def do_permissions(self, arg):
        'permissions'
        return f'here is the signup permission list:\n {self.user_service.get_unapproved_users()}'

    def do_approve(self, arg):
        'approve [username]'
        args = parse(arg)
        if len(args) < 1:
            return self.INVALID_ARGS
        return self.user_service.approve(args[0])

    def do_ticket(self, arg):
        'ticket [text] [username]'
        valid, approved = self.user_service.is_approved_admin(arg[1])
        if not valid:
            return "Username invalid!"
        if not approved:
            return "You are not approved by the super user!"
        result = self.ticket_service.create_ticket(arg[0], arg[1], SUPERUSER)
        return result

    def do_reply_ticket(self, arg):
        'reply_ticket [ticketid] [text] [username]'
        valid, approved = self.user_service.is_approved_admin(arg[1])
        if not valid:
            return "Username invalid!"
        if not approved:
            return "You are not approved by the super user!"
        result = self.ticket_service.reply_to_ticket(arg[0], " ".join(arg[1:-1], arg[-1]))
        return result

    def do_set_ticket_state(self, arg):
        'set_ticket_state [ticketid] [state] [username]'
        valid, approved = self.user_service.is_approved_admin(arg[1])
        if not valid:
            return "Username invalid!"
        if not approved:
            return "You are not approved by the super user!"
        result = self.ticket_service.set_ticket_state(arg[0], arg[1])
        return result

    def do_open_tickets(self, arg):
        'open_tickets'
        valid, approved = self.user_service.is_approved_admin(arg[1])
        if not valid:
            return "Username invalid!"
        if not approved:
            return "You are not approved by the super user!"
        result = self.ticket_service.get_all_open_tickets()
        return result

    def do_exit(self, arg):
        'type q to exit'
        return ''

    def do_label(self, arg):
        'label [title] [text] user'
        valid, approved = self.user_service.is_approved_admin(arg[1])
        if not valid:
            return "Username invalid!"
        if not approved:
            return "You are not approved by the super user!"


def parse(arg):
    return arg.split()
