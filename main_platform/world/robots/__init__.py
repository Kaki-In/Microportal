from .robot import *

class RobotsList():
    def __init__(self):
        self._robots = {}
    
    def __repr__(self):
        return "<{name} length={len}>".format(name=type(self).__name__, len=len(self))

    def addRobot(self, macAddress):
        robot = Robot(macAddress)
        self._robots[ macAddress ] = robot
        return robot
    
    def removeRobot(self, macAddress):
        del self._robots[ macAddress ]
    
    def getRobot(self, macAddress):
        return self._robots[ macAddress ]
    
    def __iter__(self):
        return iter(self._robots)

    def __len__(self):
        return len(self._robots)
    
    def __getitem__(self, macAddress):
        return self._robots[ macAddress ]
    
    def toJson(self):
        r = {}
        for id in self._robots:
            r[ id ] = self._robots[ id ].toJson()
        return r
    
    def fromJson(json):
        r = RobotsList()
        for id in json:
            r._robots[ id ] = Robot.fromJson(json[ id ])
        return r
