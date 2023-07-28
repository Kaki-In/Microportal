from . import *

class OwnerConfigurationFile(ConfigurationFile):
    def __init__(self, configuration):
        super().__init__(configuration, address="", name="", surname="")
    
    def getSenderMail(self):
        configuration = self.configuration()
        return configuration[ "address" ]
    
        
        
