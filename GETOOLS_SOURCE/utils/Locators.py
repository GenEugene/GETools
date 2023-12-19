# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Animation
from GETOOLS_SOURCE.utils import Baker
from GETOOLS_SOURCE.utils import Constraints
from GETOOLS_SOURCE.utils import Parent
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Text

from GETOOLS_SOURCE.values import Enums

# TODO think how to merge the same logic on each function. Looks like a lot of similar parts of code

nameBase = "gLoc"
nameMatched = "{0}Matched".format(nameBase)
nameConstrained = "{0}Constrained".format(nameBase)
nameBaked = "{0}Baked".format(nameBase)
nameReverse = "{0}Reverse".format(nameBase)
nameAim = "{0}Aim".format(nameBase)
scale = 1.0

def GetSize(locator):
	return (
	cmds.getAttr(locator + Enums.Types.shape + "." + Enums.Attributes.scaleLocal[0]),
	cmds.getAttr(locator + Enums.Types.shape + "." + Enums.Attributes.scaleLocal[1]),
	cmds.getAttr(locator + Enums.Types.shape + "." + Enums.Attributes.scaleLocal[2]))
def SetSize(locator, valueX, valueY, valueZ):
	if (valueX == 0 or valueY == 0 or valueZ == 0):
		cmds.warning("Target locator scale is ZERO. The lLocator scaler may have problems.")
	cmds.setAttr(locator + Enums.Types.shape + "." + Enums.Attributes.scaleLocal[0], valueX)
	cmds.setAttr(locator + Enums.Types.shape + "." + Enums.Attributes.scaleLocal[1], valueY)
	cmds.setAttr(locator + Enums.Types.shape + "." + Enums.Attributes.scaleLocal[2], valueZ)
def ScaleSize(locator, valueX, valueY, valueZ):
	size = GetSize(locator)
	sizeX = size[0] * valueX
	sizeY = size[1] * valueY
	sizeZ = size[2] * valueZ
	SetSize(locator, sizeX, sizeY, sizeZ)

def Create(name = nameBase, scale = scale, hideParent = False, subLocator = False):
	locatorCurrent = cmds.spaceLocator(name = Text.SetUniqueFromText(name))[0]
	SetSize(locatorCurrent, scale, scale, scale)
	cmds.select(locatorCurrent)

	if hideParent:
		cmds.setAttr(locatorCurrent + Enums.Types.shape + "." + Enums.Attributes.visibility, 0)
	
	if subLocator:
		subLocator = Create(locatorCurrent + "Secondary")
		SetSize(subLocator, scale, scale, scale)
		cmds.parent(subLocator, locatorCurrent)
		cmds.select(subLocator)
		return locatorCurrent, subLocator
	else:
		return locatorCurrent

def CreateOnSelected(name = nameMatched, scale = scale, minSelectedCount = 1, hideParent = False, subLocator = False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(minSelectedCount)
	if (selectedList == None):
		return None
	
	# Create locators on selected
	locatorsList = []
	sublocatorsList = []
	for item in selectedList:
		nameCurrent = Text.GetShortName(item, removeSpaces = True) + "_" + name
		created = Create(name = nameCurrent, scale = scale, hideParent = hideParent, subLocator = subLocator)

		if subLocator:
			locatorsList.append(created[0])
			sublocatorsList.append(created[1])
		else:
			locatorsList.append(created)
		
		### It doesn't works well
		# positionCurrent = cmds.xform(item, query = True, worldSpace = True, translation = True)
		# rotationCurrent = cmds.xform(item, query = True, worldSpace = True, rotation = True)
		# scaleCurrent = cmds.xform(item, query = True, worldSpace = True, scale = True)
		# cmds.xform(locatorsList[-1], worldSpace = True, translation = positionCurrent, rotation = rotationCurrent, scale = scaleCurrent)
		###

		cmds.matchTransform(locatorsList[-1], item, position = True, rotation = True, scale = True)

	# Select objects and return
	if subLocator:
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def CreateOnSelectedWithParentConstrain(name = nameConstrained, scale = scale, minSelectedCount = 1, hideParent = False, subLocator = False):
	objects = CreateOnSelected(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocator = subLocator)
	if (objects == None):
		return None

	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if subLocator:
		sublocatorsList = objects[2]
	
	# Constrain locators
	for i in range(len(selectedList)):
		Constraints.ConstrainSecondToFirstObject(selectedList[i], locatorsList[i], maintainOffset = False)
	
	# Select objects and return
	if subLocator:
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def CreateOnSelectedAndBake(name = nameBaked, scale = scale, minSelectedCount = 1, hideParent = False, subLocator = False, parentToLastSelected = False):
	objects = CreateOnSelectedWithParentConstrain(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocator = subLocator)
	if (objects == None):
		return None

	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if subLocator:
		sublocatorsList = objects[2]

	# Parent locators to last or to last sublocator
	if (parentToLastSelected):
		if subLocator:
			locatorsListWithLastSub = locatorsList[:-1]
			locatorsListWithLastSub.append(sublocatorsList[-1])
			Parent.ListToLastObjects(locatorsListWithLastSub)
		else:
			Parent.ListToLastObjects(locatorsList)

	# Bake locators and delete constraints
	cmds.select(locatorsList)
	Baker.BakeSelected()
	Animation.DeleteStaticCurves()
	Constraints.DeleteConstraints(locatorsList)
	
	# Select objects and return
	if subLocator:
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def CreateOnSelectedReverseConstrain(name = nameReverse, scale = scale, minSelectedCount = 1, hideParent = False, subLocator = False, constrainTranslate = True, constrainRotate = True):
	objects = CreateOnSelectedAndBake(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocator = subLocator)
	if (objects == None):
		return None

	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if subLocator:
		sublocatorsList = objects[2]

	# Constrain objects to locators
	for i in range(len(selectedList)):
		if subLocator:
			firstObject = sublocatorsList[i]
		else:
			firstObject = locatorsList[i]
		
		Constraints.ConstrainSecondToFirstObject(firstObject, selectedList[i], maintainOffset = False, parent = constrainTranslate and constrainRotate, point = constrainTranslate, orient = constrainRotate)

	# Select objects and return
	if subLocator:
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def BakeAsChildrenFromLastSelected(scale = scale, minSelectedCount = 2, hideParent = False, subLocator = False):
	objects = CreateOnSelectedAndBake(scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocator = subLocator, parentToLastSelected = True)
	if (objects == None):
		return None
	
	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if subLocator:
		sublocatorsList = objects[2]
	
	# Select objects and return
	if subLocator:
		cmds.select(sublocatorsList[-1])
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList[-1])
		return objects

