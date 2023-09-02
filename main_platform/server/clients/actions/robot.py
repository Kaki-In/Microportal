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
        request = platform.world().requests().getRequestById(reqid)
        request.markAsProcessed(result)

