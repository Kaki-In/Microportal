import verbosePolicy as _verbosePolicy
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
    
    def getNewId(self, id):
        self._cid += 1
        return self._cid
        
    def run(self, platform):
        self._platform = platform
        self._platform.i18n().loadFrom(getServerI18n())

        _asyncio.get_event_loop().run_until_complete(self._serve)
        _asyncio.get_event_loop().run_forever()
        
    async def _registerClient(self, wsock, path):
        if   path == "/user":
            client = UserClient(wsock, self.getNewId())
            # TODO
        elif path == "/robot":
            client = RobotClient(wsock, self.getNewId())
            # TODO
        else:
            self._platform.verbosePolicy().log(platform.i18n().translate("SERVER_WARNING_CONNECTION_BAD_PATH", path=path), _verbosePolicy.LEVEL_WARNING)
            return
        client.loadPlatform(platform)
        self._clients.append(client)
        await client.main()
