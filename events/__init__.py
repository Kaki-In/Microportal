import asyncio as _asyncio

class EventHandler():
    def __init__(self):
        self._functions = []
    
    def connect(self, func):
        self._functions.append(func)
    
    def disconnect(self, func):
        self._functions.remove(func)
    
    def emit(self, *values):
        for func in self._functions:
            _asyncio.create_task(self._run(func, values))
    
    async def _run(self, func, values):
        if _asyncio.iscoroutinefunction(func):
            await func( *values )
        else:
            func( *values )

