#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  __init__.py
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
from threading import Thread as _thr
from .userlist import *
from .client import *
import time as _time
import verbosePolicy as _vpol
from .exceptions import *
from .i18n import *

class Server():
	"""
	The main server.

	Server(addr = "localhost", port = "8266", micropylist = None):

	 | addr : the address to bind with
	 | port : the port to bind with
	 | micropylist : the list of known micropies (see micropylist)
	 | vpol : the log manager of the server (see verbosePolicy)

	"""
	def __init__(self, addr = "localhost", port = 8266, micropylist = None, vpol = None):
		self._host = (addr, port)
		self._running = False
		self._mustStop = True
		self._clients = []
		self._micropylist = micropylist or MicropyList(vpol)
		self._thread = None
		self._vpol = vpol
		self._translator = i18nTranslator(self._vpol)

	def removeClient(self, client):
		"""
		Removes the given <client> from the clients list
		"""
		if not client in self._clients:
			raise ServerError(ERR_SERVER_NO_SUCH_CLIENT)
		client.disconnect()
		self._clients.remove(client)

	def _createSocket(self):
		self._socket = _sock.socket()
		self._socket.bind(self._host)
		self._socket.listen(5)
		self._socket.settimeout(10)

	def stop(self):
		"""
		Stops the server when it's running
		"""
		self._mustStop = True

	def waitForEnd(self):
		"""
		Waits for the server to finish
		"""
		if not self._running :
			raise ServerError(ERR_SERVER_NOT_RUNNING)
		if not self._mustStop:
			raise ServerError(ERR_SERVER_NOT_STOPPING)
		self._thread.join()

	def isRunning(self):
		"""
		Returns True if the server is actually running
		"""
		return self._running

	def start(self):
		"""
		Starts the server
		"""
		self._mustStop = False
		self._thread = _thr(target = self._run)
		self._thread.start()

	def _run(self):
		if self._mustStop or self._running : return
		self._running = True
		try:
			self._createSocket()
			while not self._mustStop:
				try:
					client, address = self._socket.accept()
					cli = Client(address, self._micropylis, self._vpol)
					self._clients.append(cli)
					cli.start(client)
				except _sock.timeout: _time.sleep(1)
				except Exception as exc:
					self._vpol.log(self._i18n.getMessage("an error occured..."), _vpol.LEVEL_FATAL)
					self._vpol.log(type(exc).__name__, _vpol.LEVEL_FATAL)
					self._vpol.log(str(exc), _vpol.LEVEL_FATAL)
					self.stop()
				finally:
					for i in self._clients.copy():
						if not i.isConnected():
							self._clients.remove(i)
		finally:
			self._close()
	
	def _close(self):
		try:self._socket.shutdown(_sock.SHUT_RDWR)
		except:pass
		for i in self._clients:
			try:i.disconnect()
			except Exception as exc:
				self._vpol.log(self._i18n.getMessage("an exception occured while closing connections"))
		a = True
		while a:
			try:a = self._socket.recv(1024)
			except:break
		self._socket.close()
		self._running = False

