from .user import *
import events as _events
import typing as _T

_jsonObject = _T.Union[str, int, bool, None, list, dict, float]

class UsersList():
    def __init__(self) -> "UsersList":
        self._users: dict[str, User] = {}

        self._events: dict[str, _events.EventHandler] = {
            "userAdded": _events.EventHandler(),
            "userModified": _events.EventHandler(),
            "userRemoved": _events.EventHandler(),
        }
    
    def addUser(self, username: str, password: str, mail: str) -> None:
        if username in self._users:
            raise ValueError("user already exists")
        else:
            user = User(username, password, mail)
            self._users[ username ] = user

            onUserReload = lambda *args: self._events[ "userModified" ].emit(user)
            user.addEventListener("nameChanged", onUserReload)
            user.addEventListener("lastConnectionChanged", onUserReload)
            user.addEventListener("iconChanged", onUserReload)
            user.addEventListener("mailChanged", onUserReload)
            user.addEventListener("passwordChanged", onUserReload)

            self._events[ "userAdded" ].emit( user )
            return user
    
    def __repr__(self) -> str:
        return "<{name} length={len}>".format(name=type(self).__name__, len=len(self))

    def __len__(self) -> int:
        return len(self._users)
    
    def addUserFromJson(self, json: _jsonObject) -> None:
        username = json[ 'name' ]
        if username in self._users:
            raise ValueError("user already exists")
        else:
            user = User.fromJson(json)
            self._users[ username ] = user

            onUserReload = lambda *args: self._events[ "userModified" ].emit(user)
            user.addEventListener("nameChanged", onUserReload)
            user.addEventListener("lastConnectionChanged", onUserReload)
            user.addEventListener("iconChanged", onUserReload)
            user.addEventListener("mailChanged", onUserReload)
            user.addEventListener("passwordChanged", onUserReload)

            return user
    
    def removeUser(self, name: str) -> None:
        user = self._users[ name ]
        del self._users[ name ]
        self._events[ "userRemoved" ].emit(user)
    
    def renameUser(self, name: str, newName: str) -> None:
        user = self._users[ name ]
        self.removeUser(name)
        user.setName(newName)
        self.addUser(newName, user)
    
    def getUser(self, name: str) -> User:
        return self._users[ name ]
    
    def __getitem__(self, name: str) -> User:
        return self._users[ name ]
    
    def __iter__(self):
        return iter(self._users)
    
    def toJson(self) -> _jsonObject:
        a = {}
        for name in self:
            a[ name ] = self.getUser(name).toJson()
        return a
    
    def fromJson(json: _jsonObject) -> "UsersList":
        l = UsersList()
        for name in json:
            l.addUserFromJson(json[ name ])
        return l

    def addEventListener(self, name: str, function: _T.Callable) -> None:
        self._events[ name ].connect(function)
