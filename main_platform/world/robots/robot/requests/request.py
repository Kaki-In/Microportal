import time as _tm

class Request():
    def __init__(self, user, name, **args):
        self._user = user
        self._name = name
        self._args = args
        self._creation = monotonic()
    
    def user(self):
        return self._user
    
    def name(self):
        return self._name
    
    def getArgument(self, argument):
        return self._args[ argument ]
        
    def creationDate(self):
        return self._creation
