from .request import *

class RequestsList():
    def __init__(self):
        self._requests = []
    
    def createRequest(self, user, name, **args):
        req = Request(user, name, **args)
        self._requests.append(request)
        return req
        
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
