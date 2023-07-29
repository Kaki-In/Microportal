from .confile.mail import *
from .confile.verbosePolicy import *
from .resources.main import *
import os as _os

class Configuration():
    def __init__(self):
        self.localDirectory = "~/.microportal"
        self.logDirectory = "/var/log/microportal"
        self.confDirectory = "/etc/microportal"
        
        self.mailConfiguration = MailConfigurationFile( self.readConfiguration("mail") )
        self.verboseConfiguration = VerbosePolicyConfigurationFile( self.readConfiguration("verbosePolicy"), self.logDirectory + "/output.log" )
        
        self.resources = MainResources(self.confDirectory + "/resources")

    def readConfiguration(self, name):
        path = self.confDirectory + "/" + name + ".conf"
        if _os.path.exists(path):
            a = open(path, "r")
            lines = a.readlines()
            a.close()

            configuration = {}
            for line in lines:
                line = line.replace("\t", " ")
                while line.startswith(" "):
                    line = line[ 1 : ]

                while line.endswith(" "):
                    line = line[ : -1 ]

                if not line or line.startswith("#"):
                    continue
                    
                while "  " in line:
                    line = line.replace("  ", " ")
                    
                arguments = line.split()
                parameter = arguments[ 0 ]
                args = arguments[ 1 : ]
                configuration[ parameter ] = args
        else:
            configuration = self.getDefaultConfiguration()
            a = open(self._path, "w")
            a.write("### DEFAULT CONFIGURATION FOR {name} ###\n\n".format(name))
            for parameter in configuration:
                a.write(parameter)
                for i in lines[parameter]:
                    a.write(" " + i)
                a.write("\n")
            a.close()
        return configuration
        
