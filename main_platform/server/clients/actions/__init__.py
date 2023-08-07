class ActionsList():
    def __init__(self):
        self._actions = {}
        self.addActionListener("__ping__", self.__ping__)
    
    def loadPlatform(self, platform):
        i18n = getActionsI18n()
        platform.i18n().loadFrom(i18n)
    
    def addActionListener(self, name, function):
        self._actions.update( { name: function } )
    
    async def __ping__(self, client, platform, name, args):
        return client.createRequest("__pong__")
    
    async def execute(self, client, platform, name, args):
        verbose = platform.verbosePolicy()
        if name in self._actions:
            try:
                result = await self._actions[ name ] (client, platform, **args)
            except Exception as exc:
                verbose.log(platform.i18n().translate("ERR_ACTION_EXECUTION_FAILED", error=str(exc), type=type(exc).__name__, name=name), infolevel=verbose.LEVEL_ERROR)
                return False, exc
            else:
                return True, result
        else:
            verbose.log(platform.i18n().translate("ERR_ACTION_NOT_FOUND", name=name), infolevel=verbose.LEVEL_ERROR)
            return False, None

