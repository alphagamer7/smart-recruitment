
class Profile(object):
    def __init__(self):
        self.username = None
        self.count= None
        self.user_profile=None

    def getusername(self):
        return self.username

    def setusername(self, value):
        self.username = value


    def getcount(self):
        return self.count

    def setcount(self, value):
        self.count = value


    def getuser_profile(self):
        return self.user_profile

    def setuser_profile(self, value):
        self.user_profile = value


