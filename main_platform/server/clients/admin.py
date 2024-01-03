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
        self._vars = {
            "platform": None,
            "print": self.print,
            "input": self.input
        }

    async def main(self, platform):
        self._open.emit(platform)
        ownerConfiguration = platform.configuration().ownerConfiguration
        await self.print(platform.i18n().translate("ADMIN_WELCOMING_MESSAGE", surname = ownerConfiguration.getOwnerSurname(), name = ownerConfiguration.getOwnerName()))
        try:
            password = await self.input(platform.i18n().translate("ADMIN_ASK_PASSWORD_MESSAGE"), display = False)
        except (_websockets.ConnectionClosedOK, _websockets.ConnectionClosedError) :
            self._close.emit(platform)
            return
        except (KeyboardInterrupt, EOFError):
            password = None
        if password == platform.configuration().ownerConfiguration.getOwnerPassword():
            await self.print(platform.i18n().translate("ADMIN_ACCESS_GRANTED"))
        else:
            await self.print(platform.i18n().translate("ADMIN_ACCESS_DENIED"))
            self._close.emit(platform)
            return

        while True:
            try:
                data = await self.getCommandLine()
                await self.onMessage(data, platform)
            except (_websockets.ConnectionClosedOK, _websockets.ConnectionClosedError, SystemExit, EOFError) :
                break
            except KeyboardInterrupt:
                await self.print(_traceback.format_exc(), end="")
            except Exception as exc:
                self._error.emit(exc, platform)
        try:
            await self.print("\n" + platform.i18n().translate("ADMIN_GOODBYE_MESSAGE"))
        except:
            pass
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
                while data.endswith(" "):
                    data = data[ : -1 ]
        return data

    def moveToAFunction(self, message):
        if message.count("\n"):
            return "async def __execute__():\n    " + message.replace("\n", "    ") + "\n    return locals()\n"
        else:
            return "async def __execute__():\n    return " + message + ", locals()\n"
    
    async def onMessage(self, message, platform):
        await super().onMessage(message, platform)
        self._vars["platform"] = platform
        if not message:
            return
        try:
            try:
                exec(self.moveToAFunction(message), self._vars, self._vars)
                result = await self._vars["__execute__"] ()
                if result[ 0 ] is not None:
                    await self._wsock.send(repr(result[ 0 ]) + "\r\n")
                self._vars.update(result[ 1 ])
            except SyntaxError:
                exec(message, self._vars, self._vars)
        except SystemExit:
            raise
        except:
            await self.print(_traceback.format_exc(), end="")
        finally:
            platform.save()
    
    def run(self, promise):
        task = _asyncio.get_event_loop().create_task(promise)
        while not task.done():
            _tm.sleep(0.1)
        return task.result()
    
    async def input(self, text="", defaultValue="", display = True):
        writing = defaultValue
        lwrite = ""
        pos = len(defaultValue)
        h = 0
        await self.print(text, end="")
        if display:
            await self.print(defaultValue, end="")
        while True:
            message = await self._wsock.recv()
            if message == "\t":
                message = " " * 4
            if message == "\r":
                await self.print("\r\n", end="")
                if display: self._history.append(writing)
                return writing
            elif message == "\x7f":
                if pos > 0:
                    writing = writing[ : pos - 1] + writing[pos : ]
                    pos -= 1
                    if display:
                        await self.print("\x1b[D" + writing [ pos : ] + " ", end="")
                        await self.print("\x1b[D" * (len(writing) - pos + 1), end="")
            elif message == "\x03":
                await self.print("^C", end="\r\n")
                raise KeyboardInterrupt()
            elif message == "\x04":
                raise EOFError()
            elif message == "\x1b[A" :
                if display and h < len(self._history):
                    await self.print("\x1b[D" * pos + " " * len(writing) + "\x1b[D" * len(writing), end="")
                    h += 1
                    writing = self._history[ - h ]
                    pos = len(writing)
                    await self.print(writing, end="")
            elif message == "\x1b[B":
                if display and h > 0:
                    await self.print("\x1b[D" * pos + " " * len(writing) + "\x1b[D" * len(writing), end="")
                    h -= 1
                    if h > 0:
                        writing = self._history[ - h ]
                    else:
                        writing = lwrite
                    pos = len(writing)
                    await self.print(writing, end="")
            elif message == "\x1b[C":
                if display and pos < len(writing):
                    pos += 1
                    await self.print(message, end="")
            elif message == "\x1b[D":
                if display and pos > 0:
                    pos -= 1
                    await self.print(message, end="")
            else:
                if message[0] == "\x1b":
                    message = message[ 1 : ]
                writing = writing[ : pos] + message + writing [ pos : ]
                if display: 
                    await self.print(writing [ pos : ], end="")
                pos += len(message)
                if display: 
                    await self.print("\x1b[D" * (len(writing) - pos), end="")
            if h == 0:
                lwrite = writing
    
    async def print(self, *text, end="\r\n", sep=" "):
        raw_text = ""
        for i in text:
            if raw_text :
                raw_text += sep
            raw_text += i
        raw_text += end
        await self._wsock.send(raw_text.replace("\n", "\r\n"))

