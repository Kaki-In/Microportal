from .user import *

class UsersList():
    def __init__(self):
        self._users = {}
    
    def users(self):
        return self._users.copy()
    
    def addUser(self, name, user):
        if name in self._users:
            raise KeyError("user already exists")
        else:
            self._users[ name ] = user
    
    def removeUser(self, name):
        del self._users[ name ]
    
    def renameUser(self, name, newName):
        user = self._users[ name ]
        self.removeUser(name)
        user.setName(newName)
        self.addUser(newName, user)
    
    def getUser(name):
        return self._users[ name ]
