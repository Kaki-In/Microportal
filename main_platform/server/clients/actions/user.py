from . import *

class UserActionsList(ActionsList):
    def __init__(self):
        super().__init__()

        self.addActionListener("sendRobotAction", self.sendRobotAction)

        self.addActionListener("getRobotsList", self.getRobotsList)
        self.addActionListener("getRobotInformations", self.getRobotInformations)

        self.addActionListener("getUsersList", self.getUsersList)
        self.addActionListener("getUserInformations", self.getUserInformations)
        
        self.addActionListener("changeName", self.changeName)
        self.addActionListener("changeIcon", self.changeIcon)
        self.addActionListener("changePassword", self.changePassword)
    
    async def sendRobotAction(self, client, platform, robot, action, args):
        rlist = platform.world().robotsList()
        if robot in rlist:
            request = rlist[ robot ].requests().createRequest(client.account().name(), action, **args)
            return client.createRequest("robotActionSent", robot=robot, request=rlist[ robot ].requests().index(request))
        else:
            message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_ROBOT", mac=robot)
            return client.createRequest("robotActionError", error=message)
     
    async def getRobotsList(self, client, platform):
        rlist = platform.world().robotsList()
        return client.createRequest("updateRobotsList", robots=list(rlist))
     
    async def getRobotInformations(self, client, platform, mac):
       rlist = platform.world().robotsList()
       if mac in rlist:
           robot = rlist[ mac ]
           return client.createRequest("updateRobotInformations", name=robot.id(), type=robot.type(), last_connection=robot.lastConnectionDate(), mac=mac)
       else:
           message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_ROBOT", mac=mac)
           return client.createRequest("informationError", error=message)
    
    async def getUsersList(self, client, platform):
        ulist = platform.world().usersList()
        return client.createRequest("updateUsersList", users=list(ulist))
     
    async def getUserInformations(self, client, platform, name):
       ulist = platform.world().usersList()
       if name in ulist:
           user = ulist[ name ]
           return client.createRequest("updateUserInformations", name=user.name(), icon=user.icon().toJson(), last_connection=user.lastConnectionDate())
       else:
           message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_USER", name=name)
           return client.createRequest("informationError", error=message)
     
    async def changeName(self, client, platform, name):
        lastname = client.account().name()
        platform.world().usersList().renameUser(lastname, name)
    
    async def changeIcon(self, client, platform, icon):
        client.account().setIcon(icon.encode("utf-8"))
    
    async def changePassword(self, client, platform, password, new_password):
        if client.account().passwordMatches(password):
            client.account().setPassword(new_password)
            return self.createRequest("passwordChangeSuccess")
        else:
            message = platform.i18n().translate("USER_ACTION_ERR_BAD_PASSWORD")
            return self.createRequest("passwordChangeFailed", error=message)
    
    async def createScript(self, client, platform, robot, title):
        rlist = platform.world().robotsList()
        if robot in rlist:
            script = rlist[ robot ].scripts().createNewScripts(client.account().name())
            script.setTitle(title)
            return client.createRequest("scriptCreationSuccess")
        else:
           message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_ROBOT", mac=mac)
           return client.createRequest("scriptCreationError", error=message)
    
USER_ACTIONS = UserActionsList()
