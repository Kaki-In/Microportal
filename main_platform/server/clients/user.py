from . import *
from .actions.user import *
from .actions.disconnectedUser import *

class UserClient(Client):
    def __init__(self, wsock, id):
        super().__init__(wsock, DISCONNECTED_USER_ACTIONS, id)
        self._user = None
    
    def setAccount(self, user):
        if user is None:
            self._user = None
            self.setActionsList(DISCONNECTED_USER_ACTIONS)
        else:
            self._user = user
            self.setActionsList(USER_ACTIONS)
    
    def account(self):
        return self._user
