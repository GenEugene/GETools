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


_controlSize = 100
_nameGroupMain = "grpChain_"
_nameLocatorPrefix = "loc_"


def CreateRigVariant1(controlSize=_controlSize, *args):
	timeMin = cmds.playbackOptions(query = True, min = True)
	timeMax = cmds.playbackOptions(query = True, max = True)
	cmds.currentTime(timeMin, edit = True, update = True)

	### Create a list of names from selected objects
	selected = cmds.ls(selection = True)
	
	### Create main group as a container for all new objects
	mainGroup = cmds.group(name = _nameGroupMain + selected[-1], empty = True)
	
	### Init empty lists for groups and locators
	locators = []
	constraintsForBake = []
	
	### Count of selected objects
	count = len(selected)
	
	### Loop through each selected object, create groups, locators and parent them
	for i in range(count):
		### Create locator # TODO nurbs circle as control instead of locator (optional)
		locator = cmds.spaceLocator(name = _nameLocatorPrefix + selected[i])[0]
		locators.append(locator)
		cmds.setAttr(locator + "Shape.localScaleX", controlSize)
		cmds.setAttr(locator + "Shape.localScaleY", controlSize)
		cmds.setAttr(locator + "Shape.localScaleZ", controlSize)
		
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

def CreateRigVariant2(controlSize=_controlSize, *args):
	### Objects names
	nameGroupFixedPrefix = "grpFixed_"
	nameGroupDistributedPrefix = "grpDistr_"
	### Attributes names
	nameAttributeWeight = "distribution"
	nameAttributeGlobal = "global"
	### Nodes names
	nameMultiplyDivide = "gtMultiplyDivide"


	### Create a list of names from selected objects
	selected = cmds.ls(selection = True)
	
	### Create main group as a container for all new objects
	mainGroup = cmds.group(name = _nameGroupMain + selected[-1], empty = True)
	
	### Init empty lists for groups and locators
	groupsFixed = []
	groupsDistributed = []
	locators = []
	constraintsForBake = []
	
	### Count of selected objects
	count = len(selected)
	
	### Loop through each selected object, create groups, locators and parent them
	for i in range(count):
		### Create fixed group
		groupFixed = cmds.group(name = nameGroupFixedPrefix + selected[i], empty = True)
		groupsFixed.append(groupFixed)

		### Create distribution group
		groupDistributed = cmds.group(name = nameGroupDistributedPrefix + selected[i], empty = True)
		groupsDistributed.append(groupDistributed)
		
		### Create locator # TODO use nurbs circle [circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 1e-05 -s 8 -ch 1; objectMoveCommand;]
		locator = cmds.spaceLocator(name = _nameLocatorPrefix + selected[i])[0]
		locators.append(locator)
		cmds.setAttr(locator + "Shape.localScaleX", controlSize)
		cmds.setAttr(locator + "Shape.localScaleY", controlSize)
		cmds.setAttr(locator + "Shape.localScaleZ", controlSize)
		
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

		### Parent constraint groupFixed to original object
		constraint = cmds.parentConstraint(selected[i], groupFixed, maintainOffset = True)
		constraintsForBake.append(constraint[0])

	### Bake animation to locators and delete constraints
	timeMin = cmds.playbackOptions(query = True, min = True)
	timeMax = cmds.playbackOptions(query = True, max = True)
	cmds.bakeResults(groupsFixed, time = (timeMin, timeMax), simulation = True, minimizeRotation = True)
	cmds.delete(constraintsForBake)

	### Parent constraint original objects to locators
	for i in range(count):
		cmds.parentConstraint(locators[i], selected[i], maintainOffset = True)
	
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
	cmds.addAttr(locators[-1], longName = nameAttributeGlobal, attributeType = "double", defaultValue = 0, minValue = 0, maxValue = 1)
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

