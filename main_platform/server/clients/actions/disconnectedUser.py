from . import *

class DisconnectedUserActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self.addActionListener("createAccount", self.createAccount)
        self.addActionListener("verifyMail", self.verifyMail)
        self.addActionListener("connectToAccount", self.connectToAccount)
    
    async def createAccount(self, client, platform, name, password, mail):
        userslist = platform.world().usersList()
        if name in userslist:
            message = platform.i18n().translate("ACTION_ACCOUNT_CREATION_ERR_ALREADY_EXISTING", name=name)
            return client.createRequest("accountCreationFailed", message=message)
        else:
            userslist.addUser(name, password, mail)
            return await self.connectToAccount(client, platform, name, password)

    async def verifyMail(self, client, platform, name, password, code):
        userslist = platform.world().usersList()
        if name in userslist:
            user = userslist.getUser(name)
            if user.passwordMatches(password):
                codeIsValid = user.mailAddress().submitVerificationCode(code)
                if codeIsValid:
                    return client.createRequest("mailVerificationSuccess")
                else:
                    message = platform.i18n().translate("ACTION_MAIL_ERR_VERIFICATION_BAD_CODE")
                    return client.createRequest("mailVerificationFailed", message=message)
            else:
                message = platform.i18n().translate("ACTION_CONNECT_ERR_BAD_PASSWORD")
                return client.createRequest("mailVerificationFailed", message=message)
        else:
            message = platform.i18n().translate("ACTION_CONNECT_ERR_NO_SUCH_ACCOUNT", name=name)
            return client.createRequest("mailVerificationFailed", message=message)
    
    async def connectToAccount(self, client, platform, name, password):
        userslist = platform.world().usersList()
        if name in userslist:
            user = userslist.getUser(name)
            if user.passwordMatches(password):
                if user.mailAddress().isVerified():
                    client.setAccount(user)
                    return client.createRequest("connectionSuccess")
                else:
                    user.mailAddress().startVerification(platform)
                    return client.createRequest("startMailVerification")
            else:
                message = platform.i18n().translate("ACTION_CONNECT_ERR_BAD_PASSWORD")
                return client.createRequest("mailVerificationFailed", message=message)
        else:
            message = platform.i18n().translate("ACTION_CONNECT_ERR_NO_SUCH_ACCOUNT", name=name)
            return client.createRequest("mailVerificationFailed", message=message)

DISCONNECTED_USER_ACTIONS = DisconnectedUserActionsList()
