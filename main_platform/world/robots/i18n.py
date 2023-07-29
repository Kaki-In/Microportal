
### FILE GENERATED BY A LOCAL_PROGRAM        ###
### PLEASE DON'T MODIFY THIS FILE, WHICH     ###
### WILL BE RE-GENERATED                     ###

import i18n_setup as _i18n
import os as _os

DIRNAME = _os.path.abspath(_os.path.dirname(__FILE__))

from .robot.i18n import getRobotI18n as _getRobotI18n

LANGUAGES = ['fr_FR', 'en_US']

def getRobotsI18n():
    i18n = _i18n.I18NTranslator()

    for i in LANGUAGES:
        parser = _i18n.I18NFileParser(DIRNAME + "/{}.i18n".format(i))
        i18n.addLanguage(parser.getLanguage())

    for subTranslator in [_getRobotI18n()]:
        i18n.loadFrom(subTranslator)

    return i18n

