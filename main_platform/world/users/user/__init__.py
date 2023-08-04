import time as _time
from .icon import *
from .mail import *
import hashlib as _hash

class User():
    def __init__(self, name, password, mail):
        self._name = name
        self._password = _hash.sha256(password.encode("utf-8")).hexdigest()
        self._lastConnection = 0
        self._icon = UserIcon.createNew()
        self._mail = MailAddress(mail, name)
        
    def name(self):
        return self._name

    def setName(self, newName):
        self._name = newName

    def lastConnectionDate(self):
        return self._lastConnection
    
    def setLastConnectionDate(self, date):
        self._lastConnection = date
    
    def setLastConnectionDateNow(self):
        self._lastConnection = _time.monotonic()
    
    def icon(self):
        return self._icon

    def setIcon(self, icon):
        self._icon = UserIcon(icon)
    
    def mailAddress(self):
        return self._mail
    
    def setMailAddress(self, address):
        self._mail = address
    
    def loadNewUser(name, mail):
        user = User(name)
        user.setLastConnectionDateNow()
        user.setIcon(UserIcon.createNew())
        user.setMailAddress(mail)
        return user

    def passwordMatches(self, password):
        return self._password == _hash.sha256(password.encode("utf-8")).hexdigest()
    
    def toJson(self):
        return {
                   'name': self._name,
                   'password': self._password,
                   'lastConnection': self._lastConnection,
                   'icon': self._icon.toJson(),
                   'mail': self._mail.toJson()
               }
    
    def fromJson(json):
        j = json.copy()
        if 'icon' in j:
            del j[ 'icon' ]
        print(j)
        u = User(json[ 'name' ], "", None)
        u._password = json[ 'password' ]
        u._lastConnection = json[ 'lastConnection' ]
        u._icon = UserIcon.fromJson(json[ 'icon' ])
        u._mail = MailAddress.fromJson(json[ 'mail' ])
        print("user",u.name(),"created")
        return u
