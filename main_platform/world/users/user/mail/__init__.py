from email.mime.multipart import MIMEMultipart as _Multipart
from email.mime.text import MIMEText as _MText
import random as _rd

class MailAddress():
    def __init__(self, address, username):
        self._address = address
        self._user = username
        self._verified = False
        self._verifyData = None
    
    def __repr__(self):
        return "<{name} address={addr!r} user={user!r} verified={ver}>".format(name=type(self).__name__, addr=self._address, user=self._user, ver=self._verified)
    
    def createVerificationCode(self):
        verificationData = ''
        for _ in range(6):
            verificationData += _rd.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self._verifyData = verificationData

    def verificationCode(self):
        return self._verifyData
        
    def startVerification(self, platform):
        self.createVerificationCode()
        platform.logInfo("USER_EMAIL_NEW_VERIFICATION_CODE", username=self._user, code=self._verifyData)
    
        subject = platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_SUBJECT")
        title = platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_TITLE")
        
        content = platform.i18n().translate("USER_EMAIL_SEND_VERIFICATION_CONTENT", code=self.verificationCode())
        
        self.send(platform, subject, title, content)
        
        self._verified = False
    
    def submitVerificationCode(self, verificationCode):
        if verificationCode == self._verifyData:
            self._verified = True
        return self._verified
    
    def address(self):
        return self._address

    def isVerified(self):
        return self._verified

    def send(self, platform, subject, title, content):
        sender = platform.configuration().ownerConfiguration.getSenderMail()
        sendername = platform.configuration().ownerConfiguration.getSenderName()
        sendersurname = platform.configuration().ownerConfiguration.getSenderSurname()
        
        html = platform.configuration().resources.mail.getFile( "index.html" )
        style = platform.configuration().resources.mail.getFile( "style.css" )
        html = html.format(STYLE=style, TITLE=title, CONTENT=content)
        
        message = _Multipart()
        message[ "Subject" ] = subject
        message[ "From" ] = platform.i18n().translate("USER_EMAIL_MICROPORTAL_NAME", name=sendername, surname=sendersurname) + " <{}>".format(sender)
        message[ "To" ] = self._user + " <{}>".format(self._address)

        message.attach( _MText(html, 'html') )
        
        smtp = platform.configuration().mailConfiguration.getSMTP()
        try:
            smtp.sendmail(sender, self._address, message.as_bytes() )
        except Exception as exc:
            platform.logError("USER_EMAIL_SEND_FAILED", type=type(exc).__name__, error=str(exc))
            result = False
        else:
            platform.logInfo("USER_EMAIL_SEND_SUCCESS")
            result = True
        smtp.quit()
        return result
    
    def toJson(self):
        return {
                   'address': self._address,
                   'user': self._user,
                   'verified': self._verified,
                   'verifyData': self._verifyData
               }
    
    def fromJson(json):
        mail = MailAddress(json[ 'address' ], json[ 'user' ])
        mail._verified = json[ 'verified' ]
        mail._verifyData = json[ 'verifyData' ]
        return mail
    
        
