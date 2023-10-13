from . import *
import events as _events

class UserActionsList(ActionsList):
    def __init__(self):
        super().__init__()

        self.addActionListener("sendRobotAction", self.sendRobotAction)

        self.addActionListener("getRobotsList", self.getRobotsList)
        self.addActionListener("getRobotInformations", self.getRobotInformations)

        self.addActionListener("getUsersList", self.getUsersList)
        self.addActionListener("getUserInformations", self.getUserInformations)
        
        self.addActionListener("getScriptsList", self.getScriptsList)
        self.addActionListener("getScriptInformations", self.getScriptInformations)
        self.addActionListener("createScript", self.createScript)
        self.addActionListener("modifyScript", self.modifyScript)
        
        self.addActionListener("changeName", self.changeName)
        self.addActionListener("changeIcon", self.changeIcon)
        self.addActionListener("changePassword", self.changePassword)
        
        self._events = {
            "requestProcessing": _events.EventHandler(),
            "requestProcessed": _events.EventHandler(),
            "requestCanceled": _events.EventHandler()
        }
    
    def addEventListener(self, name, function):
        self._events[ name ].connect(function)
    
    async def sendRobotAction(self, client, platform, robot, action, args):
        rlist = platform.world().robotsList()
        if robot in rlist:

            request = platform.world().requests().create(client.account().name())
            request.setRobot(robot)
            request.setAction(action)
            request.updateArguments(args)
            request.addEventListener("processing", lambda: self._events[ "requestProcessing" ].emit(request))
            request.addEventListener("processed", lambda result: self._events[ "requestProcessed" ].emit(request))
            request.markAsReady()

            return client.createRequest("robotActionSent", robot=robot, request=request.id())
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
     
    async def getScriptsList(self, client, platform):
        slist = platform.world().scripts()
        return client.createRequest("updateScriptsList", scripts=[i.id() for i in slist])
     
    async def getScriptInformations(self, client, platform, id):
        slist = platform.world().scripts()
        script = slist[ id ]
        if script is not None:
            return client.createRequest("updateScriptInformations", name=script.name(), id=id, user=script.user(), published=script.published(), robot=script.robot(), action=script.action(), args=script.getArguments(), creationTime=script.creationTime(), modificationTime=script.modificationTime())
        else:
            message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_SCRIPT", id=id)
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
            script = platform.world().scripts().create(client.account().name())
            script.setName(title)
            return client.createRequest("scriptCreationSuccess", id=script.id())
        else:
           message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_ROBOT", robot=robot)
           return client.createRequest("scriptCreationError", error=message)
    
    async def modifyScript(self, client, platform, id, name=None, published=None, action=None, args=None, robot=None):
        slist = platform.world().scripts()
        script = slist[ id ]
        if script is not None:
            if script.user() == client.account().name():
                if name is not None:
                    script.setName(name)
                if published is not None:
                    if published:
                        script.publish()
                    else:
                        script.unpublish()
                if action is not None:
                    script.setAction(action)
                if args is not None:
                    script.setArguments(args)
                if robot is not None and robot in platform.world().robotsList():
                    script.robot = robot
                return client.createRequest("scriptModificationSuccess")
            else:
                message = platform.i18n().translate("USER_ACTION_ERR_PERMISSION_DENIED")
                return client.createRequest("scriptModificationError", error=message)
        else:
            message = platform.i18n().translate("USER_ACTION_ERR_NO_SUCH_SCRIPT", id=id)
            return client.createRequest("scriptModificationError", error=message)

