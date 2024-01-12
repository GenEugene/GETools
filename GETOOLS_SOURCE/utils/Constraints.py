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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene

import maya.cmds as cmds

from ..utils import Selector

from ..values import Enums

def ConstrainSelectedToLastObject(reverse=False, maintainOffset=True, parent=True, point=False, orient=False, scale=False, aim=False, weight=1):
	selected = Selector.MultipleObjects(2)
	if (selected == None):
		return
	ConstrainListToLastElement(reverse, selected, maintainOffset, parent, point, orient, scale, aim, weight)

def ConstrainListToLastElement(reverse=False, selected=None, maintainOffset=True, parent=True, point=False, orient=False, scale=False, aim=False, weight=1):
	if (selected == None):
		cmds.warning("### WARNING ### selected = None")
		return
	
	for i in range(len(selected)):
		if (i == len(selected) - 1):
			break
		
		if (reverse):
			index1 = i
			index2 = -1
		else:
			index1 = -1
			index2 = i
		
		ConstrainSecondToFirstObject(selected[index1], selected[index2], maintainOffset, parent, point, orient, scale, aim, weight = weight)

def ConstrainSecondToFirstObject(objectParent, objectChild, maintainOffset=True, parent=True, point=False, orient=False, scale=False, aim=False, weight=1):
	if parent:
		try:
			cmds.parentConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight)
		except:
			print("||||| Can't create parentConstraint on {0}".format(objectChild))
	else:
		if point:
			try:
				cmds.pointConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight)
			except:
				print("||||| Can't create pointConstraint on {0}".format(objectChild))
		
		if orient:
			try:
				cmds.orientConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight)
			except:
				print("||||| Can't create orientConstraint on {0}".format(objectChild))

	if scale:
		try:
			# cmds.cutKey(objectChild, attribute = ("scaleX", "scaleY", "scaleZ"), clear = True, option = "keys")
			cmds.scaleConstraint(objectParent, objectChild, maintainOffset = maintainOffset) # weight = weight
		except:
			print("||||| Can't create scaleConstraint on {0}".format(objectChild))
	
	if aim:
		ConstrainAim(objectParent, objectChild, maintainOffset, weight) # TODO add customization logic

def ConstrainAim(objectParent, objectChild, maintainOffset = True, weight = 1, aimVector = (0, 0, 1), upVector = (0, 1, 0), worldUpVector = (0, 1, 0), worldUpObject = None): # TODO complete aim logic
	# "scene" "object" "objectrotation" "vector" "none"
	if (worldUpObject == None):
		cmds.aimConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight, aimVector = aimVector, upVector = upVector, worldUpType = "vector", worldUpVector = worldUpVector)
	else:
		cmds.aimConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight, aimVector = aimVector, upVector = upVector, worldUpType = "objectrotation", worldUpVector = worldUpVector, worldUpObject = worldUpObject)

def DeleteConstraints(selected):
	# First pass
	connections = Selector.GetConnectionsOfType(selected, type = Enums.Types.constraint, source = True, destination = False)
	for item in connections:
		if (item == None):
			continue
		for connection in item:
			if (cmds.objExists(connection) == False):
				continue
			for constraint in Enums.Constraints.list:
				if constraint in connection:
					cmds.delete(connection)

	# Second pass with checking child objects (if constraint exists but not connected)
	children = Selector.GetChildrenOfType(selected, type = Enums.Types.constraint)
	for i in range(len(selected)):
		if (children[i] != None):
			for child in children[i]:
				cmds.delete(child)
def DeleteConstraintsOnSelected(*args):
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	DeleteConstraints(selectedList)

def DisconnectTargetsFromConstraint(selected):
	connections = Selector.GetConnectionsOfType(selected, type = Enums.Types.constraint, source = True, destination = False)
	
	if (connections[-1] == None):
		cmds.warning("No constraints detected inside the last selected object")
		return
	
	# 1. Maya function, no documentation
	cmds.select(selected, replace = True)
	cmds.RemoveConstraintTarget(selected[-1], selected[:-1])
	
	# 2. Custom
	# for connection in connections[-1]:
	# 	for item in selected[:-1]:
	# 		if (cmds.objExists(connection) == False):
	# 				continue

	# 		if Enums.Constraints.parentConstraint in connection:
	# 			targets = cmds.parentConstraint(connection, query = True, targetList = True)
	# 			if (item in targets):
	# 				cmds.parentConstraint(item, selected[-1], edit = True, remove = True)
			
	# 		elif Enums.Constraints.pointConstraint in connection:
	# 			targets = cmds.pointConstraint(connection, query = True, targetList = True)
	# 			if (item in targets):
	# 				cmds.pointConstraint(item, selected[-1], edit = True, remove = True)
			
	# 		elif Enums.Constraints.orientConstraint in connection:
	# 			targets = cmds.orientConstraint(connection, query = True, targetList = True)
	# 			if (item in targets):
	# 				cmds.orientConstraint(item, selected[-1], edit = True, remove = True)
			
	# 		elif Enums.Constraints.scaleConstraint in connection:
	# 			targets = cmds.scaleConstraint(connection, query = True, targetList = True)
	# 			if (item in targets):
	# 				cmds.scaleConstraint(item, selected[-1], edit = True, remove = True)
			
	# 		elif Enums.Constraints.aimConstraint in connection:
	# 			targets = cmds.aimConstraint(connection, query = True, targetList = True)
	# 			if (item in targets):
	# 				cmds.aimConstraint(item, selected[-1], edit = True, remove = True)
	pass
def DisconnectTargetsFromConstraintOnSelected(*args):
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	DisconnectTargetsFromConstraint(selectedList)
