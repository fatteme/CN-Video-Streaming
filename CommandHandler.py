import cmd
from io import StringIO
class CommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    prompt = '(youtube) '

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
            return CommandHandler.INVALID_ARGS
        if args[0] == 'user':
            pass
        elif args[0] == 'admin':
            pass
        elif args[0] == 'superadmin':
            pass
        else:
            return CommandHandler.INVALID_ARGS
        return f'login successfull.'

    def do_logout(self, arg):
        'logout'
        return f'logout successfull.'
    
    def do_signup(self, arg):
        'signup [type= user | admin] [username] [password]'
        args = parse(arg)
        if len(args) < 3:
            return CommandHandler.INVALID_ARGS
        if args[0] == 'user':
            pass
            return f'signup successfull. Admin permission is needed.'
        elif args[0] == 'admin':
            pass
            return f'signup successfull. Super admin permission is needed.'
        else:
            return CommandHandler.INVALID_ARGS
    
    def do_permissions(self, arg):
        'permissions'
        return f'here is the signup permission list:\n'

    def do_permission(self, arg):
        'permission [username]'
        args = parse(arg)
        if len(args) < 1:
            return CommandHandler.INVALID_ARGS
        return f'permission granted.'
    
    def do_exit(self, arg):
        'type q to exit'
        return ''

def parse(arg):
    return arg.split()
