import time as _tm

class Request():
    def __init__(self, username, name, **args):
        self._user = username
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
    
    def toJson(self):
        return {
                   'user': self._user,
                   'name': self._name,
                   'args': self._args,
                   'creation': self._creation
               }
    
    def fromJson(json):
        r = Request(json[ 'user' ], json[ 'name' ], **json[ 'args' ])
        r._creation = json[ 'creation' ]
        return r
