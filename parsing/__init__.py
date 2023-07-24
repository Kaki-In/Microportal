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

"""
XML parser (by hand)

Example :

 |data = \"\"\"
 |<html>
 |	<head/><body/>
 |</html>
 |\"\"\"
 |result = parse(data)
 |print(result.name(), result.attributes(), result.children())

"""

class DOMObject():
	"""
	Generated or parsed element.
	"""
	def __bytes__(self):
		d = str(self)
		while "\n  " in d:
			d = d.replace("\n  ", "\n")
		return d.replace("\n", "").encode()

	def __init__(self, name, *children, **attrs):
		self._name = name
		self._children = list(children)
		for i in children:
			if i._parent:
				i._parent.removeChild(i)
			i._parent = self
		self._attrs = attrs
		self._parent = None

	def __repr__(self):
		a = "<" + repr(self._name) + " element"
		for i in self._attrs:
			a += " " + i + "=" + repr(self._attrs[i])
		return a + ">"

	def __str__(self):
		a = "<" + self._name
		for i in self._attrs:
			a += " " + i + "=" + repr(self._attrs[i])
		if self._children:
			a += ">"
			for i in self._children:
				a += "\n    "
				a += str(i).replace("\n", "\n    ")
			a += "\n</" + self._name + ">"
		else:
			a += "/>"
		return  a

	def tagName(self):
		"""
		Returns the tag name of the element
		"""
		return self._name

	def children(self):
		"""
		Returns the children of the element
		"""
		return tuple(self._children)

	def addChild(self, child):
		"""
		Adds a child to the element children list
		"""
		self._children.append(child)
		if child._parent:
			child._parent.removeChild(child)
		child._parent = self

	def insertChild(self, child, pos):
		"""
		Inserts a child into the element children list
		"""
		self._children.insert(child, pos)
		if child._parent:
			child._parent.removeChild(child)
		child._parent = self

	def removeChild(self, child):
		"""
		Removes a child from the element children list
		"""
		self._children.remove(child)
		child._parent = None

	def attributes(self):
		"""
		Returns a dict object containing the attributes and their values
		"""
		return self._attrs.copy()

	def getattribute(self, attr):
		"""
		Returns the value of the given attribute
		"""
		return self._attrs[attr]

	def setattribute(self, attr, value):
		"""
		Changes the value of the given attribute
		"""
		self._attrs[attr] = value

	def parent(self):
		"""
		Returns the parent of the element
		"""
		return self._parent

	def __getitem__(self, attr):
		return self._attrs[attr]

	def __setitem__(self, attr, value):
		self._attrs[attr] = value

	def __iter__(self):
		return iter(self._attrs)

def isValidName(name):
	"""
	Returns True if the given name can be used as a tagname or attribute
	name.
	"""
	for i in name:
		if not (i.isalpha() or i.isdigit()):return False
	return True

def split(data):
	"""
	Returns a list containing the different elements openures and
	closures
	"""
	lines = data.split("\n")
	for i in range(len(lines)):
		while lines[i] and lines[i][0] in " \t":
			lines[i] = lines[i][1:]
		while lines[i] and lines[i][-1] in " \t":
			lines[i] = lines[i][:-1]
	while "" in lines:lines.remove("")
	data = ""
	for i in lines:
		if not i[0] in "</":data += " "
		data += i
	data = data.replace("><", ">\n<").split("\n")
	return data

def parse(data):
	"""
	Returns a parsed object containing the elements in the parsed string
	"""
	datalist = split(data)
	elembase = DOMObject("#!parsed!#")
	elemused = elembase
	for i in datalist:
		if   i[0] != "<" or i[-1] != ">":
			raise SyntaxError(i)
		elif i[1] == "/":
			elemname = i[2:-1]
			if not isValidName(elemname) or elemused is None or elemused.tagName() != elemname:
				raise SyntaxError(i)
			elemused = elemused.parent()
		else:
			elemdivision = i[1:-1].split(" ")
			name = elemdivision[0]
			if not isValidName(name):
				raise SyntaxError(i)
			elem = DOMObject(name)
			elemused.addChild(elem)
			elemused = elem
			keepelem = True
			if elemdivision[-1][-1] == "/":
				elemdivision[-1] = elemdivision[-1][:-1]
				keepelem = False
			for d in elemdivision[1:]:
				if "=" in d:
					attrname = d[:d.index("=")]
					attrval = d[d.index("=") + 1:]
					if not isValidName(attrname):
						raise SyntaxError(d, i)
					try:
						elemused[attrname] = eval(attrval)
					except Exception as exc:
						raise SyntaxError(attrval, exc, i)
				elif isValidName(d):
					elemused[d] = None
				else:
					raise SyntaxError(i)
			if not keepelem:
				elemused = elemused.parent()
	if elemused is not elembase:
		raise SyntaxError("")
	return elembase
