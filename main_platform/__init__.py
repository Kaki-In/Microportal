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

    def server(self):
        return self._server

    def world(self):
        return self._world

    def handle(self):
        try:
            self._server.run(self)
        except Exception as exc:
            self.logFatal("PLATFORM_HANDLE_ERROR", type=type(exc).__name__, error=str(exc))
        finally:
            self.save()
    
    def save(self):
        self.logInfo("PLATFORM_SAVING_WORLD")
        try:
            self._shelve.save(self._world)
        except Exception as exc:
            self.logFatal("PLATFORM_WORLD_ERROR", type=type(exc).__name__, error=str(exc))
        else:
            self.logInfo("PLATFORM_WORLD_SAVED")
    
    def logTrace(self, text, depth = 1, **args):
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_TRACE, depth = depth + 1)
    
    def logDebug(self, text, depth = 1, **args):
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_DEBUG, depth = depth + 1)
    
    def logInfo(self, text, depth = 1, **args):
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_INFO, depth = depth + 1)
    
    def logWarning(self, text, depth = 1, **args):
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_WARNING, depth = depth + 1)
    
    def logError(self, text, depth = 1, **args):
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_ERROR, depth = depth + 1)
    
    def logFatal(self, text, depth = 1, **args):
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_FATAL, depth = depth + 1)
