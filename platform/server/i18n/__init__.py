import i18n_setup as _i18n

LANGUAGES = ["en", "fr"]

def getServerI18n():
    i18n = _i18n.I18NTranslator()
    for i in LANGUAGES:
        parser = _i18n.I18NFileParser("./{}.i18n".format(i))
        i18n.addLanguage(parser.getLanguage())
    return i18n

