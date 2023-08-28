#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2023 Kaki In <91763754+Kaki-In@users.noreply.github.com>
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

import sys as _sys
import inspect as _insp
import types as _types
import os as _os
from termcolor import colored as _colored

class VerbosePolicy():
	LEVEL_TRACE   = 0
	LEVEL_DEBUG   = 1
	LEVEL_INFO    = 2
	LEVEL_WARNING = 3
	LEVEL_ERROR   = 4
	LEVEL_FATAL   = 5

	def __init__(self, trace = False, debug = False, info = False, warning = False, error = False, fatal = False, output = _sys.stdout):
		self._enableLogs = (trace, debug, info, warning, error, fatal)
		self._output = output
	
	def close(self):
		self._output.close()

	def getConstName(self, const):
		match const:
			case self.LEVEL_TRACE :
				return "TRACE"
			case self.LEVEL_DEBUG :
				return "DEBUG"
			case self.LEVEL_INFO  :
				return "INFO"
			case self.LEVEL_WARNING  :
				return "WARNING"
			case self.LEVEL_ERROR :
				return "ERROR"
			case self.LEVEL_FATAL :
				return "FATAL"
			case _:
				raise ValueError("unknown info level")

	def getConstColor(self, const):
		match const:
			case self.LEVEL_TRACE :
				return "magenta"
			case self.LEVEL_DEBUG :
				return "blue"
			case self.LEVEL_INFO  :
				return "green"
			case self.LEVEL_WARNING :
				return "light_yellow"
			case self.LEVEL_ERROR :
				return "yellow"
			case self.LEVEL_FATAL :
				return "red"
			case _:
				raise ValueError("unknown info level")

	def log(self, *message, infolevel = LEVEL_INFO):
		if not self._enableLogs[infolevel] : return
		frame = _insp.getouterframes(_insp.currentframe(), 2) [2]

		logname = self.getConstName(infolevel)

		while len(logname) < 10:
			logname = " " + logname if len(logname) % 2 == 0 else logname + " "
   
		print("[" + _colored(logname, self.getConstColor(infolevel), attrs = ("bold",), force_color=True) + "]", "[" + str(_os.path.abspath(frame.filename)) + ":" + str(frame.function) + ":" + str(frame.lineno) + "]", *message, file = self._output, flush = True)
