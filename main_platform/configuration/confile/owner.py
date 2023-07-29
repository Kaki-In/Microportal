from . import *

class OwnerConfigurationFile(ConfigurationFile):
    def __init__(self):
        super().__init__(address="", name="", surname="")
    
    def getSenderMail(self):
        configuration = self.configuration()
        return configuration[ "address" ]
    
    def getSenderName(self):
        configuration = self.configuration()
        return configuration[ "name" ]
    
    def getSenderSurname(self):
        configuration = self.configuration()
        return configuration[ "surname" ]

        
        
