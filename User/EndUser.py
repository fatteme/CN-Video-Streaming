class EndUser:
    all_end_users = []
    def __init__(self, username, password):
        EndUser.all_end_users.append(self)
        self.username = username 
        self.password = password
        self.strike = 0


#capabilities: signup, login, logout, upload, stream, like, dislike, comment