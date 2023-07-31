from .request import *

class RequestsList():
    def __init__(self):
        self._requests = []
    
    def addRequest(self, request):
        self._requests.append(request)
    
    def cancelRequest(self, request):
        self._requests.remove(request)
    
    def __iter__(self):
        return iter(self._requests)
    
    def __len__(self):
        return len(self._requests)
