import time as _time
from .icon import *
from .mail import *

class User():
    def __init__(self, name):
        self._name = name
        self._lastConnection = 0
        self._icon = None
        self._mail = None
        
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
        self._icon = icon
    
    def mailAddress(self, mail):
        self._mail = mail
    
    def setMailAddress(self, address):
        self._address = address
    
    def loadNewUser(name, mail):
        user = User(name)
        user.setLastConnectionDateNow()
        user.setIcon(UserIcon.createNew())
        user.setMail()
        return user
