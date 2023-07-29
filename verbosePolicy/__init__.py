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

import sys as _sys
import inspect as _insp
import types as _types
import os as _os
from termcolor import colored as _colored

LEVEL_TRACE = 0
LEVEL_DEBUG = 1
LEVEL_INFO  = 2
LEVEL_WARNING  = 3
LEVEL_ERROR = 4
LEVEL_FATAL = 5

_consts = _types.SimpleNamespace()
_consts.LEVEL_TRACE = LEVEL_TRACE
_consts.LEVEL_DEBUG = LEVEL_DEBUG
_consts.LEVEL_INFO  = LEVEL_INFO
_consts.LEVEL_WARN  = LEVEL_WARNING
_consts.LEVEL_ERROR = LEVEL_ERROR
_consts.LEVEL_FATAL = LEVEL_FATAL


class VerbosePolicy():
	def __init__(self, trace = False, debug = False, info = False, warning = False, error = False, fatal = False, output = _sys.stdout):
		self._enableLogs = (trace, debug, info, warning, error, fatal)
		self._output = output

	def getConstName(self, const):
		match const:
			case _consts.LEVEL_TRACE :
				return "TRACE"
			case _consts.LEVEL_DEBUG :
				return "DEBUG"
			case _consts.LEVEL_INFO  :
				return "INFO"
			case _consts.LEVEL_WARN  :
				return "WARNING"
			case _consts.LEVEL_ERROR :
				return "ERROR"
			case _consts.LEVEL_FATAL :
				return "FATAL"
			case _:
				raise ValueError("unknown info level")

	def getConstColor(self, const):
		match const:
			case _consts.LEVEL_TRACE :
				return "magenta"
			case _consts.LEVEL_DEBUG :
				return "blue"
			case _consts.LEVEL_INFO  :
				return "green"
			case _consts.LEVEL_WARN  :
				return "light_yellow"
			case _consts.LEVEL_ERROR :
				return "yellow"
			case _consts.LEVEL_FATAL :
				return "red"
			case _:
				raise ValueError("unknown info level")

	def log(self, *message, infolevel = LEVEL_INFO):
		if not self._enableLogs[infolevel] : return
		frame = _insp.getouterframes(_insp.currentframe(), 2) [1]

		logname = self.getConstName(infolevel)

		while len(logname) < 10:
			logname = " " + logname if len(logname) % 2 == 0 else logname + " "

		print("[" + _colored(logname, self.getConstColor(infolevel), attrs = ("bold",)) + "]", "[" + str(_os.path.abspath(frame.filename)) + ":" + str(frame.function) + ":" + str(frame.lineno) + "]", *message, file = self._output, flush = True)
