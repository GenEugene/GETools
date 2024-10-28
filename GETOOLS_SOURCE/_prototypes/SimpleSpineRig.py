import maya.cmds as cmds


### Variables to change before using script ###
locatorsSize = 130
nameWeightAttribute = "weight"
nameMultiplyDivide = "myMultiplyDivide"

def CreateRig():
	# Get names of selected objects as list
	selected = cmds.ls(selection = True) # , absoluteName = True
	
	# Create main group as a container for all new objects
	mainGroup = cmds.group(name = "grpLocators", empty = True)
	
	# Init empty lists for groups and locators
	groups = []
	locators = []
	
	# Count of selected objects
	count = len(selected)
	
	# Loop through each selected object, create groups, locators and parent them
	for i in range(count):
		# Create group
		locatorGroup = cmds.group(name = "grp_" + selected[i], empty = True)
		groups.append(locatorGroup)
		
		# Create locator
		locator = cmds.spaceLocator(name = "loc_" + selected[i])[0]
		locators.append(locator)
		cmds.setAttr(locator + "Shape.localScaleX", locatorsSize)
		cmds.setAttr(locator + "Shape.localScaleY", locatorsSize)
		cmds.setAttr(locator + "Shape.localScaleZ", locatorsSize)
		
		# Parent locator to group
		cmds.parent(locator, locatorGroup)
		
		# Parent group to corresponding hierarchy object
		if i == 0:
			cmds.parent(locatorGroup, mainGroup)
		else:
			cmds.parent(locatorGroup, locators[i - 1])
		
		# Match group position and rotation
		position = cmds.xform(selected[i], query = True, worldSpace = True, rotatePivot = True)
		rotation = cmds.xform(selected[i], query = True, worldSpace = True, rotation = True)
		cmds.xform(locatorGroup, translation = position, rotation = rotation, worldSpace = True)
		
		# Parent constraint original object to locator
		cmds.parentConstraint(locator, selected[i], maintainOffset = True)
	
	# Select last locator
	cmds.select(locators[-1], replace = True)
	
	# Check if selected count less than 3 objects and break function
	if (count < 3):
		cmds.warning("You have less than 3 objects selected. Rotation distribution will not be created")
		return
	
	# Create weight attribute on last locator
	cmds.addAttr(locators[-1], longName = nameWeightAttribute, attributeType = "double", defaultValue = 0.5)
	cmds.setAttr(locators[-1] + "." + nameWeightAttribute, edit = True, keyable = True)
	
	# Create MultiplyDivide node
	nodeMultiplyDivide = cmds.createNode("multiplyDivide", name = nameMultiplyDivide)
	
	# Connect rotation and weight to MultiplyDivide node
	cmds.connectAttr(locators[-1] + ".rotate", nodeMultiplyDivide + ".input1")
	cmds.connectAttr(locators[-1] + "." + nameWeightAttribute, nodeMultiplyDivide + ".input2X")
	cmds.connectAttr(locators[-1] + "." + nameWeightAttribute, nodeMultiplyDivide + ".input2Y")
	cmds.connectAttr(locators[-1] + "." + nameWeightAttribute, nodeMultiplyDivide + ".input2Z")
	
	# Connect rotation distribution to other locators' groups
	for i in range(1, count - 1):
		cmds.connectAttr(nodeMultiplyDivide + ".output", groups[i] + ".rotate")

### Run function ###
CreateRig()

