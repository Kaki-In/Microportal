from . import *
import verbosePolicy as _verbosePolicy

class VerbosePolicyConfigurationFile(ConfigurationFile):
    def __init__(self, outputPath):
        super().__init__(display=("warning", "error", "fatal"))
        self._path = outputPath
        self._verbosePolicy = self.loadVerbosePolicy()
    
    def loadVerbosePolicy(self):
        configuration = self.configuration()
        
        l = ("info", "trace", "debug", "warning", "error", "fatal")
        
        d = {}
        for i in l:
            d[ i ] = i in configuration[ "display" ]
            
        verbosePolicy = _verbosePolicy.VerbosePolicy(output = open(self._path, "a"), **d)

        return verbosePolicy
   
    def getVerbosePolicy(self):
        return self._verbosePolicy
     
    def matches(self, configuration):
        parentMatch = super().matches(configuration)
        if not parentMatch[ 0 ]:
            return parentMatch
        
        for i in configuration[ "display" ]:
            if not i in ("info", "trace", "debug", "warning", "error", "fatal"):
                return False, "unknown verbose " + repr(i)
        
        return True, ""        
    
    def setConfiguration(self, configuration):
        super().setConfiguration(configuration)
        self._verbosePolicy = self.loadVerbosePolicy()


        
        
