from .server import *
from .world.shelve import *
from .configuration import *
import i18n_setup as _i18n
import verbosePolicy as _vpol

from .i18n import getMain_platformI18n

class Platform():
    def __init__(self, configuration: Configuration | None =None) -> "Platform":
        self._configuration: Configuration = configuration or Configuration()

        self._shelve = WorldShelve(self._configuration.localDirectory + "/world.db")
        self._world = self._shelve.load()
        
        self._vpol = self._configuration.verboseConfiguration.getVerbosePolicy()

        self._server = Server()
        
        self._i18n = self._configuration.i18nConfiguration.getI18n()
        self._i18n.loadFrom(getMain_platformI18n())
        self._i18n.setVerbosePolicy(self._vpol)
        
    def configuration(self) -> Configuration:
        return self._configuration

    def verbosePolicy(self) -> _vpol.VerbosePolicy:
        return self._vpol
    
    def i18n(self) -> _i18n.I18NTranslator:
        return self._i18n

    def server(self) -> Server:
        return self._server

    def world(self) -> World:
        return self._world

    def handle(self) -> None:
        try:
            self._server.run(self)
        except Exception as exc:
            self.logFatal("PLATFORM_HANDLE_ERROR", type=type(exc).__name__, error=str(exc))
        finally:
            self.save()
    
    def save(self) -> None:
        self.logInfo("PLATFORM_SAVING_WORLD")
        try:
            self._shelve.save(self._world)
        except Exception as exc:
            self.logFatal("PLATFORM_WORLD_ERROR", type=type(exc).__name__, error=str(exc))
        else:
            self.logInfo("PLATFORM_WORLD_SAVED")
    
    def logTrace(self, text: str, depth: int = 1, **args) -> None:
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_TRACE, depth = depth + 1)
    
    def logDebug(self, text: str, depth: int = 1, **args) -> None:
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_DEBUG, depth = depth + 1)
    
    def logInfo(self, text: str, depth: int = 1, **args) -> None:
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_INFO, depth = depth + 1)
    
    def logWarning(self, text: str, depth: int = 1, **args) -> None:
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_WARNING, depth = depth + 1)
    
    def logError(self, text: str, depth: int = 1, **args) -> None:
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_ERROR, depth = depth + 1)
    
    def logFatal(self, text: str, depth: int = 1, **args) -> None:
        self._vpol.log(self._i18n.translate(text, **args), infolevel=self._vpol.LEVEL_FATAL, depth = depth + 1)
