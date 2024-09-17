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

# TODO Set different time scale values. Aim and up should use slightly different values
# TODO Use one general nucleus node

import maya.cmds as cmds
import maya.mel as mel
# from math import pow, sqrt

from ..utils import Selector
from ..utils import Text
from ..values import Enums
from ..experimental import Physics


_defaultPrefix = "physics"
_defaultNameGroup = _defaultPrefix + "Grp"
_defaultNameGroupAim = _defaultPrefix + "GrpAim"
_defaultNameNucleus = _defaultPrefix + "Nucleus"
_defaultNameParticle = _defaultPrefix + "Particle"
_defaultNameLocGoal = _defaultPrefix + "LocGoal"
_defaultNameLocGoalOffset = _defaultPrefix + "LocGoalOffset"
_defaultNameLocParticle = _defaultPrefix + "LocParticle"
_defaultNameLocAimBase = _defaultPrefix + "LocAimBase"
_defaultNameLocAim = _defaultPrefix + "LocAim"
# _defaultNameLocAimOLD = _defaultPrefix + "LocAimOLD"
_defaultNameLocAimUp = _defaultPrefix + "LocAimUp"

_valueParticleRadius = 0.1
_valueParticleConserve = 1
_valueParticleDrag = 0.01
_valueParticleDamp = 0
_valueGoalSmooth = 1
_valueGoalWeight = 0.2
_nucleusTimeScale = 0.5

_scaleLocatorsOne = 0.1


