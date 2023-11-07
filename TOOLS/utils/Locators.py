import maya.cmds as cmds
from utils import Text
from utils import Selector
from utils import Parent
from utils import Baker
from utils import Constraints

def Create(name="myLoc", scale=1, hideParent=False, subLocators=False):
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

	return locatorCurrent

def CreateOnSelected(name="myLocMatched", minSelectedCount=1, hideParent=False, subLocators=False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(minSelectedCount)
	if (selectedList == None):
		return None
	
	# Create locators on selected
	locatorsList = []
	sublocatorsList = []
	for item in selectedList:
		nameCurrent = Text.GetShortName(item, removeSpaces = True) + name
		created = Create(name = nameCurrent, hideParent = hideParent, subLocators = subLocators)

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
	cmds.select(locatorsList)
	return selectedList, locatorsList
def CreateOnSelectedWithParentConstrain(name="myLocConstrained", minSelectedCount=1, hideParent=False, subLocators=False):
	func_CreateOnSelected = CreateOnSelected(name, minSelectedCount, hideParent, subLocators)
	if (func_CreateOnSelected == None):
		return None

	# Get lists from function
	selectedList = func_CreateOnSelected[0]
	locatorsList = func_CreateOnSelected[1]
	if (subLocators):
		sublocatorsList = func_CreateOnSelected[2]
	
	# Constraint locators
	for i in range(len(selectedList)):
		Constraints.ConstrainSecondToFirstObject(selectedList[i], locatorsList[i], maintainOffset = False)
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	cmds.select(locatorsList)
	return selectedList, locatorsList
def CreateOnSelectedAndBake(name="myLocBaked", minSelectedCount=1, hideParent=False, subLocators=False, parentToLastSelected=False):
	func_CreateOnSelectedWithParentConstrain = CreateOnSelectedWithParentConstrain(name, minSelectedCount, hideParent, subLocators)
	if (func_CreateOnSelectedWithParentConstrain == None):
		return None

	# Get lists from function
	selectedList = func_CreateOnSelectedWithParentConstrain[0]
	locatorsList = func_CreateOnSelectedWithParentConstrain[1]
	if (subLocators):
		sublocatorsList = func_CreateOnSelectedWithParentConstrain[2]

	if (parentToLastSelected):
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
	cmds.select(locatorsList)
	return selectedList, locatorsList
def CreateOnSelectedReverseConstraint(name="myLocReverse", minSelectedCount=1, hideParent=False, subLocators=False):
	func_CreateOnSelectedAndBake = CreateOnSelectedAndBake(name, minSelectedCount = minSelectedCount, hideParent = hideParent, subLocators = subLocators)
	if (func_CreateOnSelectedAndBake == None):
		return None

	# Get lists from function
	selectedList = func_CreateOnSelectedAndBake[0]
	locatorsList = func_CreateOnSelectedAndBake[1]
	if (subLocators):
		sublocatorsList = func_CreateOnSelectedAndBake[2]

	# Constraint objects to locators
	for i in range(len(selectedList)):
		if (subLocators):
			Constraints.ConstrainSecondToFirstObject(sublocatorsList[i], selectedList[i], maintainOffset = False)
		else:
			Constraints.ConstrainSecondToFirstObject(locatorsList[i], selectedList[i], maintainOffset = False)
	
	# Select objects and return
	if (subLocators):
		cmds.select(sublocatorsList)
		return selectedList, locatorsList, sublocatorsList
	cmds.select(locatorsList)
	return selectedList, locatorsList

def BakeAsChildrenFromLastSelected(name="locBaked", minSelectedCount=2):
	objects = CreateOnSelectedAndBake(name = name, minSelectedCount = minSelectedCount, parentToLastSelected = True)
	if (objects == None):
		return None
	cmds.select(objects[1][-1])
	return objects

def BakeAsChildrenFromLastSelectedReverse():
	objects = BakeAsChildrenFromLastSelected()
	if (objects == None):
		return None
	
	for i in range(len(objects[0])):
		if (i == len(objects[0]) - 1):
			break
		Constraints.ConstrainSecondToFirstObject(objects[1][i], objects[0][i], maintainOffset = False)
	
	cmds.select(objects[1][-1])
	return objects
