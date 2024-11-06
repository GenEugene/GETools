### TODO nurbs circle as control instead of locator (optional)


import maya.cmds as cmds


### Change variables if needed ###
locatorsSize = 100

### Objects names
nameGroupMain = "grpChain_"
nameLocatorPrefix = "loc_"


def CreateRig():
	timeMin = cmds.playbackOptions(query = True, min = True)
	timeMax = cmds.playbackOptions(query = True, max = True)
	cmds.currentTime(timeMin, edit = True, update = True)

	### Create a list of names from selected objects
	selected = cmds.ls(selection = True)
	
	### Create main group as a container for all new objects
	mainGroup = cmds.group(name = nameGroupMain + selected[-1], empty = True)
	
	### Init empty lists for groups and locators
	locators = []
	constraintsForBake = []
	
	### Count of selected objects
	count = len(selected)
	
	### Loop through each selected object, create groups, locators and parent them
	for i in range(count):
		### Create locator
		locator = cmds.spaceLocator(name = nameLocatorPrefix + selected[i])[0]
		locators.append(locator)
		cmds.setAttr(locator + "Shape.localScaleX", locatorsSize)
		cmds.setAttr(locator + "Shape.localScaleY", locatorsSize)
		cmds.setAttr(locator + "Shape.localScaleZ", locatorsSize)
		
		### Parent locator to group
		cmds.parent(locator, mainGroup)

		### Match group position and rotation
		cmds.matchTransform(locator, selected[i], position = True, rotation = True, scale = False)

		### Parent constraint groupFixed to original object
		constraint = cmds.parentConstraint(selected[i], locator, maintainOffset = False)
		constraintsForBake.append(constraint[0])

	### Bake animation to locators and delete constraints
	cmds.bakeResults(locators, time = (timeMin, timeMax), simulation = True, minimizeRotation = True)
	cmds.delete(constraintsForBake)

	### Constrain
	for i in range(count):
		cmds.pointConstraint(selected[i], locators[i], maintainOffset = False)
		cmds.orientConstraint(locators[i], selected[i], maintainOffset = False)

		if (i > 0 and i < count - 1):
			cmds.orientConstraint(locators[i - 1], locators[i], maintainOffset = True)
			cmds.orientConstraint(locators[i + 1], locators[i], maintainOffset = True)

	### Select last locator
	cmds.select(locators[-1], replace = True)
	
### Run function ###
CreateRig()

