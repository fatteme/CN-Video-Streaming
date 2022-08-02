from matplotlib import use
from Constants import DB_CONFIG
from database.UserDBService import UserDBService
from models.user.Admin import Admin
from models.user.EndUser import EndUser
from mysql import connector
from Utils import encrypt


class UserService:
    def __init__(self):
        self.userDBService = UserDBService(config=DB_CONFIG)

    def create_end_user(self, username, password):
        user = EndUser(username=username, password=password)
        self.userDBService.create_user(user=user)
    
    def create_admin(self, username, password):
        user = Admin(username=username, password=password)
        self.userDBService.create_user(user=user)