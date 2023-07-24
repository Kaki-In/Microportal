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

import parsing as _ps
from ..pman import *
from ..exceptions import *
import asyncio as _asio
import socket as _sock
import random as _rd

class Micropy():
    """
    A micropy

    Micropy():
     -> instantiate a blank micropy (automatically used, please don't do it yourself)
    """
    def __init__(self, id, addr = None, password = None, name = None, type = None, mlist = None, vpol = None, i18n = None):
        self._addr = addr
        self._password = password
        self._name = name
        self._type = type
        self._conn = False
        self._socket = None
        self._protocolManager = None
        self._version = None
        self._mlist = list
        self._id = id
        self._vpol = vpol
        self._i18n = i18n
    
    def save(self):
        """
        Saves the micropy in the file of the micropyList
        """
        if self._mlist is not None:
            self._mlist.save()
    
    def generatePassword(self, addr):
        """
        Internal method.
        Generates and returns a password which is given to the micropy to connect
        """
        password = ""
        for i in range(256):
            password += _rd.choice((_rd.choice(([chr(0x41 + i) for i in range(26)], [chr(0x61 + i) for i in range(26)], [str(i) for i in range(10)]))))
        return password
        
    def identificator(self):
        """
        Returns the micropy identificator
        """
        return self._id

    def version(self):
        """
        Returns the version of the connected micropy
        """
        return self._version

    def name(self):
        """
        Returns the name of the connected micropy
        """
        return self._name

    def type(self):
        """
        Returns the type of the connected micropy
        """
        return self._type

    def address(self):
        """
        Returns the address of the micropy
        """
        return self._addr

    def password(self):
        """
        Returns the password of the micropy
        """
        return self._password

    def isConnected(self):
        """
        Returns the connection status (True if connected, False else)
        """
        return self._conn

    def protocolManager(self):
        """
        Returns the ProtocolManager which must be used to interact with the micropy
        """
        if not self._conn : 
            raise MicropyInteractionError(ERR_MICROPY_NOT_CONNECTED)
        return self._protocolManager

    async def connectToSocket(self, socket):
        """
        Links the micropy with the given socket
        """
        if self._conn : 
            raise MicropyInteractionError(ERR_MICROPY_ALREADY_CONNECTED)
        self._socket = socket
        self._socket.send("RUIr\r\nQUIT\r\n")
        a = self._socket.recv(1024)
        if a!="IAmIr\r\n" : 
            self._socket.close()
            raise MicropyInteractionError(ERR_MICROPY_NOT_VALID_MICROPY_ANSWER)
        self._protocolManager = ProtocolManager(self._socket, self._vpol, self._i18n)
        if self._password is None:
            request = self._protocolManager.make("ping")
            requestid = self.submitRequest(request, force = True)
            answer = await self._protocolManager.waitForRequest(requestid)
            answertype, answercontent = self._protocolManager.getRequestInformations(answer)
            if answertype != "pong" or (not "password" in answercontent) or answercontent["password"] != self._password:
                self.closeConnection()
                raise MicropyInteractionError(ERR_MICROPY_NOT_VALID_MICROPY_ANSWER)
        else:
            password = self.generatePassword()
            request = self._protocolManager.make("create", password = password, id = self._id)
            requestid = self.submitRequest(request, force = True)
            answer = await self._protocolManager.waitForRequest(requestid)
            answertype, answercontent = self._protocolManager.getRequestInformations(answer)
            if answertype != "confirm-creation":
                self.closeConnection()
                raise MicropyInteractionError(ERR_MICROPY_NOT_VALID_MICROPY_ANSWER)
            self._password = password
        if "micropyName" in answercontent:
            self._name = answercontent["micropyName"]
        if "micropyType" in answercontent:
            self._type = answercontent["micropyType"]
        if "micropyVersion" in answercontent:
            self._version = answercontent["micropyVersion"]
        if "id" in answercontent:
            self._id = int(answercontent["id"])
        self._conn = True
        self.save()
        return True
    
    async def run(self):
        ...
    
    def submitRequest(self, request, force = False):
        """
        Submits the request

        Returns the request id
        """
        if not force and not self._conn : 
            raise MicropyInteractionError(ERR_MICROPY_NOT_CONNECTED)
        self._protocolManager.sendRequest(request)
        return request["request-id"]

    async def closeConnection(self):
        """
        Requests the micropy for disconnection.
        """
        if not self._conn : 
            raise MicropyInteractionError(ERR_USER_NOT_CONNECTED)
        request = self._protocolManager.make("close")
        self.submitRequest(request, force = True)
        self._protocolManager.stop()
        await self._protocolManager.waitForEnd()

