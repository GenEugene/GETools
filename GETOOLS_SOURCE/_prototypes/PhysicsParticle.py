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
from .._prototypes import Physics


prefix = "prt"

particleRadius = 50
particleConserve = 1
particleDrag = 0.01
particleDamp = 0
goalSmooth = 3
goalWeight = 0.5
# nucleusTimeScale = 1


def Create(targetObject):
	## Names
	targetObjectConverted = Text.ConvertSymbols(targetObject)

	nameGroup = prefix + "Grp_" + targetObjectConverted

	nameLocGoalTarget = (prefix + "LocGoal", prefix + "LocTarget")
	nameLocGoal = nameLocGoalTarget[0] + targetObjectConverted
	# nameLocParticle = nameLocGoalTarget[1] + targetObjectConverted
	# nameNucleus = nameNucleus + targetObjectConverted
	nameParticle = prefix + "Particle" + targetObjectConverted
	# nameLocAimBase = prefix + "LocAimBase" + targetObjectConverted
	# nameLocAimHidden = prefix + "LocAimHidden" + targetObjectConverted
	# nameLocAim = prefix + "LocAim" + targetObjectConverted
	# nameLocAimUp = prefix + "LocAimUp" + targetObjectConverted		


	## Create group
	group = cmds.group(empty = True, name = nameGroup)
	

	## Create locator for goal
	locatorGoalTarget = cmds.spaceLocator(name = nameLocGoal)[0]
	cmds.parent(locatorGoalTarget, group)
	cmds.matchTransform(locatorGoalTarget, targetObject, position = True, rotation = True)
	cmds.parentConstraint(targetObject, locatorGoalTarget, maintainOffset = True)
	## cmds.setAttr(locatorGoalTarget + ".visibility", 0)
	## goalStartPosition = cmds.xform(locatorGoalTarget, query = True, translation = True)


	## Nucleus node # TODO
	nucleus = Physics.CreateNucleus()


	## TODO Connect collision nRigid nodes to nucleus # TODO Need to define colliderObject before this logic
	# colliderNodes[0] = cmds.createNode("nRigid", name = "myNRigid")
	# cmds.connectAttr("time1.outTime", colliderNodes[0] + ".currentTime")
	# cmds.connectAttr(colliderObjects[0] + ".worldMesh[0]", colliderNodes[0] + ".inputMesh")
	# cmds.connectAttr(colliderNodes[0] + ".currentState", nucleus + ".inputPassive[0]")
	# cmds.connectAttr(colliderNodes[0] + ".startState", nucleus + ".inputPassiveStart[0]")
	# cmds.connectAttr(nucleus + ".startFrame", colliderNodes[0] + ".startFrame")


	## Create particle, goal and get selected object position # TODO
	position = cmds.xform(targetObject, query = True, worldSpace = True, rotatePivot = True)
	particle = cmds.nParticle(name = nameParticle, position = position, conserve = 1)[0]
	cmds.goal(useTransformAsGoal = True, goal = locatorGoalTarget)
	cmds.parent(particle, group)
	### startPositionGoalParticle[1] = cmds.xform(particle, query = True, translation = True)
	cmds.setAttr(particle + ".overrideEnabled", 1)
	cmds.setAttr(particle + ".overrideDisplayType", 2)


	## Reconnect particle to temp nucleus and remove extra nodes # TODO
	mel.eval("assignNSolver {0}".format(nucleus))
	# nucleusNodesAfter = cmds.ls(type = "nucleus")
	
	# nodesForRemoving = [item for item in nucleusNodesAfter if item not in nucleusNodesBefore]
	# for item in nodesForRemoving:
	# 	if (item != nucleus):
	# 		cmds.warning("extra node deleted {0}".format(item))
	# 		cmds.delete(item)


	## Set simulation attributes # TODO
	cmds.setAttr(particle + "Shape.radius", particleRadius)
	cmds.setAttr(particle + "Shape.solverDisplay", 1)
	cmds.setAttr(particle + "Shape.conserve", particleConserve)
	cmds.setAttr(particle + "Shape.drag", particleDrag)
	cmds.setAttr(particle + "Shape.damp", particleDamp)
	cmds.setAttr(particle + "Shape.goalSmoothness", goalSmooth)
	cmds.setAttr(particle + "Shape.goalWeight[0]", goalWeight)


	## Create and connect locator to particle # TODO
	# particleLocGoalTarget[1] = cmds.spaceLocator(name = nameLocParticle)[0]
	# cmds.parent(particleLocGoalTarget[1], group)
	# cmds.matchTransform(particleLocGoalTarget[1], targetObject, position = True, rotation = True)
	# cmds.connectAttr(particle + ".center", particleLocGoalTarget[1] + ".translate", force = True)
	# cmds.setAttr(particleLocGoalTarget[1] + ".visibility", 0)


	## Create base aim locator # TODO
	# particleLocAim[0] = cmds.spaceLocator(name = nameLocAimBase)[0]
	# cmds.parent(particleLocAim[0], group)
	# cmds.matchTransform(particleLocAim[0], targetObject, position = True, rotation = True)
	# cmds.parentConstraint(targetObject, particleLocAim[0], maintainOffset = True)
	# cmds.setAttr(particleLocAim[0] + ".visibility", 0)


	## Create hidden aim locator # TODO
	# particleLocAim[1] = cmds.spaceLocator(name = nameLocAimHidden)[0]
	# cmds.matchTransform(particleLocAim[1], particleLocAim[0], position = True, rotation = True)
	# cmds.parent(particleLocAim[1], particleLocAim[0])
	# cmds.aimConstraint(particleLocGoalTarget[1], particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
	# cmds.delete(particleLocAim[1] + "_aimConstraint1")
	# particleLocAim[3] = cmds.duplicate(particleLocAim[1], name = nameLocAimUp)[0]
	# cmds.parent(particleLocAim[3], particleLocAim[1])
	# cmds.setAttr(particleLocAim[3] + ".ty", 100)
	# cmds.parent(particleLocAim[3], particleLocAim[0])
	# cmds.aimConstraint(particleLocGoalTarget[1], particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = particleLocAim[3]) # "scene" "object" "objectrotation" "vector" "none"
	

	## Create aim locator # TODO
	# particleLocAim[2] = cmds.spaceLocator(name = nameLocAim)[0]
	# cmds.matchTransform(particleLocAim[2], particleLocAim[0], position = True, rotation = True)
	# cmds.parent(particleLocAim[2], particleLocAim[0])


	cmds.select(targetObject, replace = True)

def CreateOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	for item in selectedList:
		Create(item)

