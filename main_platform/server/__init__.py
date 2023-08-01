import i18n_setup as _i18n
import websockets as _websockets
import asyncio as _asyncio

from .clients.user import *
from .clients.robot import *

class Server():
    def __init__(self, host="", port=8266, sslContext=None):
        self._host = host
        self._port = port
        self._context = sslContext
        self._serve = _websockets.serve(self._registerClient, self._host, self._port, ssl=sslContext)
        
        self._cid = 0
        
        self._clients = []
    
    def getNewId(self):
        self._cid += 1
        return self._cid
        
    def run(self, platform):
        self._platform = platform
        
        platform.logInfo("SERVER_STARTING")
        
        try:
            _asyncio.get_event_loop().run_until_complete(self._serve)
            _asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            platform.logInfo("SERVER_STOPPED")
        
    async def _registerClient(self, wsock, path):
        if   path == "/user":
            client = UserClient(wsock, self.getNewId())
        elif path == "/robot":
            client = RobotClient(wsock, self.getNewId())
        else:
            self._platform.logWarning("SERVER_WARNING_CONNECTION_BAD_PATH")
            await wsock.close()
            return
        self._clients.append(client)
        await client.main(self._platform)