def CreateParticleSetup(targetObject, parentGroup=None, customParentObject=None, positionOffset=(0,0,0)): # TODO
	### Names
	nameTargetObjectConverted = "_" + Text.ConvertSymbols(targetObject)
	nameGroup = _defaultNameGroup + nameTargetObjectConverted
	nameNucleus = _defaultNameNucleus + nameTargetObjectConverted
	nameParticle = _defaultNameParticle + nameTargetObjectConverted
	nameLocGoal = _defaultNameLocGoal + nameTargetObjectConverted
	nameLocGoalOffset = _defaultNameLocGoalOffset + nameTargetObjectConverted
	nameLocParticle = _defaultNameLocParticle + nameTargetObjectConverted

	### Create group
	if (parentGroup == None):
		cmds.select(clear = True)
		if (cmds.objExists(nameGroup)):
			cmds.delete(nameGroup)
		group = cmds.group(empty = True, name = nameGroup)
		cmds.select(clear = True)
	else:
		group = parentGroup

	### Nucleus node
	nucleusNodesBefore = cmds.ls(type = "nucleus")
	nucleus = Physics.CreateNucleus(name = nameNucleus, parent = group)
	cmds.select(clear = True)

	cmds.setAttr(nucleus + ".gravity", 0)
	cmds.setAttr(nucleus + ".timeScale", _nucleusTimeScale)
	# cmds.setAttr(nucleus + ".startFrame", self.time.values[2])
	# cmds.setAttr(nucleus + ".visibility", 0)


	### TODO Need to define colliderObjects before this logic
	### TODO Connect collision nRigid nodes to nucleus
	## colliderNodes[0] = cmds.createNode("nRigid", name = "myNRigid")
	## cmds.connectAttr("time1.outTime", colliderNodes[0] + ".currentTime")
	## cmds.connectAttr(colliderObjects[0] + ".worldMesh[0]", colliderNodes[0] + ".inputMesh")
	## cmds.connectAttr(colliderNodes[0] + ".currentState", nucleus + ".inputPassive[0]")
	## cmds.connectAttr(colliderNodes[0] + ".startState", nucleus + ".inputPassiveStart[0]")
	## cmds.connectAttr(nucleus + ".startFrame", colliderNodes[0] + ".startFrame")


	### Create locator goal
	locatorGoal = cmds.spaceLocator(name = nameLocGoal)[0]
	cmds.select(clear = True)
	cmds.parent(locatorGoal, group)
	cmds.select(clear = True)
	cmds.matchTransform(locatorGoal, targetObject, position = True, rotation = True)
	cmds.setAttr(locatorGoal + "Shape.localScaleX", _scaleLocatorsOne)
	cmds.setAttr(locatorGoal + "Shape.localScaleY", _scaleLocatorsOne)
	cmds.setAttr(locatorGoal + "Shape.localScaleZ", _scaleLocatorsOne)
	## cmds.setAttr(locatorGoal + ".visibility", 0) # TODO use when hidden
	## goalStartPosition = cmds.xform(locatorGoal, query = True, translation = True) # XXX probably deprecated

	### Constrain locator goal to specific parent object
	targetObjectForConstraint = targetObject
	if (customParentObject != None):
		targetObjectForConstraint = customParentObject
	cmds.parentConstraint(targetObjectForConstraint, locatorGoal, maintainOffset = True)

	### Create locator goal offset
	locatorGoalOffset = cmds.spaceLocator(name = nameLocGoalOffset)[0]
	cmds.select(clear = True)
	cmds.parent(locatorGoalOffset, locatorGoal)
	cmds.select(clear = True)
	cmds.matchTransform(locatorGoalOffset, locatorGoal, position = True, rotation = True)
	cmds.setAttr(locatorGoalOffset + "Shape.localScaleX", _scaleLocatorsOne)
	cmds.setAttr(locatorGoalOffset + "Shape.localScaleY", _scaleLocatorsOne)
	cmds.setAttr(locatorGoalOffset + "Shape.localScaleZ", _scaleLocatorsOne)

	### Position locator goal offset # TODO move to external method to control separately
	cmds.setAttr(locatorGoalOffset + ".translateX", positionOffset[0])
	cmds.setAttr(locatorGoalOffset + ".translateY", positionOffset[1])
	cmds.setAttr(locatorGoalOffset + ".translateZ", positionOffset[2])

	### Create particle
	position = cmds.xform(locatorGoalOffset, query = True, worldSpace = True, rotatePivot = True)
	particle = cmds.nParticle(name = nameParticle, position = position, conserve = 1)[0]
	cmds.select(clear = True)
	cmds.parent(particle, group)
	cmds.select(clear = True)

	### Create particle goal and get selected object position
	cmds.goal(particle, useTransformAsGoal = True, goal = locatorGoalOffset)
	## startPositionGoalParticle[1] = cmds.xform(particle, query = True, translation = True) # XXX probably deprecated

	### Reconnect particle to temp nucleus
	cmds.select(particle, replace = True)
	mel.eval("assignNSolver {0}".format(nucleus))
	cmds.select(clear = True)

	### Remove leftover nucleus nodes
	nucleusNodesAfter = cmds.ls(type = "nucleus")
	nucleusNodesToRemove = [item for item in nucleusNodesAfter if item not in nucleusNodesBefore]
	for item in nucleusNodesToRemove:
		if (item != nucleus):
			print("Leftover nucleus node {0} deleted".format(item))
			cmds.delete(item)

	### Set simulation attributes
	cmds.setAttr(particle + ".overrideEnabled", 1)
	cmds.setAttr(particle + ".overrideDisplayType", 2)
	cmds.setAttr(particle + "Shape.radius", _valueParticleRadius)
	cmds.setAttr(particle + "Shape.solverDisplay", 1)
	cmds.setAttr(particle + "Shape.conserve", _valueParticleConserve)
	cmds.setAttr(particle + "Shape.drag", _valueParticleDrag)
	cmds.setAttr(particle + "Shape.damp", _valueParticleDamp)
	cmds.setAttr(particle + "Shape.goalSmoothness", _valueGoalSmooth)
	cmds.setAttr(particle + "Shape.goalWeight[0]", _valueGoalWeight)

	### Create locator particle
	locatorParticle = cmds.spaceLocator(name = nameLocParticle)[0]
	cmds.select(clear = True)
	cmds.parent(locatorParticle, group)
	cmds.select(clear = True)
	cmds.matchTransform(locatorParticle, targetObject, position = True, rotation = True)
	cmds.connectAttr(particle + ".center", locatorParticle + ".translate", force = True)
	## cmds.setAttr(locatorParticle + ".visibility", 0) # TODO use when hidden

	return nameTargetObjectConverted, group, targetObject, locatorGoal, locatorParticle
