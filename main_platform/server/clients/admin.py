from . import *
import websockets as _websockets
import traceback as _traceback
import asyncio as _asyncio
import sys as _sys
import time as _tm

class AdminClient(ClientWebSocket):
    def __init__(self, wsock, id):
        super().__init__(wsock, id)
        self._history = []
        self._vars = {}

    async def main(self, platform):
        self._open.emit(platform)
        while True:
            try:
                data = await self.getCommandLine()
                await self.onMessage(data, platform)
            except (_websockets.ConnectionClosedOK, _websockets.ConnectionClosedError) :
                break
            except Exception as exc:
                self._error.emit(exc, platform)
        self._close.emit(platform)
    
    async def getCommandLine(self):
        data = await self.input(">>> ")
        while data.endswith(" "):
            data = data[ : -1 ]
        if not data:
            return
        if data.endswith(":"):
            while data.split("\n")[ -1 ]:
                tab = 0
                while data.split("\n")[ -1 ][tab] == " ":
                    tab += 1
                if data.split("\n")[ -1 ][ -1 ] == ":":
                    tab += 4
                data += "\n" + await self.input("... ", defaultValue=" " * tab)
                while line.endswith(" "):
                    line = data[ : -1 ]
        return data
    
    async def onMessage(self, message, platform):
        await super().onMessage(message, platform)
        try:
            try:
                result = eval(message, {"platform": platform}, self._vars)
                if result is not None:
                    await self.print(repr(result))
            except SyntaxError:
                exec(message, {"platform": platform}, self._vars)
        except:
            await self.print(_traceback.format_exc(), end="")
        finally:
            platform.save()
    
    def run(self, promise):
        task = _asyncio.get_event_loop().create_task(promise)
        while not task.done():
            _tm.sleep(0.1)
        return task.result()
    
    async def input(self, text="", defaultValue=""):
        writing = defaultValue
        lwrite = ""
        pos = 0
        h = 0
        await self.print(text + defaultValue, end="")
        while True:
            message = await self._wsock.recv()
            if message == "\t":
                message = " " * 4
            if message == "\r":
                await self.print("\r\n", end="")
                self._history.append(writing)
                return writing
            elif message == "\x7f":
                if pos > 0:
                    writing = writing[ : pos - 1] + writing[pos : ]
                    pos -= 1
                    await self.print("\x1b[D" + writing [ pos : ] + " ", end="")
                    await self.print("\x1b[D" * (len(writing) - pos + 1), end="")
            elif message == "\x04":
                await self._wsock.close()
            elif message == "\x1b[A":
                if h < len(self._history):
                    await self.print("\x1b[D" * pos + " " * len(writing) + "\x1b[D" * len(writing), end="")
                    h += 1
                    writing = self._history[ - h ]
                    pos = len(writing)
                    await self.print(writing, end="")
            elif message == "\x1b[B":
                if h > 0:
                    await self.print("\x1b[D" * pos + " " * len(writing) + "\x1b[D" * len(writing), end="")
                    h -= 1
                    if h > 0:
                        writing = self._history[ - h ]
                    else:
                        writing = lwrite
                    pos = len(writing)
                    await self.print(writing, end="")
            elif message == "\x1b[C":
                if pos < len(writing):
                    pos += 1
                    await self.print(message, end="")
            elif message == "\x1b[D":
                if pos > 0:
                    pos -= 1
                    await self.print(message, end="")
            else:
                if message[0] == "\x1b":
                    message = message[ 1 : ]
                writing = writing[ : pos] + message + writing [ pos : ]
                await self.print(writing [ pos : ], end="")
                pos += len(message)
                await self.print("\x1b[D" * (len(writing) - pos), end="")
            if h == 0:
                lwrite = writing
    
    async def print(self, *text, end="\n", sep=" "):
        raw_text = ""
        for i in text:
            if raw_text :
                raw_text += sep
            raw_text += i
        raw_text += end
        await self._wsock.send(raw_text.replace("\n", "\r\n"))

