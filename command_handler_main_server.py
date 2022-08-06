import cmd
from io import StringIO

from services.user_service import UserService
from constraints import OUT_OF_NETWORK_ERROR

class ClientCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    prompt = '(youtube) '
    userService = UserService()

    def do_help(self, arg: str) -> str:
        'help or ?'
        help_output = StringIO()
        super().__setattr__('stdout', help_output)
        super().do_help(arg)
        return help_output.getvalue()

    def do_login(self, arg):
        'login [type= user | admin | superadmin] [username] [password]'
        args = parse(arg)
        if len(args) < 3:
            return ClientCommandHandler.INVALID_ARGS
        if args[0] == 'user':
            return ClientCommandHandler.userService.get_end_user(username=args[1], password=args[2])
        elif args[0] == 'admin':
            # return CommandHandler.userService.get_admin(username=args[1], password=args[2])
            return OUT_OF_NETWORK_ERROR
        elif args[0] == 'superadmin':
            # return CommandHandler.userService.get_super_admin(username=args[1], password=args[2])
            return OUT_OF_NETWORK_ERROR
        else:
            return ClientCommandHandler.INVALID_ARGS

    def do_logout(self, arg):
        'logout'
        self.userService.logout()
        return f'logout successfull.'
    
    def do_signup(self, arg):
        'signup [type= user | admin] [username] [password]'
        args = parse(arg)
        if len(args) < 3:
            return ClientCommandHandler.INVALID_ARGS
        if args[0] == 'user':
            ClientCommandHandler.userService.create_end_user(args[1], args[2])
            return f'signup successfull. Admin permission is needed.'
        elif args[0] == 'admin':
            # CommandHandler.userService.create_admin(args[1], args[2])
            # return f'signup successfull. Super admin permission is needed.'
            return OUT_OF_NETWORK_ERROR
        else:
            return ClientCommandHandler.INVALID_ARGS
    
    def do_exit(self, arg):
        'type q to exit'
        return ''

class ProxyCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    prompt = '(turtle) '
    userService = UserService()

    def do_help(self, arg: str) -> str:
        'help or ?'
        help_output = StringIO()
        super().__setattr__('stdout', help_output)
        super().do_help(arg)
        return help_output.getvalue()

    # def do_login(self, arg):
    #     'login [type=  admin | superadmin] [username] [password]'
    #     args = parse(arg)
    #     if len(args) < 3:
    #         return self.INVALID_ARGS
    #     elif args[0] == 'admin':
    #         return self.userService.get_admin(username=args[1], password=args[2])
    #     elif args[0] == 'superadmin':
    #         return self.userService.get_super_admin(username=args[1], password=args[2])
    #     else:
    #         return self.INVALID_ARGS

    # def do_logout(self, arg):
    #     'logout'
    #     self.userService.logout()
    #     return f'logout successfull.'
    
    # def do_signup(self, arg):
    #     'signup [username] [password]'
    #     args = parse(arg)
    #     if len(args) < 2:
    #         return self.INVALID_ARGS
    #     self.userService.create_admin(args[1], args[2])
    #     return f'signup successfull. Super admin permission is needed.'
    
    def do_permissions(self, arg):
        'permissions'
        return f'here is the signup permission list:\n {self.userService.get_unapproved_users()}'

    def do_approve(self, arg):
        'approve [username]'
        args = parse(arg)
        if len(args) < 1:
            return self.INVALID_ARGS
        return self.userService.approve(args[0])
    
    def do_exit(self, arg):
        'type q to exit'
        return ''

def parse(arg):
    return arg.split()
