import os as _os
from .exception import *

class ConfigurationFile():
    def __init__(self, **defaultConfiguration):
        self._configuration = defaultConfiguration
        
    def setConfiguration(self, configuration):
        match = self.matches(configuration)
        if not match[ 0 ]:
            raise ConfigurationError(match[ 1 ])
        self._configuration = configuration

    def matches(self, configuration):
        for parameter in configuration:
            if not parameter in self._configuration:
                return False, "unknown parameter " + repr(parameter)

        for parameter in self._configuration:
            if not parameter in configuration:
                return False, "missing parameter " + repr(parameter)
        
        for parameter in configuration:
            if len( configuration ) < len( self._configuration ):
                return False, "too less arguments for parameter " + repr(parameter)
            if len( configuration ) > len( self._configuration ):
                return False, "too much arguments for parameter " + repr(parameter)
        
        return True, ""

    def configuration(self):
        return self._configuration
        
    

