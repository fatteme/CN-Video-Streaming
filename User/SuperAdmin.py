class SuperAdmin:
    _instance = None
    @staticmethod 
    def getInstance():
        if SuperAdmin._instance == None:
            SuperAdmin()
        return SuperAdmin._instance

    def __init__(self):
        if SuperAdmin._instance != None:
            raise Exception("You can not have more than one super admin!")
        else:
            SuperAdmin._instance = self
            self.username = "manager"
            self.password = "supreme_manager#2022"

#admin addmission, other proxy related duties

########################## test
sa = SuperAdmin.getInstance()
print(sa.username)
print(sa.password)