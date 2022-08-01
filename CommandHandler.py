import cmd

class CommandHandler(cmd.Cmd):
    prompt = '(youtube) '

    def do_login(self, arg):
        return 'login'