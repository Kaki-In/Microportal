from . import *
import os as _os
import i18n_setup as _i18n

class I18nConfigurationFile(ConfigurationFile):
    def __init__(self):
        if "LANG" in _os.environ:
            lang = _os.environ[ "LANG" ].split('.')[ 0 ]
            if not "_" in lang: 
                lang = lang.lower() + "_" + lang.upper()
        else:
            lang = "en_US"
        super().__init__(language=tuple(lang.split("_")),default=("en","US"))
    
    def getI18n(self):
        configuration = self.configuration()
        language = configuration[ "language" ]
        default = configuration[ "default" ]
        i18n = _i18n.I18NTranslator(language[ 0 ] + "_" + language[ 1 ], default[ 0 ] + "_" + default[ 1 ])
        return i18n
    

        
        
