from . import *
from .actions.robot import *
from .actions.disconnectedRobot import *

import asyncio as _asyncio

class RobotClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, DISCONNECTED_ROBOT_ACTIONS, id)
        self._robot = None
    
    def setRobot(self, robot):
        self._robot = robot
        if robot is None:
            self.setActionsList(DISCONNECTED_ROBOT_ACTIONS)
        else:
            self.setActionsList(ROBOT_ACTIONS)
            robot.setLastConnectionDateNow()

    def robot(self):
        return self._robot
    
    async def mainRobotRequests(self, platform):
        while self._running:
            await _asyncio.sleep(0.05)
            if self._robot is None:
                await _asyncio.sleep(1)
                continue
            rlist = self._robot.requests()
            if not len(rlist):
                await _asyncio.sleep(1)
                continue
            for reqid in range(len(rlist)):
                request = rlist[ reqid ]
                if request.status() == request.STATUS_WAITING:
                    req = self.createRequest("executeAction", actionName=request.name(), args=request.getArguments(), reqid=reqid)
                    await self.send(req)
                    request.markAsProcessing()

                    user = platform.world().usersList()[ request.user() ]
                    request = self.createRequest("requestProcessing", robot=self.robot().id(), id=reqid)
                    await platform.server().sendToUser(user, request)
    
    async def onOpen(self, platform):
        await super().onOpen(platform)
        _asyncio.create_task(self.mainRobotRequests(platform))

    async def onClose(self, platform):
        await super().onClose(platform)
        if self._robot is not None:
            rlist = self._robot.requests()
            for reqid in range(len(rlist)):
                request = rlist[ reqid ]
                if request.status() == request.STATUS_WAITING:
                    request.cancel()

                    user = platform.world().usersList()[ request.user() ]
                    request= self.createRequest("requestCanceled", robot=self.robot().id(), id=reqid)
                    await platform.server().sendToUser(user, request)

        self.setRobot(None)
