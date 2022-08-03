class Admin:
    def __init__(self, username, password, is_approved=0):
        self.username = username
        self.password = password
        self.is_approved = 0

#signup with superadmin permisson, login, logout, strike, video removal, strike removal, stream video