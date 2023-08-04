from .user import *

class UsersList():
    def __init__(self):
        self._users = {}
    
    def addUser(self, username, password, mail):
        if username in self._users:
            raise KeyError("user already exists")
        else:
            user = User(username, password, mail)
            self._users[ username ] = user
            return user
    
    def __repr__(self):
        return "<{name} length={len}>".format(name=type(self).__name__, len=len(self))
    
    def addUserFromJson(self, json):
        username = json[ 'name' ]
        if username in self._users:
            raise KeyError("user already exists")
        else:
            user = User.fromJson(json)
            self._users[ username ] = user
            return user
    
    def removeUser(self, name):
        del self._users[ name ]
    
    def renameUser(self, name, newName):
        user = self._users[ name ]
        self.removeUser(name)
        user.setName(newName)
        self.addUser(newName, user)
    
    def getUser(self, name):
        return self._users[ name ]
    
    def __getitem__(self, name):
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
            l.addUserFromJson(json[ name ])
        return l