def BakeAsChildrenFromLastSelectedReverse(scale = scale, hideParent = False, subLocator = False, skipLastReverse = True):
	objects = BakeAsChildrenFromLastSelected(scale = scale, hideParent = hideParent, subLocator = subLocator)
	if (objects == None):
		return None
	
	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if subLocator:
		sublocatorsList = objects[2]
	
	# Constrain objects to locators
	for i in range(len(objects[0])):
		if (skipLastReverse and i == len(selectedList) - 1):
			break
		if subLocator:
			Constraints.ConstrainSecondToFirstObject(sublocatorsList[i], selectedList[i], maintainOffset = False)
		else:
			Constraints.ConstrainSecondToFirstObject(locatorsList[i], selectedList[i], maintainOffset = False)
	
	# Select objects and return
	if subLocator:
		cmds.select(sublocatorsList[-1])
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList[-1])
		return objects

def CreateOnSelectedAim(name = nameAim, scale = scale, minSelectedCount = 1, hideParent = False, subLocator = False, aimVector = (1, 0, 0), distance = 100, reverse = True):
	objects = CreateOnSelected(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocator = subLocator)
	if (objects == None):
		return None
	
	# Get lists from function
	selectedList = objects[0]
	locatorsRootList = objects[1]
	if subLocator:
		sublocatorsList = objects[2]
	
	# Create aim locators
	groupsList = []
	locatorsOffsetsList = []
	locatorsTargetsList = []
	for i in range(len(selectedList)):
		aimGroup = cmds.group(empty = True, name = selectedList[i] + "_AimGroup")
		locOffset = Create(name = locatorsRootList[i] + "Offset", scale = scale)
		locTarget = Create(name = locatorsRootList[i] + "Target", scale = scale)

		cmds.matchTransform(locOffset, locatorsRootList[i], position = True, rotation = True, scale = True)
		cmds.matchTransform(locTarget, locatorsRootList[i], position = True, rotation = True, scale = True)

		cmds.parent(locatorsRootList[i], aimGroup)
		cmds.parent(locOffset, locatorsRootList[i])
		cmds.parent(locTarget, aimGroup)

		if subLocator:
			cmds.matchTransform(sublocatorsList[i], locOffset, position = True, rotation = True, scale = True)
			cmds.parent(sublocatorsList[i], locOffset)
		
		aimVectorScaled = [0, 0, 0]
		aimVectorScaled[0] = aimVector[0] * distance
		aimVectorScaled[1] = aimVector[1] * distance
		aimVectorScaled[2] = aimVector[2] * distance
		cmds.move(aimVectorScaled[0], aimVectorScaled[1], aimVectorScaled[2], locTarget, relative = True, objectSpace = True, worldSpaceDistance = True)

		groupsList.append(aimGroup)
		locatorsOffsetsList.append(locOffset)
		locatorsTargetsList.append(locTarget)
		
		Constraints.ConstrainListToLastElement(selected = (locatorsRootList[i], selectedList[i]), parent = False, point = True, orient = True)
		Constraints.ConstrainListToLastElement(selected = (locTarget, selectedList[i]))
	
	# Bake animation from original objects
	cmds.select(locatorsRootList + locatorsTargetsList, replace = True)
	Baker.BakeSelected()
	Constraints.DeleteConstraints(locatorsRootList)
	Constraints.DeleteConstraints(locatorsTargetsList)
	Animation.DeleteStaticCurves()

	# Create aim constraint
	for i in range(len(selectedList)):
		if (aimVector[2] == 0):
			upVector = (0, 0, 1)
		else:
			upVector = (0, 1, 0)
		cmds.aimConstraint(locatorsTargetsList[i], locatorsOffsetsList[i], maintainOffset = True, weight = 1, aimVector = aimVector, upVector = upVector, worldUpType = "objectrotation", worldUpVector = upVector, worldUpObject = locatorsRootList[i])
	
	# Reverse constrain # TODO move constraint to temp group
	if (reverse):
		for i in range(len(selectedList)):
			parentObject = None
			if subLocator:
				parentObject = sublocatorsList[i]
			else:
				parentObject = locatorsOffsetsList[i]
			
			Constraints.ConstrainSecondToFirstObject(parentObject, selectedList[i], maintainOffset = False, parent = False, point = True, orient = True)
	
	# Select objects and return
	cmds.select(locatorsTargetsList)
	if subLocator:
		return selectedList, aimGroup, locatorsRootList, locatorsOffsetsList, locatorsTargetsList, sublocatorsList
	else:
		return selectedList, aimGroup, locatorsRootList, locatorsOffsetsList, locatorsTargetsList

