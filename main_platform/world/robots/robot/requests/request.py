import time as _tm

class Request():
    STATUS_WAITING = 0
    STATUS_CANCELED = 1
    STATUS_PROCESSED = 2
    def __init__(self, username, name, **args):
        self._user = username
        self._name = name
        self._args = args
        self._creation = monotonic()
        self._status = self.STATUS_WAITING

    def user(self):
        return self._user
    
    def name(self):
        return self._name
    
    def getArguments(self, argument):
        return self._args.copy()
        
    def creationDate(self):
        return self._creation
    
    def cancel(self):
        self._status = self.STATUS_CANCELED
    
    def status(self):
        return self._status
    
    def markAsProcessed(self):
        self._status = self.STATUS_PROCESSED

    def toJson(self):
        return {
                   'user': self._user,
                   'name': self._name,
                   'args': self._args,
                   'creation': self._creation,
                   'status': self._status
               }
    
    def fromJson(json):
        r = Request(json[ 'user' ], json[ 'name' ], **json[ 'args' ])
        r._creation = json[ 'creation' ]
        r._status = json[ 'status' ]
        return r
