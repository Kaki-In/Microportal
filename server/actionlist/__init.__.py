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

from ..exceptions import *
from .action.actions import *
import parsing as _prs

class ActionsList():
    def __init__(self, mlist, ulist, vpol, i18n):
        self._mlist = mlist
        self._ulist = ulist
        self._vpol = vpol
        self._i18n = i18n
        self._actions = {}

    def addAction(self, action):
        self._actions[action.name()] = action
    
    def removeAction(self, action):
        if not action.name() in self._actions:
            raise ActionListError(ERR_ACTION_LIST_NO_SUCH_ACTION, action = repr(action.name()))
        del self._actions[action.name()]
    
    def getActionByName(self, actionname):
        if not actionname in self._actions:
            raise ActionListError(ERR_ACTION_LIST_NO_SUCH_ACTION, action = repr(actionname))
        return self._actions[actionname]
    
    async def execute(self, actionName, user, **args):
        action  = self.getActionByName(actionName)
        return await action(user)
        
        
