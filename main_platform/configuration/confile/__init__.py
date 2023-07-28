import os as _os

class ConfigurationFile():
    def __init__(self, actualConfiguration, **defaultConfiguration):
        self._defaultConfiguration = defaultConfiguration
        if self.configurationIsValid(actualConfiguration):
            self._actualConfiguration = {}
        else:
            raise TypeError("unvalid configuration")
    
    def configurationIsValid(self, configuration):
        return self.matches(configuration) == ([], [])
    
    def getDefaultConfiguration(self):
        return self._defaultConfiguration

    def matches(self, configuration):
        for parameter in configuration:
            if not parameter in self._defaultConfiguration:
                return False, "unknown parameter " + repr(parameter)

        for parameter in self._defaultConfiguration:
            if not parameter in configuration:
                return False, "missing parameter " + repr(parameter)
        
        return True, ""

    def configuration(self):
        return self._actualConfiguration
        
    

