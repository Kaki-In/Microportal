from . import *
import websockets as _websockets

class AdminClient(ClientWebSocket):
    def __init__(self, wsock, id):
        super().__init__(wsock, id)
        self._history = []
        self._vars = {}

    async def main(self, platform):
        self._open.emit(platform)
        writing = ""
        pos = 0
        h = 0
        while True:
            try:
                message = await self._wsock.recv()
                if message == "\r":
                    await self._wsock.send("\r\n")
                    await self.onMessage(writing, platform)
                    writing = ""
                    pos = 0
                    await self._wsock.send("\r\n>>> ")
                elif message == "\x7f":
                    if pos > 0:
                        writing = writing[ : pos - 1] + writing[pos : ]
                        pos -= 1
                        await self._wsock.send("\x1b[D" + writing [ pos : ] + " ")
                        await self._wsock.send("\x1b[D" * (len(writing) - pos + 1))
                elif message == "\x04":
                    await self._wsock.close()
                elif message == "\x1b[A":
                    pass
                elif message == "\x1b[B":
                    pass
                elif message == "\x1b[C":
                    if pos < len(writing):
                        pos += 1
                        await self._wsock.send(message)
                elif message == "\x1b[D":
                    if pos > 0:
                        pos -= 1
                        await self._wsock.send(message)
                else:
                    writing = writing[ : pos] + message + writing [ pos : ]
                    await self._wsock.send(writing [ pos : ])
                    pos += 1
                    await self._wsock.send("\x1b[D" * (len(writing) - pos))
            except (_websockets.ConnectionClosedOK, _websockets.ConnectionClosedError) :
                break
            except Exception as exc:
                self._error.emit(exc, platform)
        self._close.emit(platform)
    
    async def onOpen(self, platform):
        await super().onOpen(platform)
        await self._wsock.send(">>> ")
    
    async def onMessage(self, message, platform):
        await super().onMessage(message, platform)
        try:
            try:
                result = eval(message, {"platform": platform}, self._vars)
                if result is not None:
                    await self._wsock.send(repr(result))
            except SyntaxError:
                exec(message, {"platform": platform}, self._vars)
                await self._wsock.send("Done")
        except Exception as exc:
            await self._wsock.send(type(exc).__name__ + ": " + str(exc))

