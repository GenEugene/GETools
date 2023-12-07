# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

# from GETOOLS_SOURCE.utils import Locators
from GETOOLS_SOURCE.utils import Selector

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

