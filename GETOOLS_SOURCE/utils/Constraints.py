# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Selector

from GETOOLS_SOURCE.values import Enums

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
			if Enums.Constraints.parentConstraint\
			or Enums.Constraints.pointConstraint\
			or Enums.Constraints.orientConstraint\
			or Enums.Constraints.scaleConstraint\
			or Enums.Constraints.aimConstraint in connection:
				cmds.delete(connection)

	# Second pass with checking child objects (if constraint exists but not connected)
	children = Selector.GetChildrenOfType(selected, type = Enums.Types.constraint)
	for i in range(len(selected)):
		if (children[i] != None):
			for child in children[i]:
				cmds.delete(child)

def DeleteElementFromConstraint(selected): # TODO
	# constraints = Selector.GetChildrenOfType(selected, type = Enums.Types.constraint)
	# connections = Selector.GetConnectionsOfType(selected, type = Enums.Types.constraint, source = True, destination = False)

	# if (constraints[-1] == None):
	# 	cmds.warning("No constraints inside last selected object")
	# 	return

	# for constraint in constraints[-1]:
	# 	print(constraint)

		# if (constraint == None):
		# 	continue
		# for child in constraint:
		# 	cmds.pointConstraint(child, selected[-1], edit = True, remove = True)
		# 	print("child = {0}, last = {1}".format(child, selected[-1]))

	#name = "objCenterOfMass_pointConstraint1"
	#targets = cmds.pointConstraint(name, query=True, targetList=True)
	#print(targets)

	# cmds.pointConstraint("pCube1", "objCenterOfMass", edit = True, remove = True)

	pass

