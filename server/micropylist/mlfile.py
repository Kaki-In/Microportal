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

from shelve import open as _shvopen
from .micropy import *
from ..exceptions import *
from . import *
import os as _os

class MicropyListFile():
    """
    File saving and retrieving the micropies list
    """
    def __init__(self, path):
        self._path = path
        if not _os.path.exists(self._path):
            try:
                _os.makedirs(_os.path.dirname(self._path))
            except OSError as ose:
                raise ListFileSaveError(ose.errno)
            self.saveFileContent({"address" : {}, "passwords" : {}, "names" : {}, "types" : {}, "idnum" : 0, "ids" : []})

    def getMicropyList(self):
        a = self.getFileContent()
        MList = MicropyList(self, a["idnum"])
        for id in a["ids"]:
            address = a["address"][id]
            password = a["passwords"][id]
            name = a["names"][id]
            type = a["types"][id]
            MList._micropies.appened(Micropy(id, address, password, name, type, MList))
        return MList

    def getFileContent(self):
        try:
            a = _shvopen(self._path)
            d = {}
            for i in a:
                d[i] = a[i]
            a.close()
            return d
        except OSError as ose:
            raise ListFileSaveError(ose.errno)
    
    def saveFileContent(self, *contentDict):
        try:
            a = _shvopen(self._path)
            for i in contentDict:
                a[i] = contentDict[i]
            a.close()
        except OSError as ose:
            raise ListFileSaveError(ose.errno)

    def saveMicropyList(self, micropylist):
        address = {}
        passwords = {}
        names = {}
        types = {}
        ids = []
        for i in micropylist.knownMicropies():
            id = i.identificator()
            address[id] = i.address()
            passwords[id] = i.password()
            names[id] = i.name()
            types[id] = i.type()
            ids.append(id)
        idlevel = micropylist.idLevel()
        self.saveFileContent(address = address, passwords = passwords, names = names, types = types, idnum = idlevel, ids = ids)
        
