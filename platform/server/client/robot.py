from client import *
        
class RobotClient(Client):
    def __init__(self, wsock):
        super().__init__(wsock)
