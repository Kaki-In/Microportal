import os as _os

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

    def getI18NLanguage(self):
        fileContent, language = self.read()
        i18nLanguage = I18NLanguage(language)
        i18nLanguage.updateTranslations(fileContent)
        return i18nLanguage

class I18NLanguage ():
    def __init__(self, languageName):
        self._name = languageName
        self._translations = {}
    
    def languageName(self):
        return self._name
    
    def updateTranslations(self, translations):
        self._translations.update(translations)
    
    def addTranslation(self, keyWord, translation):
        self._translations[ keyWord ] = translation
    
    def translate(self, keyWord, **args):
        if keyWord in self._translations:
            return self._translations[ keyWord ].format(**args)
        else:
            raise ValueError("keyword not found")

class I18NTranslator():
    def __init__(self, lang="en"):
        self._translations = []
        self._language = lang
    