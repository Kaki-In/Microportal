from .confile.mail import *
from .confile.verbosePolicy import *
from .confile.i18n_translate import *
from .confile.owner import *
from .resources.main import *
import os as _os

class Configuration():
    def __init__(self):
        self.localDirectory = "../.microportal"
        self.logDirectory = "/var/log/microportal"
        self.confDirectory = "/etc/microportal"

        for i in (self.localDirectory, self.logDirectory, self.confDirectory):
            if not _os.path.exists(i):
                _os.makedirs(i)
        
        self.mailConfiguration = MailConfigurationFile()
        self.mailConfiguration.setConfiguration( self.readConfiguration("mail", self.mailConfiguration.configuration()) )

        self.verboseConfiguration = VerbosePolicyConfigurationFile( self.logDirectory + "/output.log" )
        self.verboseConfiguration.setConfiguration( self.readConfiguration("verbosePolicy", self.verboseConfiguration.configuration()) )
        
        self.i18nConfiguration = I18nConfigurationFile()
        self.i18nConfiguration.setConfiguration( self.readConfiguration( "i18n", self.i18nConfiguration.configuration()) )
        
        self.ownerConfiguration = OwnerConfigurationFile()
        self.ownerConfiguration.setConfiguration( self.readConfiguration("owner", self.ownerConfiguration.configuration()) )
        
        self.resources = Resources(self.confDirectory + "/resources")

    def readConfiguration(self, name, default):
        path = self.confDirectory + "/" + name + ".conf"
        if _os.path.exists(path):
            a = open(path, "r")
            lines = a.readlines()
            a.close()

            configuration = {}
            for line in lines:
                line = line.replace("\t", " ")[ : -1 ]
                while line.startswith(" "):
                    line = line[ 1 : ]

                while line.endswith(" "):
                    line = line[ : -1 ]

                if (not line) or line.startswith("#"):
                    continue
                    
                while "  " in line:
                    line = line.replace("  ", " ")
                    
                arguments = line.split(' ')
                parameter = arguments[ 0 ]
                args = arguments[ 1 : ]
                configuration[ parameter ] = args
        else:
            configuration = default
            a = open(path, "w")
            a.write("### DEFAULT CONFIGURATION FOR {name} ###\n\n".format(name=name))
            for parameter in configuration:
                a.write(parameter)
                for i in configuration[parameter]:
                    a.write(" " + i)
                a.write("\n")
            a.close()
        return configuration
        
