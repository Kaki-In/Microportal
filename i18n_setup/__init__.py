import os as _os
import verbosePolicy as _vpol

class I18NFileParser():
    def __init__(self, path):
        if not (_os.path.exists(path) and _os.path.isfile(path)):
            raise FileNotFoundError("no such file")
        self._path = path
    
    def getraw(self):
        a = open(self._path, "r")
        data = a.read()
        a.close()
        result = data.split("\n")
        i = 0
        while i < len(result):
            if not result [i] or result [i] [0] == "#":
                result.pop(i)
                continue
            if result [i] [0] in (" ", "\t"):
                result [i] = result [i] [ 1 : ]
            elif result [i] [-1] in (" ", "\t"):
                result [i] = result [i] [ : -1 ]
            else:
                i +=1
        return result
    
    def read(self):
        data = self.getraw()
        
        result = {}
        language = None
        
        for i in range(len(data)):
            line = data[i]

            if not ":" in line:
                raise SyntaxError("missing ':' in file on line " + str(line))
            
            middleIndex = line.index(":")
            
            key, value = line[ : middleIndex ], line[ middleIndex + 1 : ]
            
            while key.endswith(" "):
                key = key[ : -1 ]
            
            while value.startswith(" "):
                value = value[ 1 : ]
            
            if key.startswith("~") and key.endswith("~"):
                key = key.replace(" ", "")[ 1 : -1 ].lower()
                if key == "language":
                    language = value
                ...
            else:
                result[ key ] = value
        
        if language is None:
            raise ValueError("no language specified")
        
        return result, language
    
    def getLanguage():
        fileContent, language = self.read()
        i18nResult = I18NLanguage(language)
        i18nResult.updateTranslations(fileContent)
        return i18nResult

class I18NLanguage ():
    def __init__(self, languageName):
        self._name = languageName
        self._translations = {}
    
    def languageName(self):
        return self._name
    
    def updateTranslations(self, translations):
        self._translations.update(translations)
    
    def loadFile(self, i18nFile):
        fileContent, language = i18nFile.read()
        self.updateTranslations(fileContent)
    
    def addTranslation(self, keyWord, translation):
        self._translations[ keyWord ] = translation
    
    def translate(self, keyWord, **args):
        if keyWord in self._translations:
            return self._translations[ keyWord ].format(**args)
        else:
            raise KeyError("keyword not found : " + repr(keyWord))
    
    def __iter__(self):
        return iter(self._translations)

class I18NTranslator():
    def __init__(self, lang="en", default="en", verbosePolicy=None):
        self._languages = {}
        self._language = lang
        self._defaultLanguage = default
        
        self._verbosePolicy = verbosePolicy or VerbosePolicy()
    
    def getLanguage(self, language):
        if language in self._languages:
            return self._languages[ language ]
        else:
            raise KeyError("no such language : " + repr(language))
    
    def translate(self, keyWord, **args):
        language = self.getLanguage(self._language)
        defaultLanguage = self.getLanguage(self._defaultLanguage)
        try:
            try:
                result = language.translate(keyWord)
            except KeyError:
                result = defaultLanguage.translate(keyWord)
                self._verbosePolicy.log("translation not found for", repr(keyWord), "in language", repr(self._language), infolevel = _verboaePolicy.LEVEL_WARNING)
        except KeyError:
            self._verbosePolicy.log("translation not found for", repr(keyWord), infolevel = _verboaePolicy.LEVEL_FATAL)
            raise
        else:
            return result


    