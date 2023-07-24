#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  micropylist.py
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

"""
Exceptions of the project
"""

import sys as _sys
from .i18n import *
import verbosePolicy as _vpol

ERR_REQUEST_INVALID = 300
ERR_REQUEST_NOT_FOUND = 301

ERR_MICROPY_NOT_VALID_MICROPY_ANSWER = 300
ERR_MICROPY_NOT_CONNECTED = 400
ERR_MICROPY_ALREADY_CONNECTED = 401

ERR_USER_NOT_VALID_USER_ANSWER = 300
ERR_USER_NOT_CONNECTED = 400
ERR_USER_ALREADY_CONNECTED = 401

ERR_PROTOCOL_MANAGER_NOT_STARTED = 500
ERR_PROTOCOL_MANAGER_NOT_STOPPING = 501
ERR_PROTOCOL_MANAGER_INVALID_REQUEST_STRUCT = 302

ERR_MICROPY_LIST_NOT_SUCH_MICROPY = 404

ERR_USER_NOT_VALID_MICROPY_ANSWER = 300

ERR_USER_LIST_NO_SUCH_USER = 404

ERR_CLIENT_NOT_RUNNING = 402
ERR_CLIENT_NOT_CONNECTED = 403
ERR_CLIENT_NOT_STOPPING = 404

ERR_SERVER_NO_SUCH_CLIENT = 300
ERR_SERVER_NOT_RUNNING = 301
ERR_SERVER_NOT_STOPPING = 302

ERR_ACTION_ARGUMENT_INVALID = 301
ERR_ACTION_ARGUMENT_MISSING = 302
ERR_ACTION_INVALID_ANSWER = 501

ERR_ACTION_LIST_NO_SUCH_ACTION = 404

verbosePolicy = _vpol.VerbosePolicy(True, True, True, True, True)
translator = i18nTranslator(vpol = verbosePolicy)

class _microportalError(Exception):
    def __init__(self, errnum, **args):
        self._num = errnum
        message = self.getMessage()
        self._args = args
        if not message:
            verbosePolicy.log(translator.getMessage("Warning : an invalid error number has been given to a ".format(type(self).__name__), level = _vpol.LEVEL_WARN))
        super().__init__(translator.getMessage(message, **args))
    
    def getMessage(self):
        return str()

    def errorNumber(self):
        return self._num

class RequestError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_REQUEST_INVALID:
            return "invalid request"
        if   self._num == ERR_REQUEST_NOT_FOUND:
            return "no such request"

class MicropyInteractionError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_MICROPY_NOT_CONNECTED:
            return "micropy actually not connected"
        elif self._num == ERR_MICROPY_ALREADY_CONNECTED:
            return "micropy already connected"
        elif self._num == ERR_MICROPY_NOT_VALID_MICROPY_ANSWER:
            return "invalid micropy response ; is it really a micropy?"

class UserInteractionError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_USER_NOT_CONNECTED:
            return "user actually not connected"
        elif self._num == ERR_USER_ALREADY_CONNECTED:
            return "user already connected"
        elif self._num == ERR_USER_NOT_VALID_MICROPY_ANSWER:
            return "invalid user response ; is it really an user?"

class ProtocolManageError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_PROTOCOL_MANAGER_NOT_STARTED:
            return "the protocol manager has not been started yet"
        elif self._num == ERR_PROTOCOL_MANAGER_NOT_STOPPING:
            return "the protocol manager isn't stopping"
        elif self._num == ERR_PROTOCOL_MANAGER_INVALID_REQUEST_STRUCT:
            return "invalid request struct"
    
class ListFileSaveError(_microportalError):
    def getMessage(self):
        return ""

class MicropyListError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_MICROPY_LIST_NOT_SUCH_MICROPY:
            return "no such micropy"

class UserListError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_USER_LIST_NO_SUCH_USER:
            return "no such user"

class ClientError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_CLIENT_NOT_CONNECTED:
            return "not connected client"
        elif self._num == ERR_CLIENT_NOT_STOPPING:
            return "client not stopping"

class ServerError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_SERVER_NO_SUCH_CLIENT:
            return "no such client"

class ActionExecutionError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_ACTION_ARGUMENT_INVALID:
            return "invalid argument {argname}"
        elif self._num == ERR_ACTION_ARGUMENT_MISSING:
            return "missing argument {argname}"
        elif self._num == ERR_ACTION_INVALID_ANSWER:
            return "invalid answer"

class ActionListError(_microportalError):
    def getMessage(self):
        if   self._num == ERR_ACTION_LIST_NO_SUCH_ACTION:
            return "no such action {}"
