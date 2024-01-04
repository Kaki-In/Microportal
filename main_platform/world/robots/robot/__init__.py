import time as _time
import events as _events
import typing as _T
_jsonObject = _T.Union[str, int, bool, None, list, dict, float]

class Robot():
    def __init__(self, id: str):
        self._name: str = ""
        self._type: str = ""
        self._id: str = id
        self._lastConnection: int = 0
        
        self._events: dict[ str, _events.EventHandler ] = {
            "nameChanged": _events.EventHandler(),
            "typeChanged": _events.EventHandler(),
            "lastConnectionChanged": _events.EventHandler()
        }
    
    def __repr__(self) -> str:
        return "<{name} id={mac} name={rname} type={type}>".format(name=type(self).__name__, mac=self.id(), rname=self.name(), type=self.type())

    def name(self) -> str:
        return self._name

    def setName(self, newName : str) -> None:
        self._name = newName
        self._events[ "nameChanged" ].emit(newName)
    
    def id(self) -> str:
        return self._id
    
    def type(self) -> str:
        return self._type

    def setType(self, type) -> None:
        self._type = type
        self._events[ "typeChanged" ].emit(type)
    
    def lastConnectionDate(self) -> int:
        return self._lastConnection
    
    def setLastConnectionDate(self, date: int)  -> None:
        self._lastConnection = date
        self._events[ "lastConnectionChanged" ].emit(date)
    
    def setLastConnectionDateNow(self) -> None:
        self.setLastConnectionDate(int(_time.time() * 1000))
    
    def toJson(self) -> _jsonObject:
        return {
                   'id': self._id,
                   'name': self._name,
                   'type': self._type,
                   'lastConn': self._lastConnection,
               }

    def fromJson(json: _jsonObject) -> "Robot":
        robot = Robot(json[ 'id' ])
        robot._name = json[ 'name' ]
        robot._type = json[ 'type' ]
        robot._lastConnection = json[ 'lastConn' ]
        return robot

    def addEventListener(self, name: str, function: _T.Callable) -> None:
        self._events[ name ].connect(function)
