import websockets as _websockets
import asyncio as _asyncio
import signal as _signal

from .clients.user import *
from .clients.robot import *
from .clients.admin import *

class Server():
    def __init__(self, host="", port=8266, sslContext=None):
        self._host = host
        self._port = port
        self._context = sslContext
        self._serve = _websockets.serve(self._registerClient, self._host, self._port, ssl=sslContext)
        
        self._cid = 0
        
        self._users = []
        self._robots = []
        self._admins = []
        
    def users(self):
        return self._users.copy()
    
    def robots(self):
        return self._robots.copy()
    
    def admins(self):
        return self._admins.copy()
    
    def getNewId(self):
        self._cid += 1
        return self._cid
        
    def run(self, platform):
        self._platform = platform
        
        platform.logInfo("SERVER_STARTING")
        platform.world().requests().addEventListener("requestReady", self.onRequestReady)
        
        try:
            _asyncio.get_event_loop().run_until_complete(self._serve)
            _asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            platform.logInfo("SERVER_STOPPED")
        
    async def onRequestReady(self, request):
        await self.sendRobotRequest(request)
    
    async def sendRobotRequest(self, request):
        robot = self.getRobotClient(request.robot())
        if robot is not None:
            await robot.sendRequest(request)
    
    def getUserClients(self, user):
        clients = []
        for client in self._users.copy():
            if client.account().name() == user:
                clients.append(client)
        return clients
    
    def getRobotClient(self, robot):
        for client in self._robots.copy():
            crobot = client.robot()
            if not crobot:
                continue
            if crobot.id() == robot:
                return client
    
    async def sendToUser(self, user, request):
        clients = self.getUserClients(user)
        for client in clients:
            await client.send(request)
    
    async def sendToRobot(self, robot, request):
        client = self.getRobotClient(robot)
        if client is not None:
            await client.send(request)
   
    async def sendToAllUsers(self, request):
        for client in self._users:
            await client.send(request)
    
    async def sendToAllUsersExcept(self, user, request):
        for client in self._users:
            if client.account() is not user:
                await client.send(request)
    
    async def _registerClient(self, wsock, path):
        if   path == "/user":
            client = UserClient(wsock, self.getNewId())
            l = self._users
        elif path == "/robot":
            client = RobotClient(wsock, self.getNewId())
            l = self._robots
        elif path == "/admin":
            client = AdminClient(wsock, self.getNewId())
            l = self._admins
        else:
            self._platform.logWarning("SERVER_WARNING_CONNECTION_BAD_PATH", path=path)
            await wsock.close()
            return
        l.append(client)
        await client.main(self._platform)
        l.remove(client)
    
    async def close(self):
        loop = _asyncio.get_event_loop()
        stop = loop.create_future()
        loop.add_signal_handler(_signal.SIGTERM, stop.set_result, None)
        await stop
    
    