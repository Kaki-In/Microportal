from . import *
import smtplib as _smtp

class MailConfigurationFile(ConfigurationFile):
    def __init__(self):
        super().__init__(host=("smtp.google.com",), port=("587",), ssl=("true",), username=("YOUR_MAIL_USERNAME",), password=("password",))
    
    def getSMTP(self):
        configuration = self.configuration()

        if configuration[ "ssl" ][ 0 ] == "true":
            smtp_class = _smtp.SMTP_SSL
        else:
            smtp_class = _smtp.SMTP
        smtp = smtp_class(configuration[ "host" ][ 0 ], int(configuration[ "port"][ 0 ]) )
        smtp.login(configuration[ "username" ][ 0 ], configuration[ "password" ][ 0 ])

        return smtp

    def matches(self, configuration):
        parentMatch = super().matches(configuration)
        if not parentMatch[ 0 ]:
            return parentMatch
        
        if not configuration[ "ssl" ][ 0 ] in ("true", "false"):
            return False, '"ssl" must be a boolean'

        if not configuration[ "port" ][ 0 ].isdigit():
            return False, '"port" must be an integer'
    
        return True, ""
