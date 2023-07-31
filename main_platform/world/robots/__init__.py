from .robot import *

class RobotsList():
    def __init__(self):
        self._robots = {}
        self._id = 0
    
    def getNewRobotId(self):
        self._id += 1
        return self._id
    
    def addRobot(self, robot):
        self._robots[ self.getNewRobotId() ] = robot
    
    def removeRobot(self, id):
        del self._robots[ id ]
    
    def getRobot(self, id):
        return self._robots[ id ]
    
    def __iter__(self):
        return iter(self._robots)
    
    def toJson(self):
        r = {}
        a = {'id':self._id, 'robots':r}
        for id in a:
            r[ id ] = self._robots[ id ].toJson()
        return a
    
    def fromJson(json):
        r = RobotsList()
        r._id = json[ 'id' ]
        for id in json[ 'robots' ]:
            r._robots[ id ] = Robot.fromJson(json[ 'robots' ][ id ])
        return r
