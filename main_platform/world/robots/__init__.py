from .robot import *

class RobotsList():
    def __init__(self):
        self._robots = {}
        self._id = 0
    
    def getNewRobotId(self):
        self._id += 1
        return self._id
    
    def robots(self):
        return self._robots.copy()
    
    def addRobot(self, robot):
        self._robots[ self.getNewRobotId() ] = robot
    
    def removeRobot(self, id):
        del self._robots[ id ]
    
    def getRobot(self, id):
        return self._robots[ id ]
