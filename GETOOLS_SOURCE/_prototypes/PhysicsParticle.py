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
import maya.mel as mel
# from math import pow, sqrt

from ..utils import Selector
from ..utils import Text
from ..values import Enums
from .._prototypes import Physics


defaultPrefix = "prt"
defaultNameGroup = defaultPrefix + "Grp"
defaultNameNucleus = defaultPrefix + "Nucleus"
defaultNameParticle = defaultPrefix + "Particle"
defaultNameLocGoal = defaultPrefix + "LocGoal"
defaultNameLocParticle = defaultPrefix + "LocTarget"
defaultNameLocAimBase = defaultPrefix + "LocAimBase"
defaultNameLocAimHidden = defaultPrefix + "LocAimHidden"
defaultNameLocAim = defaultPrefix + "LocAim"
defaultNameLocAimUp = defaultPrefix + "LocAimUp"

valueParticleRadius = 20
valueParticleConserve = 1
valueParticleDrag = 0.01
valueParticleDamp = 0
valueGoalSmooth = 3
valueGoalWeight = 0.5
# nucleusTimeScale = 1


def CreateSetup(targetObject):
	### Names # TODO
	targetObjectConverted = "_" + Text.ConvertSymbols(targetObject)
	nameGroup = defaultNameGroup + targetObjectConverted
	nameNucleus = defaultNameNucleus + targetObjectConverted
	nameParticle = defaultNameParticle + targetObjectConverted
	nameLocGoal = defaultNameLocGoal + targetObjectConverted
	nameLocParticle = defaultNameLocParticle + targetObjectConverted
	
	nameLocAimBase = defaultNameLocAimBase + targetObjectConverted
	nameLocAimHidden = defaultNameLocAimHidden + targetObjectConverted
	nameLocAimUp = defaultNameLocAimUp + targetObjectConverted		
	# nameLocAim = defaultNameLocAim + targetObjectConverted


	### Create group
	cmds.select(clear = True)
	if (cmds.objExists(nameGroup)):
		cmds.delete(nameGroup)
	group = cmds.group(empty = True, name = nameGroup)
	cmds.select(clear = True)
	

	### Nucleus node
	nucleusNodesBefore = cmds.ls(type = "nucleus")
	nucleus = Physics.CreateNucleus(name = nameNucleus, parent = group)
	cmds.select(clear = True)


	## TODO Connect collision nRigid nodes to nucleus # TODO Need to define colliderObject before this logic
	## colliderNodes[0] = cmds.createNode("nRigid", name = "myNRigid")
	## cmds.connectAttr("time1.outTime", colliderNodes[0] + ".currentTime")
	## cmds.connectAttr(colliderObjects[0] + ".worldMesh[0]", colliderNodes[0] + ".inputMesh")
	## cmds.connectAttr(colliderNodes[0] + ".currentState", nucleus + ".inputPassive[0]")
	## cmds.connectAttr(colliderNodes[0] + ".startState", nucleus + ".inputPassiveStart[0]")
	## cmds.connectAttr(nucleus + ".startFrame", colliderNodes[0] + ".startFrame")


	### Create particle
	position = cmds.xform(targetObject, query = True, worldSpace = True, rotatePivot = True)
	particle = cmds.nParticle(name = nameParticle, position = position, conserve = 1)[0]
	cmds.select(clear = True)
	cmds.parent(particle, group)
	cmds.select(clear = True)


	### Create locator goal
	locatorGoal = cmds.spaceLocator(name = nameLocGoal)[0]
	cmds.select(clear = True)
	cmds.parent(locatorGoal, group)
	cmds.select(clear = True)
	cmds.matchTransform(locatorGoal, targetObject, position = True, rotation = True)
	cmds.parentConstraint(targetObject, locatorGoal, maintainOffset = True)
	## cmds.setAttr(locatorGoal + ".visibility", 0)
	## goalStartPosition = cmds.xform(locatorGoal, query = True, translation = True)
	

	### Create particle goal and get selected object position
	cmds.goal(particle, useTransformAsGoal = True, goal = locatorGoal)
	## startPositionGoalParticle[1] = cmds.xform(particle, query = True, translation = True)


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
	cmds.setAttr(particle + "Shape.radius", valueParticleRadius)
	cmds.setAttr(particle + "Shape.solverDisplay", 1)
	cmds.setAttr(particle + "Shape.conserve", valueParticleConserve)
	cmds.setAttr(particle + "Shape.drag", valueParticleDrag)
	cmds.setAttr(particle + "Shape.damp", valueParticleDamp)
	cmds.setAttr(particle + "Shape.goalSmoothness", valueGoalSmooth)
	cmds.setAttr(particle + "Shape.goalWeight[0]", valueGoalWeight)


	### Create locator particle
	locatorParticle = cmds.spaceLocator(name = nameLocParticle)[0]
	cmds.select(clear = True)
	cmds.parent(locatorParticle, group)
	cmds.select(clear = True)
	cmds.matchTransform(locatorParticle, targetObject, position = True, rotation = True)
	cmds.connectAttr(particle + ".center", locatorParticle + ".translate", force = True)
	## cmds.setAttr(locatorParticle + ".visibility", 0)


	return # TODO move to separate method


	### Create locator base aim
	locatorAimBase = cmds.spaceLocator(name = nameLocAimBase)[0]
	cmds.select(clear = True)
	cmds.parent(locatorAimBase, group)
	cmds.select(clear = True)
	cmds.matchTransform(locatorAimBase, targetObject, position = True, rotation = True)
	cmds.parentConstraint(targetObject, locatorAimBase, maintainOffset = True)
	## cmds.setAttr(locatorAimBase + ".visibility", 0)


	### Create locator hidden aim # TODO
	locatorAimHidden = cmds.spaceLocator(name = nameLocAimHidden)[0]
	cmds.select(clear = True)
	cmds.matchTransform(locatorAimHidden, locatorAimBase, position = True, rotation = True)
	cmds.parent(locatorAimHidden, locatorAimBase)
	cmds.select(clear = True)

	constraintAimHidden = cmds.aimConstraint(locatorParticle, locatorAimHidden, weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
	# cmds.delete(constraintAimHidden) # locatorAimHidden + "_aimConstraint1" # TODO use or not?


	### Create locator aim up
	locatorAimUp = cmds.duplicate(locatorAimHidden, name = nameLocAimUp)[0]
	cmds.parent(locatorAimUp, locatorAimHidden)
	cmds.select(clear = True)
	cmds.setAttr(locatorAimUp + "." + Enums.Attributes.translateShort[1], 100) # TODO set aim up distance
	cmds.parent(locatorAimUp, locatorAimBase)
	cmds.select(clear = True)
	cmds.aimConstraint(locatorParticle, locatorAimHidden, weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = locatorAimUp) # "scene" "object" "objectrotation" "vector" "none"


	### Create aim locator
	# locatorAim = cmds.spaceLocator(name = nameLocAim)[0]
	# cmds.select(clear = True)
	# cmds.matchTransform(locatorAim, locatorAimBase, position = True, rotation = True)
	# cmds.parent(locatorAim, locatorAimBase)
	# cmds.select(clear = True)

	pass


def CreateOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	for item in selectedList:
		CreateSetup(item)

