from . import *

class RobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self.addActionListener("setRobotName", self.setRobotName)
        self.addActionListener("setRobotType", self.setRobotType)
        self.addActionListener("markAsProcessed", self.markAsProcessed)
    
    async def setRobotName(self, client, platform, name):
        client.robot().setName(name)

    async def setRobotType(self, client, platform, type):
        client.robot().setType(type)
    
    async def markAsProcessed(self, client, platform, reqid, result):
        request = client.robot().requests()[ reqid ]
        request.markAsProcessed(result)
        
        username = request.user()
        for c in platform.server().users():
            user = c.account()
            if user is not None and user.name() == username:
                await c.send(c.createRequest("requestProcessed", robot=client.robot().name(), id=reqid, result=result))

ROBOT_ACTIONS = RobotActionsList()
