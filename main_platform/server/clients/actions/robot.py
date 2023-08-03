from . import *

class RobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self.addActionListener("setRobotName", self.setRobotName)
        self.addActionListener("setRobotType", self.setRobotType)
    
    async def setRobotName(self, client, platform, name):
        client.robot().setName(name)

    async def setRobotType(self, client, platform, type):
        client.robot().setType(type)

ROBOT_ACTIONS = RobotActionsList()
