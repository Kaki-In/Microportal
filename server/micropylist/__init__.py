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

from .mlfile import *
from .micropy import *
from ..exceptions import *

"""
Micropy list of the server.
"""

class MicropyList():
	"""
	Micropy list  : 
		| mlist (internal, please don't use) : the micropy list file that generated the micropy list
	"""
	def __init__(self, mlist = None, idlevel = 0):
		self._file = mlist
		self._micropies = []
		self._idlevel = idlevel
	
	def idLevel(self):
		"""
		The number of the next identificating micropy
		"""
		return self._idlevel
	
	def save(self):
		"""
		Saves the list into the file
		"""
		if self._file is not None:
			self._file.saveMicropyList(self)
	
	def knownMicropies(self):
		"""
		Returns the list of the known micropies (tuple)
		"""
		return tuple(self._micropies)

	def removeMicropy(self, id):
		"""
		Removes the micropy with the identificator <id> from the list
		"""
		for i in self._micropies:
			if i.identificator() is id:
				if i.isConnected():
					i.closeConnection()
				self._micropies.remove(i)
		self.save()
	
	def addMicropy(self, addr):
		"""
		Adds the micropy at address <addr> to the micropy list
		"""
		self._idlevel += 1
		self._micropies.append(Micropy(self._idlevel, addr))
		self.save()
	
	def connectSocketWithAdress(self, socket, address):
		"""
		Connect the socket located with the address to the micropy instance
		"""
		micropy = self.getMicropyFromAddress(addr)
		if not maddr:
			micropy = self.addMicropy(addr)
		return micropy, micropy.connectToSocket(socket)
	
	def getMicropyFromId(self, id):
		"""
		Returns the micropy with the given id
		"""
		for i in self._micropies:
			if i.identificator() == id:
				return i
		raise MicropyListError(ERR_MICROPY_LIST_NOT_SUCH_MICROPY)

	def getMicropyFromAddress(self, addr):
		"""
		Returns the micropy with the given address
		"""
		for i in self._micropies:
			if i.address() == addr:
				return i
		raise MicropyListError(ERR_MICROPY_LIST_NOT_SUCH_MICROPY)

	def getMicropiesFromName(self, name):
		"""
		Returns the micropies with the given name
		"""
		l = []
		for i in self._micropies:
			if i.name() == name:
				l.append(i)
		return l

	def getMicropiesFromType(self, typename):
		"""
		Returns the micropies with the given type
		"""
		l = []
		for i in self._micropies:
			if i.type() == typename:
				l.append(i)
		return l

