from client import *

class UserClient(Client):
    def __init__(self, wsock):
        super().__init__(wsock)
        
