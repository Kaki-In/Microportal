from email import message as _msg
import random as _rd
from verbosePolicy import *

class MailAddress():
    def __init__(self, address, username):
        self._address = address
        self._user = username
        self._verified = False
        self._verifyData = None
    
    def createVerificationCode(self):
        verificationData = ''
        for _ in range(6):
            verificationData += _rd.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self._verifyData = verificationData
    
    def verificationCode(self):
        return self._verifyData
        
    def startVerification(self, platform):
        self.createVerificationCode()

        subject = platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_SUBJECT")
        title = platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_TITLE")
        
        platform.verbosePolicy().log(platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_CONTENT", code="TEST"), infolevel = LEVEL_DEBUG)
        content = platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_CONTENT", code=self.verificationCode())
        
        self.send(platform, subject, title, content)
        
        self._verified = False
    
    def setVerified(self):
        self._verified = True
    
    def address(self):
        return self._address

    def send(self, platform, subject, title, content):
        sender = platform.configuration().ownerConfiguration.getSenderMail()
        
        html = platform.configuration().resources.mail.getFile( "index.html" )
        style = platform.configuration().resources.mail.getFile( "style.css" )
        html = content.format(STYLE=style, TITLE=title, CONTENT=content)
        
        message = _msg.Message()
        message.set_content( html )
        message[ "Subject" ] = subject
        message[ "From" ] = sender
        message[ "To" ] = self._address
        
        smtp = platform.configuration().mailConfiguration.getSMTP()
        smtp.send_message(message)
        smtp.quit()
    
        
