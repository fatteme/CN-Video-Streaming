class EndUser:
    def __init__(self, username, password, is_admin=False):
        EndUser.all_end_users.append(self)
        self.username = username 
        self.password = password
        self.strikes = 0
        self.is_admin = is_admin


# capabilities: signup, login, logout, upload, stream, like, dislike, comment