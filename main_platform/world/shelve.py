from . import *
import json as _json

class WorldShelve():
    def __init__(self, path):
        self._path = path
    
    def save(self, world):
        a = open(self._path, "w")
        a.write(_json.dump(world.toJson()))
        a.close()
    
    def load(self):
        a = open(self._path, "r")
        data = a.read()
        a.close()
        
        return World.fromJson(_json.dump(data))

