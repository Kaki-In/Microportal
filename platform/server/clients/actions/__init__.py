import asyncio as _asyncio
import verbosePolicy as _verbosePolicy

class ActionsList():
    def __init___(self):
        self._actions = {}
    
    def loadPlatform(self, platform):
        i18n = getActionsI18n()
        platform.i18n().loadFrom(i18n)
    
    def addActionListener(self, name, function):
        self._actions.update( { name: function } )
    
    async def execute(self, client, platform, name, **args):
        if name in self._actions:
            try:
                result = await self._actions[ name ] (client, platform, **args)
            except Exception as exc:
                platform.verbosePolicy.log(platform.i18n().translate("ERR_ACTION_EXECUTION_FAILED", error=str(exc), type=type(exc).__name__, name=name), infolevel=_verbosePolicy.LEVEL_ERROR)
                return False, exc
            else:
                return True, result
        else:
            platform.verbosePolicy.log(platform.i18n().translate("ERR_ACTION_NOT_FOUND", name=name), infolevel=_verbosePolicy.LEVEL_ERROR)
            return False, None

