from .server import *
from .world.shelve import *
import i18n_setup as _i18n

from .i18n import getPlatformI18n

class Platform():
    def __init__(self, path="~/.microportal/data.db", vpol=None, i18n=None):
        self._shelve = WorldShelve(path)
        self._world = self._shelve.readWorld()
        
        self._vpol = vpol
        
        self._server = Server()
        
        self._i18n = i18n or getPlatformI18n()
    
    def verbosePolicy(self):
        return self._vpol
