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

from .ulfile import *
from .user import *
from ..exceptions import *

"""
Client list of the server.
"""

class UserList():
	"""
	Micropy list  : 
		| ulist (internal, please don't use) : the users list file that generated the users list
	"""
	def __init__(self, ulist = None, idlevel = 0):
		self._file = ulist
		self._users = []
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
			self._file.saveUsersList(self)
	
	def knownUsers(self):
		"""
		Returns the list of the known users (tuple)
		"""
		return tuple(self._users)

	def removeUsers(self, id):
		"""
		Removes the user with the identificator <id> from the list
		"""
		for i in self._users:
			if i.identificator() is id:
				if i.isConnected():
					i.closeConnection()
				self._users.remove(i)
		self.save()
	
	def addUser(self, name, password, mail):
		"""
		Adds the user at mail-address <mail> to the users list
		"""
		self._idlevel += 1
		self._users.append(User(self._idlevel, name = name, password = password, mail = mail))
		self.save()
	
	def connectSocketWithAccount(self, socket, accid):
		"""
		Connects the socket located with the address to the user instance
		"""
		user = self.getUserFromIdentificator(accid)
		if not user:
			raise UserListError(ERR_USER_LIST_NO_SUCH_USER)
		return user, user.connectToSocket(socket)
	
	def getUserFromId(self, id):
		"""
		Returns the user with the given id
		"""
		for i in self._users:
			if i.identificator() == id:
				return i
		raise UserListError(ERR_USER_LIST_NO_SUCH_USER)

	def getUserFromMail(self, mail):
		"""
		Returns the user with the given address
		"""
		for i in self._users:
			if i.address() == mail:
				return i
		raise UserListError(ERR_USER_LIST_NO_SUCH_USER)

	def getUsersFromLogin(self, login):
		"""
		Returns the users with the given login
		"""
		l = []
		for i in self._users:
			if i.login() == login:
				l.append(i)
		return l
