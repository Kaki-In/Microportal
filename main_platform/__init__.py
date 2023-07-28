from .server import *
from .world.shelve import *
from .configuration import *
import i18n_setup as _i18n

from .i18n import getPlatformI18n

class Platform():
    def __init__(self, configuration):
        self._shelve = WorldShelve(configuration.path())
        self._world = self._shelve.readWorld()
        self.configuration = configuration or Configuration()
        
        self._vpol = configuration.verboseConfiguration.getVerbosePolicy()
        
        self._server = Server()
        
        self._i18n = getPlatformI18n()
        self._i18n.setVerbosePolicy(self._vpol)

    def verbosePolicy(self):
        return self._vpol
