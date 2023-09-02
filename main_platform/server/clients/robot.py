from . import *
from .actions.robot import *
from .actions.disconnectedRobot import *

import asyncio as _asyncio

class RobotClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, DisconnectedRobotActionsList(), id)
        self._robot = None
    
    def setRobot(self, platform, robot):
        self._robot = robot
        if robot is None:
            self.setActionsList(DisconnectedRobotActionsList())
        else:
            self.setActionsList(RobotActionsList())
            robot.setLastConnectionDateNow()

            requests = platform.world().requests().getRequestsByRobot(self._robot.id())
            for request in requests:
                if request.robot() == robot.id() and request.state() == request.STATE_WAITING:
                    _asyncio.create_task(self.sendRequest(request))

    def robot(self):
        return self._robot

    async def sendRequest(self, request):
        req = self.createRequest("executeAction", actionName=request.action(), args=request.getArguments(), reqid=request.id())
        await self.send(req)
        request.markAsProcessing()
