# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Baker
from GETOOLS_SOURCE.utils import Constraints
from GETOOLS_SOURCE.utils import Parent
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Text

# TODO think how to merge the same logic on each function. Looks like a lot of similar parts of code

nameBase = "gLoc"
nameMatched = "{0}Matched".format(nameBase)
nameConstrained = "{0}Constrained".format(nameBase)
nameBaked = "{0}Baked".format(nameBase)
nameReverse = "{0}Reverse".format(nameBase)
nameAim = "{0}Aim".format(nameBase)
scale = 1.0

def Create(name = nameBase, scale = scale, hideParent = False, subLocators = False):
	locatorCurrent = cmds.spaceLocator(name = Text.SetUniqueFromText(name))[0]
	cmds.setAttr(locatorCurrent + "Shape.localScaleX", scale)
	cmds.setAttr(locatorCurrent + "Shape.localScaleY", scale)
	cmds.setAttr(locatorCurrent + "Shape.localScaleZ", scale)
	cmds.select(locatorCurrent)

	if hideParent:
		cmds.setAttr(locatorCurrent + "Shape" + ".visibility", 0)
	
	if (subLocators):
		subLocator = Create(locatorCurrent + "Secondary")
		cmds.setAttr(subLocator + "Shape.localScaleX", scale)
		cmds.setAttr(subLocator + "Shape.localScaleY", scale)
		cmds.setAttr(subLocator + "Shape.localScaleZ", scale)
		cmds.parent(subLocator, locatorCurrent)
		cmds.select(subLocator)
		return locatorCurrent, subLocator
	else:
		return locatorCurrent

def CreateOnSelected(name = nameMatched, scale = scale, minSelectedCount = 1, hideParent = False, subLocators = False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(minSelectedCount)
	if (selectedList == None):
		return None
	
	# Create locators on selected
	locatorsList = []
	sublocatorsList = []
	for item in selectedList:
		nameCurrent = name + "_" + Text.GetShortName(item, removeSpaces = True)
		created = Create(name = nameCurrent, scale = scale, hideParent = hideParent, subLocators = subLocators)

		if (subLocators):
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
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def CreateOnSelectedWithParentConstrain(name = nameConstrained, scale = scale, minSelectedCount = 1, hideParent = False, subLocators = False):
	objects = CreateOnSelected(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocators = subLocators)
	if (objects == None):
		return None

	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if (subLocators):
		sublocatorsList = objects[2]
	
	# Constrain locators
	for i in range(len(selectedList)):
		Constraints.ConstrainSecondToFirstObject(selectedList[i], locatorsList[i], maintainOffset = False)
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def CreateOnSelectedAndBake(name = nameBaked, scale = scale, minSelectedCount = 1, hideParent = False, subLocators = False, parentToLastSelected = False):
	objects = CreateOnSelectedWithParentConstrain(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocators = subLocators)
	if (objects == None):
		return None

	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if (subLocators):
		sublocatorsList = objects[2]

	# Parent locators to last or to last sublocator
	if (parentToLastSelected):
		if (subLocators):
			locatorsListWithLastSub = locatorsList[:-1]
			locatorsListWithLastSub.append(sublocatorsList[-1])
			Parent.ListToLastObjects(locatorsListWithLastSub)
		else:
			Parent.ListToLastObjects(locatorsList)

	# Bake locators and delete constraints
	cmds.select(locatorsList)
	Baker.BakeSelected()
	for locator in locatorsList:
		children = cmds.listRelatives(locator, type = "constraint")
		for child in children:
			cmds.delete(child)
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def CreateOnSelectedReverseConstrain(name = nameReverse, scale = scale, minSelectedCount = 1, hideParent = False, subLocators = False):
	objects = CreateOnSelectedAndBake(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocators = subLocators)
	if (objects == None):
		return None

	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if (subLocators):
		sublocatorsList = objects[2]

	# Constrain objects to locators
	for i in range(len(selectedList)):
		if (subLocators):
			Constraints.ConstrainSecondToFirstObject(sublocatorsList[i], selectedList[i], maintainOffset = False)
		else:
			Constraints.ConstrainSecondToFirstObject(locatorsList[i], selectedList[i], maintainOffset = False)
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

def BakeAsChildrenFromLastSelected(scale = scale, minSelectedCount = 2, hideParent = False, subLocators = False):
	objects = CreateOnSelectedAndBake(scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocators = subLocators, parentToLastSelected = True)
	if (objects == None):
		return None
	
	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if (subLocators):
		sublocatorsList = objects[2]
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList[-1])
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList[-1])
		return objects

def BakeAsChildrenFromLastSelectedReverse(scale = scale, hideParent = False, subLocators = False, skipLastReverse = True):
	objects = BakeAsChildrenFromLastSelected(scale = scale, hideParent = hideParent, subLocators = subLocators)
	if (objects == None):
		return None
	
	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if (subLocators):
		sublocatorsList = objects[2]
	
	# Constrain objects to locators
	for i in range(len(objects[0])):
		if (skipLastReverse and i == len(selectedList) - 1):
			break
		if (subLocators):
			Constraints.ConstrainSecondToFirstObject(sublocatorsList[i], selectedList[i], maintainOffset = False)
		else:
			Constraints.ConstrainSecondToFirstObject(locatorsList[i], selectedList[i], maintainOffset = False)
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList[-1])
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList[-1])
		return objects

def CreateOnSelectedAim(name = nameAim, scale = scale, minSelectedCount = 1, hideParent = False, subLocators = False): # TODO
	objects = CreateOnSelected(name = name, scale = scale, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocators = subLocators)
	if (objects == None):
		return None
	
	# Get lists from function
	selectedList = objects[0]
	locatorsList = objects[1]
	if (subLocators):
		sublocatorsList = objects[2]
	
	# Main cycle
	for i in range(len(selectedList)): # TODO
		# root locator
		# 	offset locator
		# target locator

		print(selectedList[i])
	

	# cmds.group(empty = True, name = ) # TODO add each root locator to this group

	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	else:
		cmds.select(locatorsList)
		return selectedList, locatorsList

