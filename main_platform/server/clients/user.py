from . import *
from .actions.user import *
from .actions.disconnectedUser import *

class UserClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, DisconnectedUserActionsList(), id)
        self._user = None
    
    def setAccount(self, user):
        if user is None:
            self._user = None
            self.setActionsList(DisconnectedUserActionsList())
        else:
            self._user = user

            self.setActionsList(UserActionsList())
            self.actionsList().addEventListener("requestProcessing", self.onRequestProcessing)
            self.actionsList().addEventListener("requestProcessed", self.onRequestProcessed)
            self.actionsList().addEventListener("requestCanceled", self.onRequestCanceled)
            
            user.setLastConnectionDateNow()
    
    def account(self):
        return self._user

    async def onRequestProcessing(self, request):
        await self.send(self.createRequest("requestProcessing", id = request.id()))
     
    async def onRequestProcessed(self, request):
        await self.send(self.createRequest("requestProcessed", id = request.id(), result = request.result()))
     
    async def onRequestCanceled(self, request):
        await self.send(self.createRequest("requestCanceled", id = request.id()))
     
