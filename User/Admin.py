class Admin:
    all_admins = []
    def __init__(self, username, password):
        Admin.all_admins.append(self)
        self.username = username
        self.password = password

#signup with superadmin permisson, login, logout, strike, video removal, strike removal, stream video