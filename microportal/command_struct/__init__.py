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

from .instruction_item import *

class PortalCommand():
	def __init__(self, *items):
		self._items = items

	def __iter__(self):
		return iter(self._items)

	def __bytes__(self):
		b = b""
		for i in self._items:
			if b : b += ";"
			b += bytes(i)

		return b
