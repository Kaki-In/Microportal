from . import *
from .actions.user import *
from .actions.disconnectedUser import *

class UserClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, DISCONNECTED_USER_ACTIONS, id)
        self._user = None
    
