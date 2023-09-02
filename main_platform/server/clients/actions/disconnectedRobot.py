from . import *

class DisconnectedRobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self.addActionListener("mac", self.plugMacAddress)
    
    async def plugMacAddress(self, client, platform, mac):
        rlist = platform.world().robotsList()
        if mac in rlist:
            robot = rlist.getRobot(mac)
        else:
            robot = rlist.addRobot(mac)
        client.setRobot(platform, robot)

