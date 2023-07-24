#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  micropylist.py
#
#  Copyright 2023 Kaki In <kaki@mifamofi.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import asyncio as _asio
import socket as _sock
import parsing as _prs
from ..exceptions import *
import verbosePolicy as _vpol

class ProtocolManager():
    """
    Protocol Manager of a single micropy

    Arguments : 
        - socket : the socket connected to the micropy/client
    """
    def __init__(self, socket, vpol, i18n):
        self._socket = socket
        self._requests = []
        self._answers = []
        self._sentRequests = 0
        self._receiveData = b""
        self._stopping = False
        self._isConnected = False
        self._promise = self.start()
        self._vpol = vpol
        self._i18n = i18n
    
    def start(self):
        """
        Starts the manager
        """
        self._stopping = False
        self._promise = self._run()
        return self._promise

    def stop(self):
        """
        Stops the protocol if started
        """
        if not self._promise : 
            raise ProtocolManageError(ERR_PROTOCOL_MANAGER_NOT_STARTED)
        self._stopping = True
    
    async def waitForEnd(self):
        """
        Waits for the end of the protocol if started
        """
        if not self._stopping :
            raise ProtocolManageError(ERR_PROTOCOL_MANAGER_NOT_STOPPING)
        await self._promise
        self._stopping = False
        self._promise = None
    
    async def _run(self):
        """
        Main loop of the manager (internal method)
        """
        self._isConnected = True
        while not self._stopping:
            while not self._requests :
                self._checkForReceivedRequests()
                await _asio.sleep(0.1)
            request = self._requests.pop(0)
            self._socket.send(bytes(request) + b"\r\n")
        
    def sendRequest(self, request):
        """
        Sends a request.
        """
        request["request-id"], self._sentRequests = self._sentRequests, self._sentRequests + 1
        self._requests.append(request)
    
    async def waitForRequest(self, reqid):
        """
        Waits for the request with the given request id.

        Returns : the answer relative to the id
        """
        while True:
            for i in self._answers:
                if i["request-id"] == reqid:
                    return i
            await _asio.sleep(1)
    
    def _checkForReceivedRequests(self):
        """
        Internal Method. Checks for the answers sent by the micropy
        """
        try:
            data = self._socket.recv(1024)
        except _sock.timeout:
            return

        r = [self._receiveData]
        sdata = data.split("\r\n")

        if r[0][:-2] != "\r\n":
            r[0] += sdata.pop(0)
        r += sdata

        if r[-1][-2:] == "\r\n":
            r.append(b"")
        self._receiveData = r.pop(-1)

        for i in r:
            try:
                self._answers.append(_prs.parse(r).children()[0])
            except SyntaxError as exc:
                self._vpol.log(self._i18n.getMessage("Got an unexpected syntax error when parsing a request"), _vpol.LEVEL_FATAL)
                self.stop()
            except ValueError as exc:
                self._vpol.log(self._i18n.getMessage("Got an unexpected value error when parsing a request"), _vpol.LEVEL_FATAL)
                self.stop()
    
    def make(self, actiontype, **args):
        """
        Makes a DOMObject request of type <actiontype> with the given arguments
        """
        request = _prs.DOMObject("request")
        action = _prs.DOMObject("action")
        action["type"] = actiontype
        for i in args:
            arg = _prs.DOMObject(i)
            arg["value"] = repr(args[i])
            action.addChild(arg)
        request.addChild(action)
        return request

    def getRequestInformations(self, request):
        """
        Gives the informations contained in the request <request>

        Return a tuple as format (actionType:str, arguments:dict)
        """
        children = request.children()
        if len(children) != 1:
            raise ProtocolManageError(ERR_PROTOCOL_MANAGER_INVALID_REQUEST_STRUCT)
        action = children[0]
        if not 'type' in action:
            raise ProtocolManageError(ERR_PROTOCOL_MANAGER_INVALID_REQUEST_STRUCT)
        atype = action["type"]
        args = {}
        for arg in action.children():
            argname = arg.tagName()
            if not "value" in arg:
                raise ProtocolManageError(ERR_PROTOCOL_MANAGER_INVALID_REQUEST_STRUCT)
            value = arg["value"]
            args.update({argname : value})
        return atype, args
    
