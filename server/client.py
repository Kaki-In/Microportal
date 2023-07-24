#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  client.py
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

import socket as _sock
from .pman import *
from .exceptions import *
from .micropylist import *
from .userlist import *
import verbosePolicy as _vpol

class Client():
	"""
	Facade for micropies and users as clients
	"""
	def __init__(self, address, mlist, ulist, vpol):
		self._address = address
		self._client = None
		self._thread = None
		self._mustStop = True
		self._mlist = mlist
		self._ulist = ulist
		self._vpol = vpol
		self._running = False
	
	def start(self, socket, address):
		"""
		Starts the client
		"""
		self._run(socket, address)

	def disconnect(self):
		"""
		Disconnects the client when it's connected
		"""
		self.protocolManager().stop()

	def isRunning(self):
		"""
		Returns True if the client is actually running
		"""
		return self._running

	async def waitForEnd(self):
		"""
		Waits for the client to finish
		"""
		if not self._running :
			raise ClientError(ERR_CLIENT_NOT_RUNNING)
		await self.protocolManager().waitForEnd()
	
	def protocolManager(self):
		if self._client is None:
			raise ClientError(ERR_CLIENT_NOT_CONNECTED)
		return self._client.protocolmanager()
	
	async def _close(self, socket):
		"""
		Internal Method
		Closes connections of the connected client at end
		"""
		try:
			socket.shutdown(_sock.SHUT_RDWR)
		except:
			pass
		a = True
		while a:
			try:
				a = socket.recv(1024)
				continue
			except socket.timeout:
				continue
			except:
				break
		socket.close()
		self._running = False
	
	def client(self):
		return self._client

	async def _run(self, socket, address):
		"""
		Internal Method. Runs the client connection
		"""
		socket.settimeout(5)
		self._running = True
		try:
			file = socket.makefile()
			info = file.readline()
			if info == "connectAsUser\n":
				info2 = file.readline()
				try:
					user = self._ulist.connectSocketWithAccount(socket, int(info2[:-1]))[0]
				except ClientError as exc:
					self._vpol.log(str(exc), self._vpol.LEVEL_FATAL)
					return 
				login = user.login()
				self._vpol.log(self._i18n.getMessage("Connected user {username}", username = login), _vpol.LEVEL_INFO)
				self._client = user
			elif info == "connectAsMicropy\n":
				micropy = self._mlist.connectSocketWithAdress(socket, address[0])[0]
				name = micropy.name()
				if name:
					self._vpol.log(self._i18n.getMessage("Connected micropy {name}", name = name), _vpol.LEVEL_INFO)
				else:
					self._vpol.log(self._i18n.getMessage("Connected a micropy at address {address}", address = address), _vpol.LEVEL_INFO)
				self._client = micropy
			else:
				self._vpol.log(self._i18n.getMessage("A client sent an invalid connection response : {info}", info = repr(info)), _vpol.LEVEL_FATAL)
				return
			await self._client.run()
		finally:
			socket.send(b"!EOF\r\n")
			self._close(socket)

