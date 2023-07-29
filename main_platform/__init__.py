from .server import *
from .world.shelve import *
from .configuration import *
import i18n_setup as _i18n

from .i18n import getMain_platformI18n

class Platform():
    def __init__(self, configuration=None):
        self._configuration = configuration or Configuration()

        self._shelve = WorldShelve(self._configuration.localDirectory + "/world.db")
        self._world = self._shelve.load()
        
        self._vpol = self._configuration.verboseConfiguration.getVerbosePolicy()

        self._server = Server()
        
        self._i18n = self._configuration.i18nConfiguration.getI18n()
        self._i18n.loadFrom(getMain_platformI18n())
        self._i18n.setVerbosePolicy(self._vpol)
        
    def configuration(self):
        return self._configuration

    def verbosePolicy(self):
        return self._vpol
    
    def i18n(self):
        return self._i18n
