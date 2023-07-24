#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  userlist.py
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
from PIL import Image as _pilimg
import math as _mh
import random as _rd

class User():
    """
    An user

    User():
     -> instantiate a blank user (automatically used, please don't do it yourself)
    """
    def __init__(self, id, mail, password = None, login = None, image = None, ulist = None, mlist = None, vpol = None, i18n = None):
        self._mail = mail
        self._password = password
        self._login = login
        if type(image) is bytes:
            dim = int(_mh.sqrt(len(image) / 3))
            if len(image) == dim ** 2 * 3:
                image = _pilimg.frombytes("RGB", (dim, dim), image).resize((1200, 1200))
            else:
                image = None
        else:
            image = None
        self._image = image or self.generateImage()
        self._conn = False
        self._socket = None
        self._protocolManager = None
        self._version = None
        self._ulist = ulist
        self._mlist = mlist
        self._id = id
        self._vpol = vpol
        self._i18n = i18n
    
    def setImage(self, image):
        """
        Sets the image of the user
        """
        dim = int(_mh.sqrt(len(image) / 3))
        if len(image) == dim ** 2 * 3:
            image = _pilimg.frombytes(_pilimg.RGB, (dim, dim), image).resize((1200, 1200))
        else:
            image = self.generateImage()
        self._image = image
        self.save()
    
    def save(self):
        """
        Saves the user in the file of the userList
        """
        if self._ulist is not None:
            self._ulist.save()
        
    def generateImage(self):
        """
        Internal Method
        Generates and returns an image for the user
        """
        b = ""
        l = [[[0] * 3 for _ in range(5)] for _ in range(5)]
        color = _rd.choice([(85 * (i % 4), 85 * (i//2 % 4), 85 * (i//4 % 4)) for i in range(1, 63)])
        backcolor = _rd.choice(((0, 0, 0), (255, 255, 255)))
        for y in range(5):
            line = ""
            for x in range(5):
                n = _rd.randrange(2)
                part = ""
                for k in range(3):
                    if x <= 2:
                        if n:
                            intens = color [k]
                            intens = color [k]
                        else:
                            intens = backcolor [k]
                            intens = backcolor [k]
                    else:
                        intens = l[4 - x][y][k]
                    l[x][y][k] = intens
                    part += chr(intens)
                line += part * 240
            b += line * 240
        image = _pilimg.frombytes("RGB", (1200, 1200), b.encode("latin1"))
        return image
    
    def identificator(self):
        """
        Returns the user identificator
        """
        return self._id

    def version(self):
        """
        Returns the version of the user
        """
        return self._version

    def login(self):
        """
        Returns the name of the user
        """
        return self._name

    def image(self):
        """
        Returns the image of the user
        """
        return self._image

    def mailAddress(self):
        """
        Returns the address of the user
        """
        return self._mail

    def password(self):
        """
        Returns the password of the user
        """
        return self._password

    def isConnected(self):
        """
        Returns the connection status (True if connected, False else)
        """
        return self._conn

    def protocolManager(self):
        """
        Returns the ProtocolManager which must be used to interact with the user
        """
        if not self._conn : 
            raise UserInteractionError(ERR_USER_NOT_CONNECTED)
        return self._protocolManager

    async def connectToSocket(self, socket):
        """
        Links the user with the given socket
        """
        if self._conn : 
            raise UserInteractionError(ERR_USER_ALREADY_CONNECTED)
        self._socket = socket
        self._socket.send("RUIr\r\nQUIT\r\n")
        a = self._socket.recv(1024)
        if a!="IAmIr\r\n" : 
            self._socket.close()
            raise UserInteractionError(ERR_USER_NOT_VALID_USER_ANSWER)
        self._protocolManager = ProtocolManager(self._socket, self._vpol, self._i18n)
        if self._password is None:
            request = self._protocolManager.make("ping")
            requestid = self.submitRequest(request, force = True)
            answer = await self._protocolManager.waitForRequest(requestid)
            answertype, answercontent = self._protocolManager.getRequestInformations(answer)
            if answertype != "pong" or (self._password and (not "password" in answercontent or answercontent["password"] != self._password)):
                self.closeConnection()
                raise UserInteractionError(ERR_USER_NOT_VALID_USER_ANSWER)
        else:
            password = self.generatePassword()
            request = self._protocolManager.make("create", password = password, id = self._id)
            requestid = self.submitRequest(request, force = True)
            answer = await self._protocolManager.waitForRequest(requestid)
            answertype, answercontent = self._protocolManager.getRequestInformations(answer)
            if answertype != "confirm-creation":
                self.closeConnection()
                raise UserInteractionError(ERR_USER_NOT_VALID_USER_ANSWER)
            self._password = password
        if "userLogin" in answercontent:
            self._name = answercontent["userLogin"]
        if "userImage" in answercontent:
            self._image = answercontent["userImage"]
        if "userVersion" in answercontent:
            self._version = answercontent["userVersion"]
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
            raise UserInteractionError(ERR_USER_NOT_CONNECTED)
        self._protocolManager.sendRequest(request)
        return request["request-id"]

    async def closeConnection(self):
        """
        Requests the user for disconnection.
        """
        if not self._conn : 
            raise UserInteractionError(ERR_USER_NOT_CONNECTED)
        request = self._protocolManager.make("close")
        self.submitRequest(request, force = True)
        self._protocolManager.stop()
        await self._protocolManager.waitForEnd()

