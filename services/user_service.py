from numpy import isin
from consts import DB_CONFIG
from database.user_db_service import UserDBService
from models.user.admin import Admin
from models.user.end_user import EndUser
from models.user.super_user import SuperAdmin
from utils import encrypt


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
    
    def logout(self):
        self.user = None

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
    
    def set_proxy_user(self, username):
        if username == 'manager':
            user = SuperAdmin.getInstance()
        else:
            user = self.userDBService.get_user(username=username)
        self.user = user


    def get_unapproved_users(self):
        if not self.user:
            return 'You need to login first, try help login for more info.'
        if isinstance(self.user, EndUser):
            return 'End users do not have permission for this.'
        elif isinstance(self.user, Admin):
            if not self.user.is_approved:
                return 'Admins need to be approved.'
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

    def approve(self, username):
        user = self.userDBService.get_user(username=username)
        if isinstance(self.user, EndUser):
            return 'End users do not have permission for this.'
        elif isinstance(self.user, Admin):
            if not self.user.is_approved:
                return 'Admins need to be approved.'
            else:
                if isinstance(user, Admin):
                    return 'Admin cannot grant permission for admin users.'
                user.is_approved = 1
                self.userDBService.update_user(user=user)
        elif isinstance(self.user, SuperAdmin):
            user.is_approved = 1
            self.userDBService.update_user(user=user)
        return f'permission granted to {username}.'

    def is_approved_admin(self, username):
        user = self.userDBService.get_user(username=username)
        if not user:
            return False, False
        return True, user.is_approved

    def unstrike_user(self, username):
        print('unstriking ', username)
        user = self.userDBService.get_user(username=username)
        if isinstance(user, EndUser):
            user.strikes = 0
            self.userDBService.update_user(user=user)
            return 'user unstriked!'
        else:
            return 'This act cannot be done on a/an (super)admin' 