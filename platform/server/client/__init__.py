import asyncio as _asyncio
from .actions import *

class ClientWebSocket():
    def __init__(self, wsock):
        self._wsock = wsock
    
    def start(self, platform):
        _asyncio.createTask(self.main(platform))
    
    async def main(self, platform):
        _asyncio.createTask(self.onOpen(platform))
        # TODO
        ...
    
    async def onOpen(self, event, platform):
        pass
    
    async def onMessage(self, message, platform):
        pass
    
    async def onError(self, error, platform):
        raise error
    
    async def onClose(self, event, platform):
        pass

class Client(ClientWebSocket):
    def __init__(self, wsock, actionsList):
        self._list = actionsList
        super().__init__(wsock)
    
    async def onMessage(self, message, platform):
        self._list.execute(self, message, platform)

