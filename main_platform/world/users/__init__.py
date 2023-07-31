from .user import *

class UsersList():
    def __init__(self):
        self._users = {}
    
    def addUser(self, user):
        name = user.name()
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
    
    def getUser(self, name):
        return self._users[ name ]
    
    def __iter__(self):
        return iter(self._users)
    
    def toJson(self):
        a = {}
        for name in self:
            a[ name ] = self.getUser(name).toJson()
        return a
    
    def fromJson(json):
        l = UsersList()
        for name in json:
            user = User.fromJson(json[ name ])
            l.addUser(user)
        return l
