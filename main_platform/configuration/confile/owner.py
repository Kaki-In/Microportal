from . import *

class OwnerConfigurationFile(ConfigurationFile):
    def __init__(self):
        super().__init__(address=('john.doe@gmail.com',), name=('doe',), surname=('john',))
    
    def getSenderMail(self):
        configuration = self.configuration()
        return configuration[ "address" ][ 0 ]
    
    def getSenderName(self):
        configuration = self.configuration()
        return configuration[ "name" ][ 0 ]
    
    def getSenderSurname(self):
        configuration = self.configuration()
        return configuration[ "surname" ][ 0 ]

        
        
