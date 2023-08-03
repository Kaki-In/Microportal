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
            await _asyncio.sleep(1)
            if self._robot is None:
                continue
            rlist = self._robot.requests()
            for request in rlist:
                if request.status() == request.STATUS_WAITING:
                    req = self.createRequest("executeAction", actionName=request.name(), args=request.getArguments())
                    await self.send(req)
                    request.markAsProcessed()
    
    async def onOpen(self, platform):
        await super().onOpen(platform)
        _asyncio.create_task(self.mainRobotRequests(platform))

