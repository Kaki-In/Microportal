class MailAddress():
    def __init__(self, address):
        self._address = address
        self._verified = False
        self._verifyData = None
    
    def setVerified(self):
        self._verified = True
    
    def address(self):
        return self._address

    def send(self, object, )
