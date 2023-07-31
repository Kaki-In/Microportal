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
        html = html.format(STYLE=style, TITLE=title, CONTENT=content)
        
        message = _msg.Message()
        message[ "Subject" ] = subject
        message[ "From" ] = sender
        message[ "To" ] = self._address
        message.add_header('Content-Type', 'text/html')
        message.set_payload(html)
        
        platform.verbosePolicy().log(message.as_string(), infolevel = LEVEL_DEBUG)
        
        smtp = platform.configuration().mailConfiguration.getSMTP()
        try:
            smtp.sendmail(sender, self._address, message.as_bytes().decode(encoding='UTF-8'))
        except Exception as exc:
            platform.verbosePolicy().log(platform.i18n().translate("USER_EMAIL_SEND_FAILED", type=type(exc).__name__, error=str(exc)), infolevel = LEVEL_ERROR)
            result = False
        else:
            platform.verbosePolicy().log(platform.i18n().translate("USER_EMAIL_SEND_SUCCESS", infolevel = LEVEL_INFO))
            result = True
        smtp.quit()
        return result
    
        
