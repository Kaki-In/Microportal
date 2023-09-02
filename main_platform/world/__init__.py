from .users import *
from .robots import *
from .requests import *
from .scripts import *
import os as _os

class World():
    def __init__(self):
        self._users = UsersList()
        self._robots = RobotsList()
        self._requests = RequestsList()
        self._scripts = ScriptsList()
    
    def usersList(self):
        return self._users
    
    def robotsList(self):
        return self._robots

    def requests(self):
        return self._requests

    def scripts(self):
        return self._scripts
    
    def toJson(self):
        return {
                   'users': self._users.toJson(),
                   'robots': self._robots.toJson(),
                   'requests': self._requests.toJson(),
                   'scripts': self._scripts.toJson()
               }
    
    def fromJson(json):
        w = World()
        w._users = UsersList.fromJson(json[ 'users' ])
        w._robots = RobotsList.fromJson(json[ 'robots' ])
        w._requests = RequestsList.fromJson(json[ 'requests' ])
        w._scripts = ScriptsList.fromJson(json[ 'scripts' ])
        return w


            
