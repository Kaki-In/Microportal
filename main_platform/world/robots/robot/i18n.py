
### FILE GENERATED BY A LOCAL_PROGRAM        ###
### PLEASE DON'T MODIFY THIS FILE, WHICH     ###
### WILL BE RE-GENERATED                     ###

import i18n_setup as _i18n
import os as _os
print(_os.path.abspath(_os.path.curdir))

LANGUAGES = ['fr_FR', 'en_US']

def getRobotI18n():
    i18n = _i18n.I18NTranslator()

    for i in LANGUAGES:
        parser = _i18n.I18NFileParser(_os.path.abspath("./{}.i18n".format(i)))
        i18n.addLanguage(parser.getLanguage())

    for subTranslator in []:
        i18n.loadFrom(subTranslator)

    return i18n

