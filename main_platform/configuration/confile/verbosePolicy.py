from . import *
import verbosePolicy as _verbosePolicy

class VerbosePolicyConfigurationFile(ConfigurationFile):
    def __init__(self, configuration, outputPath):
        super().__init__(configuration, trace="false", debug="false", info="false", warn="true", error="true", fatal="true")
        self._path = outputPath
    
    def getVerbosePolicy(self):
        configuration = self.configuration()
        
        verbosePolicy = _verbosePolicy.VerbosePolicy(configuration[ "trace" ] == "true", configuration[ "debug" ] == "true", configuration[ "info" ] == "true", configuration[ "warn" ] == "true", configuration[ "error" ] == "true", configuration[ "fatal" ] == "true", self._path)

        return verbosePolicy
    
    def matches(self, configuration):
        parentMatch = super().matches(configuration)
        if not parentMatch[ 0 ]:
            return parentMatch
        
        for parameter in ("trace", "debug", "info", "warn", "error", "fatal"):
            if not configuration[ parameter ] in ("true", "false"):
                return False, '"{}" must be a boolean'.format(parameter)
        
        return True, ""        


        
        
