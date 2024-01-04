from .robot import *
import events as _events
import typing as _T
_jsonObject = _T.Union[str, int, bool, None, list, dict, float]

class RobotsList():
    def __init__(self):
        self._robots: dict[str, Robot] = {}
        
        self._events: dict[str, _events.EventHandler] = {
            "robotAdded": _events.EventHandler(),
            "robotModified": _events.EventHandler(),
            "robotRemoved": _events.EventHandler(),
        }
    
    def __repr__(self) -> str:
        return "<{name} length={len}>".format(name=type(self).__name__, len=len(self))

    def __len__(self) -> int:
        return len(self._robots)

    def _plugOnRobotEvents(self, robot: Robot) -> None:
        onUserReload = lambda *args: self._events[ "robotModified" ].emit(robot)
        robot.addEventListener("nameChanged", onUserReload)
        robot.addEventListener("typeChanged", onUserReload)
        robot.addEventListener("lastConnectionChanged", onUserReload)
    
    def addRobot(self, macAddress: str) -> Robot:
        robot = Robot(macAddress)
        self._robots[ macAddress ] = robot
        self._plugOnRobotEvents(robot)
        
        self._events[ "robotAdded" ].emit(robot)
        return robot
    
    def removeRobot(self, macAddress: str) -> None:
        del self._robots[ macAddress ]
    
    def getRobot(self, macAddress: str) -> Robot:
        return self._robots[ macAddress ]
    
    def __iter__(self) -> iter:
        return iter(self._robots)

    def __len__(self)-> int:
        return len(self._robots)
    
    def __getitem__(self, macAddress: str) -> Robot:
        return self._robots[ macAddress ]
    
    def toJson(self) -> _jsonObject:
        r = {}
        for id in self._robots:
            r[ id ] = self._robots[ id ].toJson()
        return r
    
    def fromJson(json: _jsonObject) -> 'RobotsList':
        r = RobotsList()
        for id in json:
            robot = Robot.fromJson(json[ id ])
            r._robots[ id ] = robot
            r._plugOnRobotEvents(robot)
        return r

    def addEventListener(self, name: str, function: _T.Callable) -> None:
        self._events[ name ].connect(function)
