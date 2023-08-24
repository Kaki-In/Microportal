import time as _time
from .requests import *
from .scripts import *

class Robot():
    def __init__(self, id):
        self._name = ""
        self._type = ""
        self._id = id
        self._lastConnection = 0
        
        self._waitingRequests = RequestsList()
        
        self._scripts = ScriptsList()
    
    def __repr__(self):
        return "<{name} id={mac} name={rname} type={type}>".format(name=type(self).__name__, mac=self.id(), rname=self.name(), type=self.type())

    def name(self):
        return self._name

    def setName(self, newName):
        self._name = newName
    
    def id(self):
        return self._id
    
    def scripts(self):
        return self._scripts

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
    
    def requests(self):
        return self._waitingRequests
    
    def toJson(self):
        return {
                   'id': self._id,
                   'name': self._name,
                   'type': self._type,
                   'lastConn': self._lastConnection,
                   'waitingRequests': self._waitingRequests.toJson(),
                   'scripts': self._scripts.toJson()
               }

    def fromJson(json):
        robot = Robot(json[ 'id' ])
        robot._name = json[ 'name' ]
        robot._type = json[ 'type' ]
        robot._lastConnection = json[ 'lastConn' ]
        robot._waitingRequests = RequestsList.fromJson(json[ 'waitingRequests' ])
        robot._scripts = ScriptsList.fromJson(json[ 'scripts' ])
        return robot
