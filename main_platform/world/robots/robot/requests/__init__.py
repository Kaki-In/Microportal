from .request import *

class RequestsList():
    def __init__(self):
        self._requests = []
    
    def __repr__(self):
        return "<{name} length={len}>".format(name=type(self).__name__, len=len(self))
    
    def createRequest(self, user, requestName, **args):
        req = Request(user, requestName, **args)
        self._requests.append(req)
        return req
    
    def createRequestFromScript(self, user, script):
        req = Request(user, script.name(), script.arguments())
        self._requests.append(req)
        return req
    
    def index(self, request):
        return self._requests.index(request)
        
    def __getitem__(self, index):
        return self._requests[ index ]
    
    def __iter__(self):
        return iter(self._requests)
    
    def __len__(self):
        return len(self._requests)
    
    def toJson(self):
        return [i.toJson() for i in self]
    
    def fromJson(json):
        l = RequestsList()
        rlist = []
        for r in json:
            rlist.append(Request.fromJson(r))
        l._requests = rlist
        return l
