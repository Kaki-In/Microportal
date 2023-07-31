import time as _time
from .requests import *

class Robot():
    def __init__(self):
        self._name = ""
        self._type = ""
        self._address = ""
        self._lastConnection = 0
        
        self._waitingRequests = RequestsList()

    def name(self):
        return self._name

    def setName(self, newName):
        self._name = newName

    def type(self):
        return self._type

    def setType(self, type):
        self._type = type
    
    def lastConnectionDate(self):
        return self._lastConnection
    
    def setLastConnectionDate(self, date):
        self._lastConnection = date
    
    def setLastConnectionDateNow(self):
        self._lastConnection = _time.monotonic()
    
    def ipAddress(self):
        return self._address
    
    def setIpAddress(self, address):
        self._address = address
    
    def requests(self):
        return self._waitingRequests
