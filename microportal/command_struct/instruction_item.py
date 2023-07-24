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

CMD_SP = 0
CMD_GP = 1
CMD_SLK = 2
CMD_WuRU = 3
CMD_WatRU = 4

class PortalInstructionItem():
	def __init__(self, cmdtype, *args):
		self._args = args
		self._type = cmdtype

	def commandName(self):
		return ("SP", "GP", "SLK", "WuRU", "WatRU")[self._type]

	def args(self):
		return self._args

	def __repr__(self):
		return "<PortalInstruction({}) object at {}>".format(self.commandName(), hex(id(self)))

	def __bytes__(self):
		b = self.commandName().encode()
		for i in self._args:
			if type(i) is int:
				a = str(i).encode()
			elif type(i) is str:
				a = i.encode()
			elif type(i) is bool:
				a = (b"false", b"true") [i]
			elif type(i) is bytes:
				a = i
			else:
				raise TypeError("{} type not handled".format(repr(type(i).__name__)))
			b += b" " + a

		return b


