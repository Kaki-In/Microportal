from .users import *
from .robots import *
import os as _os

class World():
    def __init__(self):
        self._users = UsersList()
        self._robots = RobotsList()
                
    def usersList(self):
        return self._users
    
    def robotsList(self):
        return self._robots
    
    def toJson(self):
        return {
                   'users': self._users.toJson(),
                   'robots': self._robots.toJson()
               }
    
    def fromJson(json):
        w = World()
        w._users = UsersList.fromJson(json[ 'users' ])
        w._robots = UsersList.fromJson(json[ 'robots' ])
        return w


            
