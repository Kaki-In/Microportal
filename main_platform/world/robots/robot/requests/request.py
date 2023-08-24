import time as _tm

class Request():
    STATUS_WAITING = 0
    STATUS_CANCELED = 1
    STATUS_PROCESSING = 2
    STATUS_PROCESSED = 3
    
    def __init__(self, username, name, **args):
        self._user = username
        self._name = name
        self._args = args
        self._creation = _tm.monotonic()
        self._status = self.STATUS_WAITING
        self._result = None
    
    def __repr__(self):
        return "<{name} name={rname} status={status}>".format(name=type(self).__name__, rname=self._name, status=self._status)

    def user(self):
        return self._user
    
    def name(self):
        return self._name
    
    def getArguments(self):
        return self._args.copy()
        
    def creationDate(self):
        return self._creation
    
    def cancel(self):
        self._status = self.STATUS_CANCELED
    
    def status(self):
        return self._status
    
    def markAsProcessing(self):
        self._status = self.STATUS_PROCESSING
    
    def markAsProcessed(self, result):
        self._status = self.STATUS_PROCESSED
        self._result = result
    
    def result(self):
        return self._result

    def toJson(self):
        return {
                   'user': self._user,
                   'name': self._name,
                   'args': self._args,
                   'creation': self._creation,
                   'status': self._status,
                   'result': self._result
               }
    
    def fromJson(json):
        r = Request(json[ 'user' ], json[ 'name' ], **json[ 'args' ])
        r._creation = json[ 'creation' ]
        r._status = json[ 'status' ]
        r._result = json[ 'result' ]
        return r
