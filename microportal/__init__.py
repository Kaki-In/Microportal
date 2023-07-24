#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2023 Kaki In <kaki@kick-peppy>
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

import socket as _socket
from .command_struct import *

class PortalCommandEmission():
	def __init__(self, command, host, port = 8626):
		self._command = command
		self._host = (host, port)

	def _connect(self):
		self._socket = _socket.socket()
		self._socket.settimeout(5)
		self._socket.connect(self._host)

	def emit(self):
		self._connect()
		self._socket.send(bytes(self._command))
		result = b""
		a = True
		while a:
			a = self._socket.recv(1024)
			result += a
		self._close()
		return result

	def _close(self):
		a = True
		while a:
			a = self._socket.recv(1024)
		self._socket.close()
