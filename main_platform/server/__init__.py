import websockets as _websockets
import asyncio as _asyncio
import signal as _signal
import ssl as _ssl

from .clients.user import *
from .clients.robot import *
from .clients.admin import *

class Server():
    def __init__(self, host: str="", port: int=8266, sslContext: _ssl.SSLContext=None) -> "Server":
        self._host: str = host
        self._port: int = port
        self._context: _ssl.SSLContext = sslContext
        self._serve = _websockets.serve(self._registerClient, self._host, self._port, ssl=sslContext)
        
        self._cid: int = 0
        
        self._users: list[ UserClient ] = []
        self._robots: list[ RobotClient ] = []
        self._admins: list[ AdminClient ] = []
        
    def users(self) -> list[ UserClient ]:
        return self._users.copy()
    
    def robots(self) -> list[ UserClient ]:
        return self._robots.copy()
    
    def admins(self) -> list[ AdminClient ]:
        return self._admins.copy()
    
    def getNewId(self) -> int:
        self._cid += 1
        return self._cid
        
    def run(self, platform: "_Platform") -> None:
        self._platform = platform
        
        platform.logInfo("SERVER_STARTING")
        platform.world().requests().addEventListener("requestReady", self.onRequestReady)
        
        platform.world().usersList().addEventListener("userModified", self.onUserModified)
        platform.world().usersList().addEventListener("userAdded", self.onUserModified)
        platform.world().usersList().addEventListener("userRemoved", self.onUserRemoved)
        
        platform.world().robotsList().addEventListener("robotModified", self.onRobotModified)
        platform.world().robotsList().addEventListener("robotAdded", self.onRobotModified)
        platform.world().robotsList().addEventListener("robotRemoved", self.onRobotRemoved)
        
        try:
            _asyncio.get_event_loop().run_until_complete(self._serve)
            _asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            platform.logInfo("SERVER_STOPPED")
    
    async def onUserModified(self, user: "User") -> None:
        for client in self._users:
            if client.account() is not None:
                await client.send(await client.actionsList().getUserInformations(client, self._platform, user.name()))
        
    async def onUserRemoved(self, user) -> None:
        for userClient in self.getUserClients(user.name()):
            await userClient.close()
        for client in self._users:
            if client.account() is not None:
                await client.send(await client.actionsList().getUsersList(client, self._platform))
        
    async def onRobotModified(self, robot: "Robot") -> None:
        for client in self._users:
            if client.account() is not None:
                await client.send(await client.actionsList().getRobotInformations(client, self._platform, robot.id()))
        
    async def onRobotRemoved(self, robot) -> None:
        robotClient = self.getRobotClient(robot.id())
        if robotClient:
            await robotClient.close()
        for client in self._users:
            if client.account() is not None:
                await client.send(await client.actionsList().getRobotsList(client, self._platform))
        
    async def onRequestReady(self, request):
        await self.sendRobotRequest(request)
    
    async def sendRobotRequest(self, request):
        robot = self.getRobotClient(request.robot())
        if robot is not None:
            await robot.sendRequest(request)
    
    def getUserClients(self, user):
        clients = []
        for client in self._users.copy():
            account = client.account()
            if account and account.name() == user:
                clients.append(client)
        return clients
    
    def getRobotClient(self, robot):
        for client in self._robots.copy():
            crobot = client.robot()
            if crobot and crobot.id() == robot:
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

        if  path == "/user":
            # inform the others that the user has been disconnected.
            # unuseful for the connection because of the last_connection time that
            # already calls a refresh of the user
            account = client.account()
            if account:
                await self.onUserModified(account)
        elif path == "/robot":
            robot = client.robot()
            if robot:
                await self.onRobotModified(robot)
    
    async def close(self):
        loop = _asyncio.get_event_loop()
        stop = loop.create_future()
        loop.add_signal_handler(_signal.SIGTERM, stop.set_result, None)
        await stop
    
    