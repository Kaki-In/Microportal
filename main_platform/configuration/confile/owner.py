from . import *

class OwnerConfigurationFile(ConfigurationFile):
    def __init__(self):
        super().__init__(address=('YOUR_MAIL_ADDRESS',), name=('doe',), surname=('john',), password=("admin"))
    
    def getOwnerMail(self):
        configuration = self.configuration()
        return configuration[ "address" ][ 0 ]
    
    def getOwnerName(self):
        configuration = self.configuration()
        return configuration[ "name" ][ 0 ]
    
    def getOwnerSurname(self):
        configuration = self.configuration()
        return configuration[ "surname" ][ 0 ]

    def getOwnerPassword(self):
        configuration = self.configuration()
        return configuration[ "password" ][ 0 ]

        
        
