from . import *
import smtplib as _smtp

class MailConfigurationFile(ConfigurationFile):
    def __init__(self):
        super().__init__(host="smtp.google.com", port="465", ssl="true", username="johndoe@google.com", password="password")
    
    def getSMTP(self):
        configuration = self.configuration()

        if configuration[ "ssl" ] == "true":
            smtp_class = _smtp.SMTP_SSL
        else:
            smtp_class = _smtp.SMTP
        smtp = smtp_class(configuration[ "host" ], int(configuration[ "port"]) )
        smtp.login(configuration[ "username" ], configuration[ "password" ])

        return smtp

    def matches(self, configuration):
        parentMatch = super().matches(configuration)
        if not parentMatch[ 0 ]:
            return parentMatch
        
        if not configuration[ "ssl" ] in ("true", "false"):
            return False, '"ssl" must be a boolean'

        if not configuration[ "port" ].isdigit():
            return False, '"port" must be an integer'
    
        return True, ""
