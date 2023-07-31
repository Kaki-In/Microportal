import asyncio as _asyncio
from .actions import *
import events as _events
import websockets as _websockets

class ClientWebSocket():
    def __init__(self, wsock):
        self._wsock = wsock
        self._closed = False

        self._open = _events.EventHandler()
        self._open.addEventFunction(self.onOpen)

        self._message = _events.EventHandler()
        self._message.addEventFunction(self.onMessage)

        self._error = _events.EventHandler()
        self._error.addEventFunction(self.onError)

        self._close = _events.EventHandler()
        self._close.addEventFunction(self.onClose)

    async def main(self, platform):
        while True:
            try:
                self._open.emit(platform)
                async for message in _websockets:
                    self._message.emit(message, platform)
            except _websockets.ConnectionClosedOK:
                break
            except Exception as exc:
                self._error.emit(exc, platform)
        self._close.emit(platform)
    
    async def onOpen(self, platform):
        verbosePolicy = platform.configuration().verboseConfiguration
        verbosePolicy.log("Client is connected", infolevel = verbosePolicy.LEVEL_INFO) 
    
    async def onMessage(self, message, platform):
        verbosePolicy = platform.configuration().verboseConfiguration
        verbosePolicy.log("Received message", repr(message), infolevel = verbosePolicy.LEVEL_INFO) 
    
    async def onError(self, error, platform):
        verbosePolicy = platform.configuration().verboseConfiguration
        verbosePolicy.log("An error occured", repr(error), infolevel = verbosePolicy.LEVEL_INFO) 
    
    async def onClose(self, platform):
        verbosePolicy = platform.configuration().verboseConfiguration
        verbosePolicy.log("Client is disconnected", infolevel = verbosePolicy.LEVEL_INFO) 

class Client(ClientWebSocket):
    def __init__(self, wsock, actionsList, id):
        super().__init__(wsock)
        self._list = actionsList
        self._id = id
    
    async def onMessage(self, message, platform):
        self._list.execute(self, message, platform)

