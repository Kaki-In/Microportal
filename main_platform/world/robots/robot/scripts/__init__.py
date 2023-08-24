from .script import *

class ScriptsList():
    def __init__(self):
        self._scripts = []
    
    def createNewScript(self, username):
        s = Script(username)
        self._scripts.append(s)
        return s
    
    def __repr__(self):
        return "<{name} length={len}>".format(name=type(self).__name__, len=len(self))

    def __len__(self):
        return len(self._scripts)
    
    def __iter__(self):
        return iter(self._scripts)
    
    def toJson(self):
        return [i.toJson() for i in self]
    
    def fromJson(json):
        slist = ScriptsList()
        for s in json:
            slist._scripts.append(Script.fromJson(s))
        return slist
    
