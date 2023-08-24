from . import *
import os as _os
import json as _json

class WorldShelve():
    def __init__(self, path):
        self._path = path
    
    def save(self, world):
        try:
            a = open(self._path, "w")
            a.write(_json.dumps(world.toJson()))
            a.close()
        except:
            _os.remove(self._path)
            raise
    
    def load(self):
        if not _os.path.exists(self._path):
            return World()
        a = open(self._path, "r")
        data = a.read()
        a.close()
        
        return World.fromJson(_json.loads(data))

