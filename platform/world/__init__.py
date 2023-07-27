from .users import *
from .robots import *
import os as _os

class World():
    def __init__(self):
        self._users = UserList()
        self._robots = RobotsList()
        
    def userList(self):
        return self._users
    
    def robotsList(self):
        return self._robots

class WorldShelve():
    def __init__(self, path):
        if not (_os.path.exists(path) and _os.path.isfile(path)):
            
