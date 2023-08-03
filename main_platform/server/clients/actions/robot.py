from . import *

class RobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self.addActionListener("setRobotName", self.setRobotName)
        self.addActionListener("setRobotType", self.setRobotType)
    
    async def setRobotName(self, client, platform, name):
        self._robot.setName(name)

    async def setRobotType(self, client, platform, type):
        self._robot.setType(type)

ROBOT_ACTIONS = RobotActionsList()
