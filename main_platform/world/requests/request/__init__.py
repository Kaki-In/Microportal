import events as _events
import typing as _T
_jsonObject = _T.Union[str, int, bool, None, list, dict, float]
import time as _time

class Request():
    STATE_CREATING = 0
    STATE_WAITING = 1
    STATE_PROCESSING = 2
    STATE_PROCESSED = 3
    STATE_CANCELED = -1

    def __init__(self, user: str, id: int):
        self._user = user
        self._robot = None
        self._action = None
        self._args = {}
        self._state = self.STATE_CREATING
        self._id = id
        self._result = None
        self._creationTime = None
        self._sendTime = None
        self._processedTime = None
        self._canceledTime = None

        self._events = {
            "created": _events.EventHandler(),
            "processing": _events.EventHandler(),
            "processed": _events.EventHandler(),
            "canceled": _events.EventHandler()
        }
    
    def __repr__(self) -> str:
        state = self.state()
        a = "<Request state=" + str(state) + " user=" + repr(self.user())
        if state != self.STATE_CREATING:
            a += " robot={robot!r} action={action!r} args={args!r}".format(robot = self.robot(), action = self.action(), args = self.getArguments())
        a += ">"
        return a
    
    def id(self):
        return self._id

    def addEventListener(self, event: str, function: _T.Callable [[_T.Optional[_jsonObject]], _T.Any]) -> _T.NoReturn:
        self._events[ event ].connect(function)
    
    def state(self) -> int:
        return self._state

    def user(self) -> str:
        return self._user

    def action(self) -> str:
        return self._action

    def setAction(self, action) -> _T.NoReturn:
        if self._state != self.STATE_CREATING: 
            raise TypeError("request already created")
        self._action = action
    
    def robot(self) -> str:
        return self._robot
    
    def setRobot(self, robot: str) -> _T.NoReturn:
        if self._state != self.STATE_CREATING: 
            raise TypeError("request already created")
        self._robot = robot

    def getArguments(self) -> dict:
        return self._args.copy()
    
    def setArgument(self, key: str, value: _jsonObject) -> _T.NoReturn:
        if self._state != self.STATE_CREATING: 
            raise TypeError("request already created")
        self._args[ key ] = value
    
    def updateArguments(self, args: _T.Dict [str, _jsonObject]) -> _T.NoReturn:
        if self._state != self.STATE_CREATING: 
            raise TypeError("request already created")
        self._args.update(args)

    def getArgument(self, key: str) -> _jsonObject:
        return self._args[ key ]
        
    def removeArgument(self, key: str) -> _T.NoReturn:
        del self._args[ key ]
    
    def __getitem__(self, key: str) -> _jsonObject:
        return self.getArgument(key)
    
    def __setitem__(self, key: str, value: _jsonObject) -> _T.NoReturn:
        self.setArgument(key, value)
    
    def __delitem__(self, key: str):
        self.removeArgument(key)
        
    def cancel(self) -> _T.NoReturn:
        if self._state in (self.STATE_PROCESSING, self.STATE_PROCESSED):
            raise TypeError("request already sent")
        self._canceledTime = _time.monotonic()
        self._state = self.STATE_CANCELED

        self._events[ "canceled" ].emit()
    
    def markAsReady(self) -> _T.NoReturn:
        if self._state != self.STATE_CREATING:
            raise TypeError("request already created")
        if self._robot is None:
            raise ValueError("robot not set")
        if self._action is None:
            raise ValueError("action not set")
        self._creationTime = _time.monotonic()
        self._state = self.STATE_WAITING

        self._events[ "created" ].emit()
    
    def markAsProcessing(self) -> _T.NoReturn:
        if self._state != self.STATE_WAITING:
            raise TypeError("request not waiting")
        self._sendTime = _time.monotonic()
        self._state = self.STATE_PROCESSING

        self._events[ "processing" ].emit()

    def markAsProcessed(self, result: _jsonObject) -> _T.NoReturn:
        if self._state != self.STATE_PROCESSING:
            raise TypeError("request not processing")
        self._state = self.STATE_PROCESSED
        self._processedTime = _time.monotonic()
        self._result = result

        self._events[ "processed" ].emit(result)

    def result(self) -> _T.NoReturn:
        if self._state != self.STATE_PROCESSED:
            raise TypeError("request not processed yet")
        return self._result

    def creationTime(self) -> float:
        return self._creationTime

    def sendTime(self) -> float:
        return self._sendTime
    
    def processedTime(self) -> float:
        return self._processedTime
    
    def canceledTime(self) -> float:
        return self._canceledTime

    def toJson(self) -> dict:
        return {
            "state" : self._state if self._state != self.STATE_PROCESSING else self.STATE_CANCELED,
            "user": self._user,
            "robot": self._robot,
            "action": self._action,
            "args": self._args,
            "id": self._id,
            "result": self._result,
            "times": [self._creationTime, self._sendTime, self._processedTime, self._canceledTime]
        }
    
    def fromJson(json: dict) -> 'Request':
        request = Request(json[ "user" ], json[ "id" ])
        request._robot = json[ "robot" ]
        request._action = json[ "action" ]
        request._args = json[ "args" ]
        request._id = json[ "id" ]
        request._result = json[ "result" ]
        request._creationTime, request._sendTime, request._processedTime, request._canceledTime = json[ "times" ]
        return request
