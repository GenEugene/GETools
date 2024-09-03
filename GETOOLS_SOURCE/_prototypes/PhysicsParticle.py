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
from math import pow, sqrt

from . import Selector
from . import Text


class ParticleSettings:
	# NAMING
	prefix = "ovlp"
	prefixLayer = "_" + prefix

	nameGroup = prefix + "Group"
	nameLocGoalTarget = (prefix + "LocGoal", prefix + "LocTarget")
	nameLocAim = (prefix + "LocAimBase", prefix + "LocAimHidden", prefix + "LocAim", prefix + "LocAimUp")
	nameNucleus = prefix + "Nucleus"
	nameParticle = prefix + "Particle"
	
	# SIMULATION SETTINGS
	particleRadius = 5
	particleConserve = 1
	particleDrag = 0.01
	particleDamp = 0
	goalSmooth = 3
	goalWeight = 0.5
	nucleusTimeScale = 1

class Particle:
	def __init__(self):
		# OBJECTS
		self.selectedObjects = ""
		self.nucleus = ""
		self.nucleusNodesBefore = [""]
		self.nucleusNodesAfter = [""]

		# PARTICLE MODE
		self.particle = ""
		self.particleLocGoalTarget = ["", ""]
		self.particleLocAim = ["", "", "", ""]
		self.particleGoalStartPosition = [None, (0, 0, 0)]

	def _ParticleSetupInit(self, *args):
		# Remove previous setup if exists
		self._ParticleSetupDelete(deselect = False)
		
		# Get selected objects
		self.selectedObjects = Selector.MultipleObjects(minimalCount = 1)
		if (self.selectedObjects == None):
			self.selectedObjects = ""
			return
		
		self.selectedObjects = self.selectedObjects[0]

		# Create group
		cmds.select(clear = True)
		if (cmds.objExists(ParticleSettings.nameGroup)):
			cmds.delete(ParticleSettings.nameGroup)
		cmds.group(empty = True, name = ParticleSettings.nameGroup)
		
		# Run setup logic
		self._ParticleSetupCreate(self.selectedObjects)
		cmds.select(self.selectedObjects, replace = True)
		
	def _ParticleSetupCreate(self, objCurrent, *args): # TODO replace locators by locators class
		# Names
		objConverted = Text.ConvertSymbols(objCurrent)
		nameLocGoal = ParticleSettings.nameLocGoalTarget[0] + objConverted
		nameLocParticle = ParticleSettings.nameLocGoalTarget[1] + objConverted
		nameNucleus = ParticleSettings.nameNucleus + objConverted
		nameParticle = ParticleSettings.nameParticle + objConverted
		nameLocAimBase = ParticleSettings.nameLocAim[0] + objConverted
		nameLocAimHidden = ParticleSettings.nameLocAim[1] + objConverted
		nameLocAim = ParticleSettings.nameLocAim[2] + objConverted
		nameLocAimUp = ParticleSettings.nameLocAim[3] + objConverted		

		# Create locator for goal
		self.particleLocGoalTarget[0] = cmds.spaceLocator(name = nameLocGoal)[0]
		cmds.parent(self.particleLocGoalTarget[0], ParticleSettings.nameGroup)
		cmds.matchTransform(self.particleLocGoalTarget[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.particleLocGoalTarget[0], maintainOffset = True)
		cmds.setAttr(self.particleLocGoalTarget[0] + ".visibility", 0)
		self.particleGoalStartPosition[0] = cmds.xform(self.particleLocGoalTarget[0], query = True, translation = True)

		# Nucleus node
		self.nucleusNodesBefore = cmds.ls(type = "nucleus")
		self.nucleus = cmds.createNode("nucleus", name = nameNucleus)
		cmds.connectAttr("time1.outTime", self.nucleus + ".currentTime")
		cmds.parent(self.nucleus, ParticleSettings.nameGroup)
		# self.sliderNTimeScale.startName = self.nucleus
		cmds.setAttr(self.nucleus + ".gravity", 0)
		cmds.setAttr(self.nucleus + ".timeScale", self.sliderNucleusTimeScale.Get())
		cmds.setAttr(self.nucleus + ".startFrame", self.time.values[2])
		cmds.setAttr(self.nucleus + ".visibility", 0)


		# TODO Connect collision nRigid nodes to nucleus # TODO Need to define colliderObject before this logic
		# self.colliderNodes[0] = cmds.createNode("nRigid", name = "myNRigid")
		# cmds.connectAttr("time1.outTime", self.colliderNodes[0] + ".currentTime")
		# cmds.connectAttr(self.colliderObjects[0] + ".worldMesh[0]", self.colliderNodes[0] + ".inputMesh")
		# cmds.connectAttr(self.colliderNodes[0] + ".currentState", self.nucleus + ".inputPassive[0]")
		# cmds.connectAttr(self.colliderNodes[0] + ".startState", self.nucleus + ".inputPassiveStart[0]")
		# cmds.connectAttr(self.nucleus + ".startFrame", self.colliderNodes[0] + ".startFrame")


		# Create particle, goal and get selected object position
		position = cmds.xform(objCurrent, query = True, worldSpace = True, rotatePivot = True)
		self.particle = cmds.nParticle(name = nameParticle, position = position, conserve = 1)[0]
		cmds.goal(useTransformAsGoal = True, goal = self.particleLocGoalTarget[0])
		cmds.parent(self.particle, ParticleSettings.nameGroup)
		# self.startPositionGoalParticle[1] = cmds.xform(self.particle, query = True, translation = True)
		cmds.setAttr(self.particle + ".overrideEnabled", 1)
		cmds.setAttr(self.particle + ".overrideDisplayType", 2)

		# Reconnect particle to temp nucleus and remove extra nodes
		mel.eval("assignNSolver {0}".format(nameNucleus))
		self.nucleusNodesAfter = cmds.ls(type = "nucleus")
		nodesForRemoving = [item for item in self.nucleusNodesAfter if item not in self.nucleusNodesBefore]
		for item in nodesForRemoving:
			if (item != self.nucleus):
				# cmds.warning("extra node deleted {0}".format(item))
				cmds.delete(item)

		# Set simulation attributes
		cmds.setAttr(self.particle + "Shape.radius", self.sliderParticleRadius.Get())
		cmds.setAttr(self.particle + "Shape.solverDisplay", 1)
		cmds.setAttr(self.particle + "Shape.conserve", self.sliderParticleConserve.Get())
		cmds.setAttr(self.particle + "Shape.drag", self.sliderParticleDrag.Get())
		cmds.setAttr(self.particle + "Shape.damp", self.sliderParticleDamp.Get())
		cmds.setAttr(self.particle + "Shape.goalSmoothness", self.sliderParticleGoalSmooth.Get())
		cmds.setAttr(self.particle + "Shape.goalWeight[0]", self.sliderParticleGoalWeight.Get())

		# Create and connect locator to particle
		self.particleLocGoalTarget[1] = cmds.spaceLocator(name = nameLocParticle)[0]
		cmds.parent(self.particleLocGoalTarget[1], ParticleSettings.nameGroup)
		cmds.matchTransform(self.particleLocGoalTarget[1], objCurrent, position = True, rotation = True)
		cmds.connectAttr(self.particle + ".center", self.particleLocGoalTarget[1] + ".translate", force = True)
		cmds.setAttr(self.particleLocGoalTarget[1] + ".visibility", 0)

		# Create base aim locator
		self.particleLocAim[0] = cmds.spaceLocator(name = nameLocAimBase)[0]
		cmds.parent(self.particleLocAim[0], ParticleSettings.nameGroup)
		cmds.matchTransform(self.particleLocAim[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.particleLocAim[0], maintainOffset = True)
		cmds.setAttr(self.particleLocAim[0] + ".visibility", 0)

		# Create hidden aim locator
		self.particleLocAim[1] = cmds.spaceLocator(name = nameLocAimHidden)[0]
		cmds.matchTransform(self.particleLocAim[1], self.particleLocAim[0], position = True, rotation = True)
		cmds.parent(self.particleLocAim[1], self.particleLocAim[0])
		cmds.aimConstraint(self.particleLocGoalTarget[1], self.particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		cmds.delete(self.particleLocAim[1] + "_aimConstraint1")
		self.particleLocAim[3] = cmds.duplicate(self.particleLocAim[1], name = nameLocAimUp)[0]
		cmds.parent(self.particleLocAim[3], self.particleLocAim[1])
		cmds.setAttr(self.particleLocAim[3] + ".ty", 100)
		cmds.parent(self.particleLocAim[3], self.particleLocAim[0])
		cmds.aimConstraint(self.particleLocGoalTarget[1], self.particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.particleLocAim[3]) # "scene" "object" "objectrotation" "vector" "none"
		
		# Create aim locator
		self.particleLocAim[2] = cmds.spaceLocator(name = nameLocAim)[0]
		cmds.matchTransform(self.particleLocAim[2], self.particleLocAim[0], position = True, rotation = True)
		cmds.parent(self.particleLocAim[2], self.particleLocAim[0])


