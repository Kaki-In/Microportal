from . import *

class DisconnectedRobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self.addActionListener("mac", self.plugMacAddress())
    
    def plugMacAddress(self, client, platform, mac):
        pass

DISCONNECTED_ROBOT_ACTIONS = DisconnectedRobotActionsList()
