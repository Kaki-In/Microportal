from email import message as _msg
import random as _rd

class MailAddress():
    def __init__(self, address):
        self._address = address
        self._verified = False
        self._verifyData = None
    
    def startVerification(self, platform, name):
        verificationData = ''
        for _ in range(6):
            verificationData += _rd.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self._verifyData = verificationData
        
        message = """

<html>
    <head>
        <meta charset="utf-8">
        <style></style>
    </head>

    <body>
    </body>
</html>

"""
        
        self.send(platform, platform.i18n().translate("USER_EMAIL_SEND_PLEASE_VERIFY_YOUR_MAIL"), message)
    
    def setVerified(self):
        self._verified = True
    
    def address(self):
        return self._address

    def send(self, platform, subject, content):
        sender = platform.configuration().owner.getSenderMail()
        
        message = _msg.Message()
        message.set_content(content)
        message[ "Subject" ] = subject
        message[ "From" ] = sender
        message[ "To" ] = self._address
        
        smtp = platform.configuration().mailConfiguration.getSMTP()
        smtp.send_message(message)
        smtp.quit()
    
        
