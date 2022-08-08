import cmd
from io import StringIO

from services.user_service import UserService
from consts import OUT_OF_NETWORK_ERROR

class ClientCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    prompt = '(youtube) '
    user_service = UserService()

    def has_logged_in(self):
        return self.user_service.user != None

    def do_help(self, arg: str) -> str:
        'help or ?'
        help_output = StringIO()
        super().__setattr__('stdout', help_output)
        super().do_help(arg)
        return help_output.getvalue(), False

    def do_login(self, arg):
        'login [type= admin | superadmin] [username] [password]'
        args = parse(arg)
        if len(args) < 3:
            return ClientCommandHandler.INVALID_ARGS, False
        elif args[0] == 'admin':
            return self.user_service.get_admin(username=args[1], password=args[2]), False
        elif args[0] == 'superadmin':
            return self.user_service.get_super_admin(username=args[1], password=args[2]), False
        else:
            return ClientCommandHandler.INVALID_ARGS, False

    def do_logout(self, arg):
        'logout'
        self.user_service.logout()
        return f'logout successfull.', False

    def do_signup(self, arg):
        'signup [username] [password]'
        args = parse(arg)
        if len(args) < 2:
            return ClientCommandHandler.INVALID_ARGS, False
        self.user_service.create_admin(args[0], args[1])
        return f'signup successfull. Super admin permission is needed.', False

    def do_exit(self, arg):
        'type q to exit'
        return '', False    

    def do_reply_ticket(self, arg):
        'reply [ticketid] [text]'
        if not self.has_logged_in():
            return OUT_OF_NETWORK_ERROR, False
        return self.user_service.user.username, True

    def do_ticket(self, arg):
        'ticket [text] [username]'
        if not self.has_logged_in():
            return OUT_OF_NETWORK_ERROR, False
        return self.user_service.user.username, True

    def do_set_ticket_state(self, arg):
        'set_ticket_state [ticketid] [state] [username]'
        if not self.has_logged_in():
            return OUT_OF_NETWORK_ERROR, False
        return self.user_service.user.username, True

    def do_open_tickets(self, arg):
        'open_tickets'
        if not self.has_logged_in():
            return OUT_OF_NETWORK_ERROR, False
        return self.user_service.user.username, True

<<<<<<< HEAD
    def do_permissions(self, arg):
        'permissions'
        if not self.has_logged_in():
            return OUT_OF_NETWORK_ERROR, False
        return self.user_service.user.username, True

    def do_approve(self, arg):
        'approve [username]'
=======
    def do_label(self, arg):
        'label [title] [text]'
>>>>>>> c7f6c24e9dcb5e4221b955da5b0948fb26b9baad
        if not self.has_logged_in():
            return OUT_OF_NETWORK_ERROR, False
        return self.user_service.user.username, True


def parse(arg):
    return arg.split()
