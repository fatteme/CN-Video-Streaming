class EndUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.strike = 0


#capabilities: signup, login, logout, upload, stream, like, dislike, comment