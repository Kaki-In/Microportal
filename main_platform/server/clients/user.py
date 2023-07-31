from . import *
from .actions.user import *

class UserClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, USER_ACTIONS, id)
        self._user = None
    
