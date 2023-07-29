from .server import *
from .world.shelve import *
from .configuration import *
import i18n_setup as _i18n

from .i18n import getMain_platformI18n

class Platform():
    def __init__(self, configuration=None):
        self._configuration = configuration or Configuration()

        self._shelve = WorldShelve(self._configuration.localDirectory + "/world.db")
        self._world = self._shelve.readWorld()
        
        self._server = Server()
        
        self._i18n = getMain_platformI18n()
        self._i18n.setVerbosePolicy(self._configuration.verboseConfiguration.getVerbosePolicy())

    def configuration(self):
        return self._configuration

    def verbosePolicy(self):
        return self._vpol
