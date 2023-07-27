from .server import *
from .world import *
import i18n_setup as _i18n

class Platform():
    def __init__(self, path="~/.microportal/data.db", vpol=None, i18n=None):
        self._shelve = WorldShelve(path)
        self._world = self._shelve.readWorld()
        
        self._vpol = vpol
        
        self._server = Server()
        
        self._i18n = i18n or _i18n.I18NTranslator()
    
    def verbosePolicy(self):
        return self._vpol
