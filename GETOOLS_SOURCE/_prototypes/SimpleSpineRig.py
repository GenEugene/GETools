### TODO unique naming fix
### TODO support different rotate orientation
### TODO preserve animation
### TODO nurbs circle as control instead of locator (optional)


import maya.cmds as cmds


### Change variables if needed ###
locatorsSize = 130

### Objects names
nameGroupMain = "SimpleChain"
nameGroupFixedPrefix = "grpFixed_"
nameGroupDistributedPrefix = "grpDistr_"
nameLocatorPrefix = "loc_"

### Attributes names
nameAttributeWeight = "distribution"
nameAttributeGlobal = "global"

### Nodes names
nameMultiplyDivide = "gtMultiplyDivide"


def CreateRig():
	### Create a list of names from selected objects
	selected = cmds.ls(selection = True)
	
	### Create main group as a container for all new objects
	mainGroup = cmds.group(name = nameGroupMain, empty = True)
	
	### Init empty lists for groups and locators
	groupsDistributed = []
	locators = []
	
	### Count of selected objects
	count = len(selected)
	
	### Loop through each selected object, create groups, locators and parent them
	for i in range(count):
		### Create fixed group
		groupFixed = cmds.group(name = nameGroupFixedPrefix + selected[i], empty = True)

		### Create distribution group
		groupDistributed = cmds.group(name = nameGroupDistributedPrefix + selected[i], empty = True)
		groupsDistributed.append(groupDistributed)
		
		### Create locator # TODO use nurbs circle [circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 1e-05 -s 8 -ch 1; objectMoveCommand;]
		locator = cmds.spaceLocator(name = nameLocatorPrefix + selected[i])[0]
		locators.append(locator)
		cmds.setAttr(locator + "Shape.localScaleX", locatorsSize)
		cmds.setAttr(locator + "Shape.localScaleY", locatorsSize)
		cmds.setAttr(locator + "Shape.localScaleZ", locatorsSize)
		
		### Parent locator to group
		cmds.parent(locator, groupDistributed)
		
		### Parent group to corresponding hierarchy object
		if i == 0:
			cmds.parent(groupFixed, mainGroup)
		else:
			cmds.parent(groupFixed, locators[i - 1])
		cmds.parent(groupDistributed, groupFixed)
		
		### Match group position and rotation
		cmds.matchTransform(groupFixed, selected[i], position = True, rotation = True, scale = False)

		### Parent constraint original object to locator
		cmds.parentConstraint(locator, selected[i], maintainOffset = True)

	### Show last locator Rotate Order and connect it to Distribution groups
	cmds.setAttr(locators[-1] + ".rotateOrder", channelBox = True)
	for i in range(count):
		groupsDistributed[i]
		cmds.connectAttr(locators[-1] + ".rotateOrder", groupsDistributed[i] + ".rotateOrder")
	
	### Check if selected count less than 3 objects and break function
	if (count < 3):
		cmds.warning("You have less than 3 objects selected. Rotation distribution will not be created")
		return
	
	### Create weight attribute on last locator
	cmds.addAttr(locators[-1], longName = nameAttributeWeight, attributeType = "double", defaultValue = count - 1)
	cmds.setAttr(locators[-1] + "." + nameAttributeWeight, edit = True, keyable = True)
	
	### Create MultiplyDivide node
	nodeMultiplyDivide = cmds.createNode("multiplyDivide", name = nameMultiplyDivide)
	cmds.setAttr(nodeMultiplyDivide + ".operation", 2)
	
	### Connect rotation and weight to MultiplyDivide node
	cmds.connectAttr(locators[-1] + ".rotate", nodeMultiplyDivide + ".input1")
	cmds.connectAttr(locators[-1] + "." + nameAttributeWeight, nodeMultiplyDivide + ".input2X")
	cmds.connectAttr(locators[-1] + "." + nameAttributeWeight, nodeMultiplyDivide + ".input2Y")
	cmds.connectAttr(locators[-1] + "." + nameAttributeWeight, nodeMultiplyDivide + ".input2Z")

	### Connect rotation distribution to other locators' groups
	for i in range(1, count - 1):
		cmds.connectAttr(nodeMultiplyDivide + ".output", groupsDistributed[i] + ".rotate")
	
	### Add global attribute for last locator
	cmds.addAttr(locators[-1], longName = nameAttributeGlobal, attributeType = "double", defaultValue = 1, minValue = 0, maxValue = 1)
	cmds.setAttr(locators[-1] + "." + nameAttributeGlobal, edit = True, keyable = True)

	### Create Orient Constraint for last locator
	cmds.orientConstraint(mainGroup, groupsDistributed[-1], maintainOffset = True)[0]

	### Show blend orient attribute by setting keys on constrained rotation attributes # I frankly don't know how to do it better
	cmds.setKeyframe(groupsDistributed[-1] + ".rx")
	cmds.setKeyframe(groupsDistributed[-1] + ".ry")
	cmds.setKeyframe(groupsDistributed[-1] + ".rz")

	### Connect Global attribute to blend orient attribute
	cmds.connectAttr(locators[-1] + "." + nameAttributeGlobal, groupsDistributed[-1] + ".blendOrient1")

	### Select last locator
	cmds.select(locators[-1], replace = True)
	
### Run function ###
CreateRig()

