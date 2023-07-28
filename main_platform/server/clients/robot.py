from . import *
from .actions.robot import *

class RobotClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, ROBOT_ACTIONS, id)
        self._name = ""
        self._type = None

