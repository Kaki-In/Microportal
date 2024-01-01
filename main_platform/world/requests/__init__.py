import events as _events
from .request import *
import typing as _T

class RequestsList():
    def __init__(self):
        self._requests = []
        self._givingIds = 0
        
        self._events = {
            "create": _events.EventHandler(),
            "requestReady": _events.EventHandler(),
            "requestProcessing": _events.EventHandler(),
            "requestProcessed": _events.EventHandler(),
            "requestCanceled": _events.EventHandler(),
            "delete": _events.EventHandler()
        }
    
    def addEventListener(self, event: str, function: _T.Callable [[Request], _T.Any]) -> None:
        self._events[ event ].connect(function)
        
    def getNewId(self) -> int:
        self._givingIds += 1
        return self._givingIds
        
    def create(self, user: str) -> Request:
        request = Request(user, self.getNewId())
        self._requests.append(request)

        request.addEventListener("created", lambda: self._events[ "requestReady" ].emit(request))
        request.addEventListener("processing", lambda: self._events[ "requestProcessing" ].emit(request))
        request.addEventListener("processed", lambda result: self._events[ "requestProcessed" ].emit(request))
        request.addEventListener("canceled", lambda: self._events[ "requestCanceled" ].emit(request))

        self._events[ "create" ].emit(request)
        return request

    def delete(self, request: Request) -> None:
        if request.state() != request.STATE_PROCESSED:
            request.cancel()

        self._requests.remove(request)
        self._events[ "delete" ].emit(request)

    def getRequestsByRobot(self, robotName: str) -> _T.Tuple [Request]:
        results = []
        for request in self._requests:
            if request.robot() == robotName:
                results.append(request)
        return tuple(results)

    def getRequestsByUser(self, userName: str) -> _T.Tuple [Request]:
        results = []
        for request in self._requests:
            if request.user() == userName:
                results.append(request)
        return tuple(results)

    def requests(self) -> _T.Tuple [Request] :
        return tuple(self._requests)
    
    def getRequestById(self, id: int) -> Request:
        for request in self._requests:
            if request.id() == id:
                return request
    
    def __len__(self) -> int:
        return len(self._requests)
    
    def __iter__(self):
        return iter(self._requests)
    
    def toJson(self) -> dict:
        requests = []
        for request in self._requests:
            requests.append(request.toJson())
        return {
            "requests" : requests,
            "id": self._givingIds
        }
    
    def fromJson(json: dict) -> 'RequestsList':
        rlist = RequestsList()
        rlist._givingIds = json[ "id" ]
        rlist._requests = []
        for request in json[ "requests" ]:
            rlist._requests.append(Request.fromJson(request))
        return rlist