def CreateAimSetup(particleSetup=None, positionOffset=(0,0,0)):
	if (particleSetup == None):
		cmds.warning("No Particle Setup specified. Cancel algorithm")
		return

	### Get particle setup variables
	nameTargetObjectConverted = particleSetup[0]
	group = particleSetup[1]
	targetObject = particleSetup[2]
	locatorGoal = particleSetup[3]
	locatorParticle = particleSetup[4]

	### Names
	nameGroupAim = _defaultNameGroupAim + nameTargetObjectConverted
	nameLocAimBase = _defaultNameLocAimBase + nameTargetObjectConverted
	nameLocAim = _defaultNameLocAim + nameTargetObjectConverted
	nameLocAimUp = _defaultNameLocAimUp + nameTargetObjectConverted		
	# nameLocAimOLD = _defaultNameLocAimOLD + nameTargetObjectConverted

	### Create group
	cmds.select(clear = True)
	if (cmds.objExists(nameGroupAim)):
		cmds.delete(nameGroupAim)
	groupAim = cmds.group(empty = True, name = nameGroupAim)
	cmds.select(clear = True)
	cmds.parent(groupAim, group)
	cmds.select(clear = True)

	### Create locator base aim
	locatorAimBase = cmds.spaceLocator(name = nameLocAimBase)[0]
	cmds.select(clear = True)
	cmds.parent(locatorAimBase, groupAim)
	cmds.select(clear = True)
	cmds.matchTransform(locatorAimBase, targetObject, position = True, rotation = True)
	cmds.setAttr(locatorAimBase + "Shape.localScaleX", _scaleLocatorsOne)
	cmds.setAttr(locatorAimBase + "Shape.localScaleY", _scaleLocatorsOne)
	cmds.setAttr(locatorAimBase + "Shape.localScaleZ", _scaleLocatorsOne)


	### Constrain locator aim base to locator goal
	cmds.parentConstraint(locatorGoal, locatorAimBase, maintainOffset = True)
	## cmds.setAttr(locatorAimBase + ".visibility", 0) # TODO use when hidden


	### Create locator aim
	locatorAim = cmds.spaceLocator(name = nameLocAim)[0]
	cmds.select(clear = True)
	cmds.matchTransform(locatorAim, locatorAimBase, position = True, rotation = True)
	cmds.parent(locatorAim, locatorAimBase)
	cmds.select(clear = True)
	cmds.setAttr(locatorAim + ".displayLocalAxis", True)


	# constraintAim = cmds.aimConstraint(locatorParticle, locatorAim, weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none") # XXX probably deprecated
	# cmds.delete(constraintAim) # locatorAim + "_aimConstraint1" # XXX probably deprecated


	### TODO Create locator aim up
	locatorAimUp = cmds.duplicate(locatorAim, name = nameLocAimUp)[0]
	cmds.parent(locatorAimUp, locatorAim)
	cmds.select(clear = True)
	cmds.setAttr(locatorAimUp + "." + "translateX", positionOffset[0])
	cmds.setAttr(locatorAimUp + "." + "translateY", positionOffset[1])
	cmds.setAttr(locatorAimUp + "." + "translateZ", positionOffset[2])
	cmds.parent(locatorAimUp, locatorAimBase)
	cmds.select(clear = True)
	cmds.setAttr(locatorAimUp + ".visibility", 0)
	cmds.setAttr(locatorAimUp + "Shape.localScaleX", _scaleLocatorsOne)
	cmds.setAttr(locatorAimUp + "Shape.localScaleY", _scaleLocatorsOne)
	cmds.setAttr(locatorAimUp + "Shape.localScaleZ", _scaleLocatorsOne)


	### Create aim up particle setup
	particleUpSetup = CreateParticleSetup(locatorAimUp)

	### Get particle up setup variables
	groupUp = particleUpSetup[1]
	locatorParticleUp = particleUpSetup[4]

	cmds.parent(groupUp, nameGroupAim)
	cmds.select(clear = True)

	### Create aim constraint
	cmds.aimConstraint(locatorParticle, locatorAim, weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = locatorParticleUp)
	

	### Create locator aim OLD # XXX probably deprecated
	# locatorAimOLD = cmds.spaceLocator(name = nameLocAimOLD)[0]
	# cmds.select(clear = True)
	# cmds.matchTransform(locatorAimOLD, locatorAimBase, position = True, rotation = True)
	# cmds.parent(locatorAimOLD, locatorAimBase)
	# cmds.select(clear = True)

	return locatorAim

def CreateOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	for item in selectedList:
		CreateParticleSetup(item)
def CreateAimOnSelected(*args): # TODO
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	offsetDistance = 5 # HACK for testing
	
	for item in selectedList:
		particleSetup = CreateParticleSetup(targetObject = item, positionOffset = (0, 0, offsetDistance)) # HACK for testing
		CreateAimSetup(particleSetup, positionOffset = (offsetDistance, 0, 0))
		# CreateAimSetup(particleSetup, positionOffset = (0, offsetDistance, 0))
def CreateAimChainOnSelected(*args): # TODO
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	distanceAim = 5 # HACK for testing
	distanceAimUp = 5 # HACK for testing
	particleAimSetupList = []
	
	for i in range(len(selectedList)):
		customParentObject = None
		if (i > 0):
			customParentObject = particleAimSetupList[i - 1]
		
		particleSetup = CreateParticleSetup(targetObject = selectedList[i], customParentObject = customParentObject, positionOffset = (0, 0, distanceAim)) # HACK for testing
		particleAimSetup = CreateAimSetup(particleSetup, positionOffset = (0, distanceAimUp, 0))
		particleAimSetupList.append(particleAimSetup)


# Enums.Main.axes