import time as _time
from .icon import *
from .mail import *
import hashlib as _hash
import events as _events
import typing as _T
_jsonObject = _T.Union[str, int, bool, None, list, dict, float]

class User():
    def __init__(self, name: str, password: str, mail: str) -> "User":
        self._name: str = name
        self._password: str = _hash.sha256(password.encode("utf-8")).hexdigest()
        self._lastConnection: int = 0
        self._icon: UserIcon = UserIcon.createNew()
        self._mail: MailAddress = MailAddress(mail, name)
        
        self._events: dict[ str, _events.EventHandler ] = {
            "nameChanged": _events.EventHandler(),
            "passwordChanged": _events.EventHandler(),
            "lastConnectionChanged": _events.EventHandler(),
            "iconChanged": _events.EventHandler(),
            "mailChanged": _events.EventHandler(),
        }
        
    def __repr__(self) -> str:
        return "<{name} name={username!r}>".format(name=type(self).__name__, username=self.name())
        
    def name(self) -> str:
        return self._name

    def setName(self, newName: str) -> None:
        self._name = newName
        self._events[ "nameChanged" ].emit(newName)

    def lastConnectionDate(self) -> int:
        return self._lastConnection
    
    def setLastConnectionDate(self, date: int) -> None:
        self._lastConnection = date
        self._events[ "lastConnectionChanged" ].emit(date)
    
    def setLastConnectionDateNow(self) -> None:
        self.setLastConnectionDate( int( _time.time() * 1000 ) )
    
    def icon(self) -> UserIcon:
        return self._icon

    def setIcon(self, icon: bytes) -> None:
        self._icon = UserIcon(icon)
        self._events[ "iconChanged" ].emit(self._icon)
    
    def mailAddress(self) -> str:
        return self._mail
    
    def setMailAddress(self, address: str) -> None:
        self._mail = MailAddress(address)
        self._events[ "mailChanged" ].emit(self._mail)
    
    def loadNewUser(name: str, mail: str) -> "User":
        user = User(name)
        user.setLastConnectionDateNow()
        user.setIcon(UserIcon.createNew())
        user.setMailAddress(mail)
        return user

    def passwordMatches(self, password: str) -> bool:
        return self._password == _hash.sha256(password.encode("utf-8")).hexdigest()
    
    def toJson(self):
        return {
                   'name': self._name,
                   'password': self._password,
                   'lastConnection': self._lastConnection,
                   'icon': self._icon.toJson(),
                   'mail': self._mail.toJson()
               }
    
    def fromJson(json: _jsonObject) -> "User":
        u = User(json[ 'name' ], "", None)
        u._password = json[ 'password' ]
        u._lastConnection = json[ 'lastConnection' ]
        u._icon = UserIcon.fromJson(json[ 'icon' ])
        u._mail = MailAddress.fromJson(json[ 'mail' ])
        return u

    def addEventListener(self, name: str, function: _T.Callable) -> None:
        self._events[ name ].connect(function)
