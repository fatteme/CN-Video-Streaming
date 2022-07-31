class ticket:
    def __init__(self, user, text):
        self.user = user
        self.assignee = None
        self.text = text
        self.reply = None
        self.state = "NEW"