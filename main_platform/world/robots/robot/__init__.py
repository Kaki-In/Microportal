import time as _time

class Robot():
    def __init__(self, id):
        self._name = ""
        self._type = ""
        self._id = id
        self._lastConnection = 0
    
    def __repr__(self):
        return "<{name} id={mac} name={rname} type={type}>".format(name=type(self).__name__, mac=self.id(), rname=self.name(), type=self.type())

    def name(self):
        return self._name

    def setName(self, newName):
        self._name = newName
    
    def id(self):
        return self._id
    
    def type(self):
        return self._type

    def setType(self, type):
        self._type = type
    
    def lastConnectionDate(self):
        return self._lastConnection
    
    def setLastConnectionDate(self, date):
        self._lastConnection = date
    
    def setLastConnectionDateNow(self):
        self._lastConnection = _time.time() * 1000
    
    def toJson(self):
        return {
                   'id': self._id,
                   'name': self._name,
                   'type': self._type,
                   'lastConn': self._lastConnection,
               }

    def fromJson(json):
        robot = Robot(json[ 'id' ])
        robot._name = json[ 'name' ]
        robot._type = json[ 'type' ]
        robot._lastConnection = json[ 'lastConn' ]
        return robot
