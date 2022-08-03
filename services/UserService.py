from numpy import isin
from Constants import DB_CONFIG
from database.UserDBService import UserDBService
from models.user.Admin import Admin
from models.user.EndUser import EndUser
from models.user.SuperAdmin import SuperAdmin
from Utils import encrypt


class UserService:
    def __init__(self):
        self.userDBService = UserDBService(config=DB_CONFIG)
        self.user = None

    def create_end_user(self, username, password):
        user = EndUser(username=username, password=password)
        self.userDBService.create_user(user=user)
    
    def create_admin(self, username, password):
        user = Admin(username=username, password=password)
        self.userDBService.create_user(user=user)
    
    def get_end_user(self, username, password):
        user = self.userDBService.get_user(username=username)
        if user.is_admin:
            return 'username does not belong to an end user.'
        if not user.is_approved:
            return 'this account needs admin approval to proceed.'
        if encrypt(password) != user.password:
            return 'invalid password.'
        self.user = user
        return f'user {user.username} logged in successfully.'
        
    def get_admin(self, username, password):
        user = self.userDBService.get_user(username=username)
        if not user.is_approved:
            return 'this account needs super admin approval to proceed.'
        if encrypt(password) != user.password:
            return 'invalid password.'
        self.user = user
        return f'user {user.username} logged in successfully.'

    def get_super_admin(self, username, password):
        sa = SuperAdmin.getInstance()
        if sa.username == username and sa.password == password:
            self.user = sa
            return 'super admin logged in successfully.'
        else:
            return 'username or password is incorrect'

    def get_unapproved_users(self):
        if not self.user:
            return 'You need to login first, try help login for more info.'
        if isinstance(self.user, EndUser):
            return 'End users do not hhave permission for this.'
        elif isinstance(self.user, Admin):
            if not self.user.is_approved:
                return 'Admin needs to be approved'
            else:
                return self.get_unapproved_end_users()
        elif isinstance(self.user, SuperAdmin):
            return self.get_unapproved_admins()


    def get_unapproved_end_users(self):
        users = self.userDBService.get_unapproved_users()
        return '\n'.join(list(map(lambda a : a.username, users)))
    
    def get_unapproved_admins(self):
        users = self.userDBService.get_unapproved_users(is_admin=1)
        return '\n'.join(list(map(lambda a : a.username, users)))