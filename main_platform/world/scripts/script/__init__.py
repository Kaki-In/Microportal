import typing as _T
import time as _time
_jsonObject = _T.Union[str, int, bool, None, list, dict, float]

class Script():
    def __init__(self, user: str, id: int):
        self._user = user
        self._robot = None
        self._action = None
        self._args = {}
        self._published = False
        self._id = id
        self._creation = _time.monotonic()
        self._modified = _time.monotonic()
    
    def id(self) -> int:
        return self._id
    
    def user(self) -> str:
        return self._user
    
    def published(self) -> bool:
        return self._published

    def robot(self) -> str:
        return self._robot
    
    def setRobot(self, robot: str) -> _T.NoReturn:
        self._modified = _time.monotonic()
        self._robot = robot
    
    def action(self) -> str:
        return self._action

    def setAction(self, action: str) -> _T.NoReturn:
        self._modified = _time.monotonic()
        self._action = action
    
    def getArguments(self) -> dict:
        return self._args.copy()
    
    def setArgument(self, key: str, value: _jsonObject) -> _T.NoReturn:
        self._modified = _time.monotonic()
        self._args[ key ] = value
    
    def getArgument(self, key: str) -> _jsonObject:
        return self._args[ key ]

    def removeArgument(self, key: str) -> _T.NoReturn:
        self._modified = _time.monotonic()
        del self._args[ key ]
    
    def __setitem__(self, key: str, value: _jsonObject) -> _T.NoReturn:
        self.setArgument(key, value)
    
    def __getitem__(self, key: str) -> _jsonObject:
        return self.getArgument(key)

    def __delitem__(self, key: str) -> _T.NoReturn:
        self.removeArgument(key)
    
    def creationTime(self) -> float:
        return self._creation

    def modificationTime(self) -> float:
        return self._modified
        
    def toJson(self) -> dict:
        return {
            "id": self._id,
            "user": self._user,
            "robot": self._robot,
            "action": self._action,
            "args": self._args,
            "published": self._published,
            "creation": self._creation,
            "modification": self._modified
        }

    def fromJSON(json: dict) -> 'Script':
        script = Script(json[ "user" ], json[ "id" ])
        script._robot = json[ "robot" ]
        script._action = json[ "action" ]
        script._args = json[ "args" ]
        script._published = json[ "published" ]
        script._creation = json[ "creation" ]
        script._modified = json[ "modification" ]


