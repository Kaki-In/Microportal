
### FILE GENERATED BY A LOCAL_PROGRAM        ###
### PLEASE DON'T MODIFY THIS FILE, WHICH     ###
### WILL BE RE-GENERATED                     ###

import i18n_setup as _i18n
import os as _os

from .configuration.i18n import getConfigurationI18n as _getConfigurationI18n
from .server.i18n import getServerI18n as _getServerI18n
from .world.i18n import getWorldI18n as _getWorldI18n

LANGUAGES = ['fr_FR', 'en_US']

def getMain_platformI18n():
    i18n = _i18n.I18NTranslator()

    for i in LANGUAGES:
        parser = _i18n.I18NFileParser(_os.path.abspath("./{}.i18n".format(i)))
        i18n.addLanguage(parser.getLanguage())

    for subTranslator in [_getConfigurationI18n(), _getServerI18n(), _getWorldI18n()]:
        i18n.loadFrom(subTranslator)

    return i18n

