# GETOOLS is under the terms of the MIT License
# Copyright (c) 2018-2024 Eugene Gataulin (GenEugene). All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds

from ..values import Enums

def MultipleObjects(minimalCount=1, transformsOnly=True, shapes=False):
	# Save selected objects to variable
	if (transformsOnly):
		selectedList = cmds.ls(selection = True, type = Enums.Types.transform, shapes = shapes)
	else:
		selectedList = cmds.ls(selection = True, shapes = shapes)

	# Check selected objects
	if (len(selectedList) < minimalCount):
		if (minimalCount == 1):
			ending = ""
		else:
			ending = "s"
		cmds.warning("You need to select at least {0} object{1}".format(minimalCount, ending))
		return None
	else:
		return selectedList

def SelectHierarchy(*args):
	cmds.SelectHierarchy()

def SelectHierarchyTransforms(*args):
	selected = MultipleObjects()
	if (selected == None):
		return None

	cmds.select(hierarchy = True)
	list = cmds.ls(selection = True, type = Enums.Types.transform, shapes = False)
	cmds.select(clear = True)
	
	for i in range(len(list)):
		cmds.select(list[i], add = True)
	
	return list

def PrintSelected(*args):
	selected = MultipleObjects(transformsOnly = False)
	if (selected == None):
		return

	print("\nSelected Objects Printed Below: {0}".format(len(selected)))
	print("-------------------------------")
	for item in selected:
		print(item)
	print("")

def GetChildrenOfType(selected, type=""):
	result = []
	for item in selected:
		if (cmds.objExists(item)):
			result.append(cmds.listRelatives(item, type = type))
		else:
			result.append(None)
	return result

def GetConnectionsOfType(selected, type="", source=True, destination=True):
	result = []
	for item in selected:
		if (cmds.objExists(item)):
			result.append(cmds.listConnections(item, type = type, source = source, destination = destination))
		else:
			result.append(None)
	return result

def GetChannelBoxAttributes(*args):
	selected = cmds.channelBox("mainChannelBox", query = True, selectedMainAttributes = True) # selectedHistoryAttributes # selectedMainAttributes # selectedOutputAttributes # selectedShapeAttributes
	return selected

