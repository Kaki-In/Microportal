from .actions import *
import events as _events
import websockets as _websockets
import json as _json
import asyncio as _asyncio

class ClientWebSocket():
    def __init__(self, wsock, id):
        self._wsock = wsock
        self._closed = False
        self._id = id
        
        self._toSend = []
        self._running = False

        self._open = _events.EventHandler()
        self._open.addEventFunction(self.onOpen)

        self._message = _events.EventHandler()
        self._message.addEventFunction(self.onMessage)

        self._error = _events.EventHandler()
        self._error.addEventFunction(self.onError)

        self._close = _events.EventHandler()
        self._close.addEventFunction(self.onClose)
    
    async def mainDataSend(self):
        while self._running:
            await _asyncio.sleep(0.05)
            if not self._toSend:
                await _asyncio.sleep(1)
                continue
            await self._wsock.send(self._toSend.pop(0))

    async def main(self, platform):
        self._running = True
        self._open.emit(platform)

        _asyncio.create_task(self.mainDataSend())

        while True:
            try:
                message = await self._wsock.recv()
                self._message.emit(message, platform)
            except (_websockets.ConnectionClosedOK, _websockets.ConnectionClosedError) :
                break
            except Exception as exc:
                self._error.emit(exc, platform)
        self._running = False
        self._close.emit(platform)
        await self._wsock.close()
    
    async def onOpen(self, platform):
        platform.logInfo("CLIENT_WEB_SOCKET_ON_OPEN", id=self._id)
    
    async def onMessage(self, message, platform):
        platform.logInfo("CLIENT_WEB_SOCKET_ON_MESSAGE", id=self._id, message=message)
    
    async def onError(self, error, platform):
        platform.logError("CLIENT_WEB_SOCKET_ON_ERROR", type=type(error).__name__, error=str(error), id=self._id)
    
    async def onClose(self, platform):
        platform.logInfo("CLIENT_WEB_SOCKET_ON_CLOSE", id=self._id)
    
    async def send(self, jsonObject):
        message = _json.dumps(jsonObject)
        self._toSend.append(message)

class Client(ClientWebSocket):
    def __init__(self, wsock, actionsList, id):
        super().__init__(wsock, id)
        self._list = actionsList
    
    def actionsList(self):
        return self._list

    def setActionsList(self, actionsList):
        self._list = actionsList
    
    async def onMessage(self, message, platform):
        await super().onMessage(message, platform)
        try:
            obj = _json.loads(message)
            result = await self._list.execute(self, platform, obj[ "name" ], obj[ "args" ])
            if result[ 0 ] and result[ 1 ] is not None:
                await self.send(result[ 1 ])
        except Exception as exc:
            platform.logError("CLIENT_REQUEST_ERROR", type=type(exc).__name__, error=str(exc), id=self._id)

    def createRequest(self, requestName, **args):
        return {"name" : requestName, "args" : args}
