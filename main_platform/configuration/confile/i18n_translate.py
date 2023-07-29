from . import *
import os
import i18n_setup as _i18n

class I18nConfigurationFile(ConfigurationFile):
    def __init__(self, outputPath):
        if "LANG" in _os.environ:
            lang = os.environ[ "LANG" ].split('.')[ 0 ]
        else:
            lang = "en_US"
        super().__init__(language=tuple(lang.split("_")),default=("en","US"))
        self._path = outputPath
    
    def getI18n(self):
        configuration = self.configuration()
        language = configuration[ "language" ]
        default = configuration[ "default" ]
        i18n = _i18n.I18nTranslator(language[ 0 ] + "_" + language[ 1 ], default[ 0 ] + "_" + default[ 1 ])
        return i18n
    

        
        
