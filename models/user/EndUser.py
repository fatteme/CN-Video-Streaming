class EndUser:
    def __init__(self, username, password, strikes = 0, is_admin = False, is_approved = False):
        self.username = username 
        self.password = password
        self.strikes = strikes
        self.is_admin = is_admin
        self.is_approved = is_approved


# capabilities: signup, login, logout, upload, stream, like, dislike, comment