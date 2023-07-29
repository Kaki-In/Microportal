from . import *
from .mail import *

import os as _os

class Resources(ResourcesDirectory):
    def __init__(self, directory):
        super().__init__(directory)

        self.mail = MailResources(self._directory + "/mail")
    
    

