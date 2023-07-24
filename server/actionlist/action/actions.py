from . import *

class SetPinAction(Action):
    def __init__(self):
        super().__init__("setpin", "micropyId", "pin", "active")
    
    async def main(self, mlist, ulist, micropyId, pin, active):
        micropy = mlist.getMicropyFromId(micropyId)
        request = micropy.protocolManager().make("setpin", pin = pin, active = active)
        requestId = micropy.submitRequest(request)
        answer = await micropy.protocolManager().waitForRequest(requestId)
        answername, answerargs = micropy.protocolManager().getRequestInformations(answer)
        if answername != "septin" or not "response" in answerargs:
            raise ActionExecutionError(ERR_ACTION_INVALID_ANSWER)
        return True, answerargs

class GetPinAction(Action):
    def __init__(self):
        super().__init__("getpin", "micropyId", "pin")
    
    async def main(self, mlist, ulist, micropyId, pin):
        micropy = mlist.getMicropyFromId(micropyId)
        request = micropy.protocolManager().make("getpin", pin = pin)
        requestId = micropy.submitRequest(request)
        answer = await micropy.protocolManager().waitForRequest(requestId)
        answername, answerargs = micropy.protocolManager().getRequestInformations(answer)
        if answername != "septin" or not "response" in answerargs:
            raise ActionExecutionError(ERR_ACTION_INVALID_ANSWER)
        return True, answerargs
        
class GetNameAction(Action):
    def __init__(self):
        super().__init__("getname", "micropyId")
    
    async def main(self, mlist, ulist, micropyId):
        micropy = mlist.getMicropyFromId(micropyId)
        return micropy.name()
        
class GetTypeAction(Action):
    def __init__(self):
        super().__init__("gettype", "micropyId")
    
    async def main(self, mlist, ulist, micropyId):
        micropy = mlist.getMicropyFromId(micropyId)
        return micropy.type()
        
class GetTypeAction(Action):
    def __init__(self):
        super().__init__("gettype", "micropyId")
    
    async def main(self, mlist, ulist, micropyId):
        micropy = mlist.getMicropyFromId(micropyId)
        return micropy.type()
        
