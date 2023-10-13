from .script import *
import typing as _T

class ScriptsList():
    def __init__(self):
        self._scripts: _T.List [Script] = []
        self._givingId: int = 0
    
    def __iter__(self) -> iter:
        return iter(self._scripts)
    
    def __getitem__(self, id: int) -> Script:
        return self.getScriptById(id)

    def getScriptById(self, id: int) -> Script:
        for script in self._scripts:
            if script.id() == id:
                return script
    
    def getNewId(self) -> int:
        self._givingId += 1
        return self._givingId

    def create(self, user: str) -> Script:
        script = Script(user, self.getNewId())
        self._scripts.append(script)
        return script

    def getScriptsByUser(self, user: str, publishedOnly: bool = False) -> _T.Tuple [Script]:
        scripts = []
        for script in self._scripts:
            if script.user() == user and ( publishedOnly is False or script.published() ):
                scripts.append(script)
        return tuple(script)

    def getScriptsByRobot(self, robot: str) -> _T.Tuple [Script]:
        scripts = []
        for script in self._scripts:
            if script.robot() == robot:
                scripts.append(script)
        return scripts

    def toJson(self) -> dict:
        scripts = []
        for script in self._scripts:
            scripts.append(script.toJson())
        return {
            "scripts" : scripts,
            "id": self._givingId
        }

    def fromJson(json: dict) -> 'ScriptsList':
        slist = ScriptsList()
        slist._givingId = json[ "id" ]
        for script in json[ "scripts" ]:
            slist._scripts.append(Script.fromJSON(script))
        return slist
         