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
from functools import partial

from .. import Settings
from ..utils import Baker
from ..utils import Colors
from ..utils import Constraints
from ..utils import Locators
from ..utils import Selector
from ..utils import Text


class CenterOfMassAnnotations:
	### Setup
	create = "Create center of mass object.\nIt's just a simple joint that temporary stored in memory."
	activate = "Make selected center of mass object as active.\nUseful if you have more than one center of mass object or if you closed script or Maya.\
	\nCenter of mass must be activated if you want to use other features from script."
	select = "Select current activated center of mass object"
	clean = "Delete center of mass object"
	_projector = "Create extra object projected from center of mass to"
	projectorYZ = _projector + " YZ plane"
	projectorXZ = _projector + " XZ plane"
	projectorXY = _projector + " XY plane"

	### Weights
	disconnectTargets = "Disconnect selected objects from Center Of Mass"
	weightsCustom = "Custom weights"
	_weightInfo = "Approximate weight as percentage. In sum all weights should give 100%."
	_weightSymmetry = "Select objects on both sides and activate button."
	weightHead = _weightInfo
	weightChest = _weightInfo
	weightAbdomen = _weightInfo
	weightShoulder = "{1}\n{0}".format(_weightInfo, _weightSymmetry)
	weightElbow = "{1}\n{0}".format(_weightInfo, _weightSymmetry)
	weightHand = "{1}\n{0}".format(_weightInfo, _weightSymmetry)
	weightThigh = "{1}\n{0}".format(_weightInfo, _weightSymmetry)
	weightKnee = "{1}\n{0}".format(_weightInfo, _weightSymmetry)
	weightFoot = "{1}\n{0}".format(_weightInfo, _weightSymmetry)

	### Baking
	bakeToCOM = "Bake selected objects as locators relative to the center of mass object."
	bakeToCOMLink = "{0}\nAfter bake constrain selected objects back to locators.".format(bakeToCOM)
	bakeOriginal = "Bake animation back to original objects from locators."
	link = "Constrain cached objects to baked locators."
	linkOffset = "{0}\nUse maintain offset to keep transform difference".format(link)
	selectRoot = "Select root locator if exists"

class CenterOfMassSettings:
	COMRadius = 10 / 3
	weightMinMax = (1, 10)

	# BODYPARTS MAPPING PERCENTAGE
	partHead = ("head", 7.3)
	partChest = ("chest", 35.8)
	partAbdomen = ("abdomen", 10.1)
	partShoulder = ("shoulder", 3.1)
	partElbow = ("elbow", 1.7)
	partHand = ("hand ", 0.8)
	partThigh = ("thigh", 11.5)
	partKnee = ("knee", 4.4)
	partFoot = ("foot", 1.9)

class CenterOfMass:
	_version = "v1.4"
	_name = "CENTER OF MASS"
	_title = _name + " " + _version

	# HACK use only for code editor # TODO try to find better way to get access to other classes with cross import
	# from ..modules import GeneralWindow
	# def __init__(self, generalInstance: GeneralWindow.GeneralWindow):
	def __init__(self, generalInstance):
		self.generalInstance = generalInstance

		self.COMObject = None
		self.CachedSelectedObjects = None

		self.layoutSetup = None
		self.layoutWeights = None
		self.layoutBaking = None
	def UICreate(self, layoutMain):
		self.UILayoutSetup(layoutMain)
		self.UILayoutWeights(layoutMain)
		self.UILayoutBaking(layoutMain)
	def UILayoutSetup(self, layoutMain):
		self.layoutSetup = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "SETUP", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutSetup, adjustableColumn = True)
		#
		COMButtons1 = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = COMButtons1, cellWidth = Settings.windowWidthMargin / COMButtons1, cellHeight = Settings.lineHeight)
		cmds.button(label = "Create", command = self.COMCreate, backgroundColor = Colors.green50, annotation = CenterOfMassAnnotations.create)
		cmds.button(label = "Activate", command = self.COMActivate, backgroundColor = Colors.yellow50, annotation = CenterOfMassAnnotations.activate)
		cmds.button(label = "Select", command = self.COMSelect, backgroundColor = Colors.lightBlue50, annotation = CenterOfMassAnnotations.select)
		cmds.button(label = "Clean", command = self.COMClean, backgroundColor = Colors.red50, annotation = CenterOfMassAnnotations.clean)
		#
		COMButtons2 = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = COMButtons2, cellWidth = Settings.windowWidthMargin / COMButtons2, cellHeight = Settings.lineHeight)
		cmds.button(label = "Projector YZ", command = partial(self.COMFloorProjection, "x"), backgroundColor = Colors.red10, annotation = CenterOfMassAnnotations.projectorYZ)
		cmds.button(label = "Projector XZ", command = partial(self.COMFloorProjection, "y"), backgroundColor = Colors.green10, annotation = CenterOfMassAnnotations.projectorXZ)
		cmds.button(label = "Projector XY", command = partial(self.COMFloorProjection, "z"), backgroundColor = Colors.blue10, annotation = CenterOfMassAnnotations.projectorXY)
	def UILayoutWeights(self, layoutMain):
		self.layoutWeights = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "WEIGHTS", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutWeights, adjustableColumn = True)

		count = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Disconnect From Center Of Mass", command = self.COMDisconnectTargets, backgroundColor = Colors.red10, annotation = CenterOfMassAnnotations.disconnectTargets)
		
		def PartButton(partInfo = ("", 0), minMaxValue = CenterOfMassSettings.weightMinMax, onlyValue = False, annotation = ""):
			value = partInfo[1]
			text = "{1}" if onlyValue else "{0} {1}"
			colorValue = 1 - (value / (minMaxValue[1] - minMaxValue[0]))
			colorFinal = (colorValue, colorValue, colorValue)
			cmds.button(label = text.format(partInfo[0], value), command = partial(self.COMConstrainToSelected, value), backgroundColor = colorFinal, annotation = annotation)

		### WEIGHTS PALETTE
		count = 10
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		
		def CustomButton(value):
			PartButton(("", value), onlyValue = True, annotation = CenterOfMassAnnotations.weightsCustom)
		CustomButton(1)
		CustomButton(2)
		CustomButton(3)
		CustomButton(4)
		CustomButton(5)
		CustomButton(6)
		CustomButton(7)
		CustomButton(8)
		CustomButton(9)
		CustomButton(10)

		### BODYPARTS
		count = 3
		layoutBodyGrid = cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight * count)
		
		cmds.columnLayout(parent = layoutBodyGrid, adjustableColumn = True)
		PartButton(CenterOfMassSettings.partHead, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightHead)
		PartButton(CenterOfMassSettings.partChest, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightChest)
		PartButton(CenterOfMassSettings.partAbdomen, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightAbdomen)
		
		cmds.columnLayout(parent = layoutBodyGrid, adjustableColumn = True)
		PartButton(CenterOfMassSettings.partShoulder, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightShoulder)
		PartButton(CenterOfMassSettings.partElbow, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightElbow)
		PartButton(CenterOfMassSettings.partHand, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightHand)
		
		cmds.columnLayout(parent = layoutBodyGrid, adjustableColumn = True)
		PartButton(CenterOfMassSettings.partThigh, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightThigh)
		PartButton(CenterOfMassSettings.partKnee, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightKnee)
		PartButton(CenterOfMassSettings.partFoot, minMaxValue = (CenterOfMassSettings.partHand[1], CenterOfMassSettings.partChest[1]), annotation = CenterOfMassAnnotations.weightFoot)
	def UILayoutBaking(self, layoutMain):
		self.layoutBaking = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "BAKING", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)

		count = 3
		cmds.gridLayout(numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)

		cmds.button(label = "Bake To COM", command = self.BakeScenario2, backgroundColor = Colors.orange10, annotation = CenterOfMassAnnotations.bakeToCOM)
		cmds.button(label = "Bake + Link", command = self.BakeScenario3, backgroundColor = Colors.orange50, annotation = CenterOfMassAnnotations.bakeToCOMLink)
		cmds.button(label = "Bake Original", command = self.BakeCached, backgroundColor = Colors.orange100, annotation = CenterOfMassAnnotations.bakeOriginal)
		
		cmds.button(label = "Link", command = partial(self.LinkCached, False), backgroundColor = Colors.yellow10, annotation = CenterOfMassAnnotations.link)
		cmds.button(label = "Link Offset", command = partial(self.LinkCached, True), backgroundColor = Colors.yellow10, annotation = CenterOfMassAnnotations.linkOffset)
		cmds.button(label = "Select Root", command = self.SelectParent, backgroundColor = Colors.lightBlue50, annotation = CenterOfMassAnnotations.selectRoot)


	### CENTER OF MASS
	def COMObjectCheck(self, *args):
		if (self.COMObject == None):
			cmds.warning("Center of mass doesn't stored in the script memory. You need to create new COM object or select one in the scene and press \"Activate\" button")
			return False
		else:
			if (cmds.objExists(self.COMObject)):
				return True
			else:
				cmds.warning("Center of mass stored in the script memory, but doesn't exist in the scene. You need to create new COM object or select one in the scene and press \"Activate\" button")
				return False
	def COMCreate(self, *args):
		# self.centerOfMass = cmds.polySphere(name = "myCenterOfMass", subdivisionsX = 8, subdivisionsY = 6, radius = 10)
		# self.centerOfMass = Locators.Create("locCenterOfMass", 5)
		# self.COMObjectRef = cmds.polyPrimitive(name = "objCenterOfMass", radius = CenterOfMassSettings.COMRadius, polyType = 0, constructionHistory = 0)
		# cmds.polySoftEdge(angle = 0, constructionHistory = 0)
		# self.COMGroupRef = cmds.group(name = "grpCenterOfMass")
		
		cmds.select(clear = True)
		self.COMObject = cmds.joint(name = Text.SetUniqueFromText("objCenterOfMass"), radius = CenterOfMassSettings.COMRadius)
		cmds.setAttr(self.COMObject + ".drawLabel", 1)
		cmds.setAttr(self.COMObject + ".type", 18)
		cmds.setAttr(self.COMObject + ".otherType", "Center Of Mass", type = "string")
		cmds.select(self.COMObject)
	def COMActivate(self, *args):
		# Check selected objects
		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return
		self.COMObject = selectedList[0]
	def COMSelect(self, *args):
		if (self.COMObjectCheck()):
			cmds.select(self.COMObject)
	def COMClean(self, *args):
		if (self.COMObjectCheck()):
			cmds.delete(self.COMObject)
			self.COMObject = None
			cmds.warning("Last active center of mass object was deleted")
	def COMFloorProjection(self, skipAxis="y", *args):
		if (not self.COMObjectCheck()):
			return

		name = "COM" + "Projection" + "xyz".replace(skipAxis, "").upper()
		projection = cmds.polyPrimitive(name = Text.SetUniqueFromText(name), radius = CenterOfMassSettings.COMRadius, polyType = 0, constructionHistory = 0)
		cmds.polySoftEdge(angle = 0, constructionHistory = 0)

		cmds.setAttr(projection[0] + "Shape" + ".visibility", 0)
		cmds.setAttr(projection[0] + "Shape" + ".overrideEnabled", 1)
		cmds.setAttr(projection[0] + "Shape" + ".overrideDisplayType", 2)

		cmds.select(clear = True)

		cmds.pointConstraint(self.COMObject, projection, maintainOffset = False, skip = skipAxis)

		joint1 = cmds.joint(name = Text.SetUniqueFromText("objCenterOfMassFloorProjectionJoint1"), radius = 1)
		joint2 = cmds.joint(name = Text.SetUniqueFromText("objCenterOfMassFloorProjectionJoint2"), radius = 1)
		cmds.pointConstraint(self.COMObject, joint1, maintainOffset = False)
		cmds.pointConstraint(projection, joint2, maintainOffset = False)
		cmds.setAttr(joint1 + ".overrideEnabled", 1)
		cmds.setAttr(joint2 + ".overrideEnabled", 1)
		cmds.setAttr(joint1 + ".overrideDisplayType", 2)
		cmds.setAttr(joint2 + ".overrideDisplayType", 2)
		cmds.parent(joint1, projection)

		cmds.select(clear = True)
	def COMConstrainToSelected(self, weight, *args):
		if (not self.COMObjectCheck()):
			return
		
		# Check selected objects
		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return
		
		selectedList.append(self.COMObject)
		Constraints.ConstrainListToLastElement(selected = selectedList, reverse = True, maintainOffset = False, parent = False, point = True, weight = weight)
	def COMDisconnectTargets(self, *args):
		if (self.COMObject == None or not cmds.objExists(self.COMObject)):
			cmds.warning("Center Of Mass object is not connected to script. Please select Center Of Mass object and press Activate button before")
			return

		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return
		
		selectedList.append(self.COMObject)
		Constraints.DisconnectTargetsFromConstraint(selectedList)
		cmds.select(selectedList[:-1], replace = True)


	### BAKING
	def BakeScenario2(self, *args):
		if (not self.COMObjectCheck()):
			return
		
		cmds.select(self.COMObject, add = True)
		selectedList = cmds.ls(selection = True)

		if (len(selectedList) == 1):
			cmds.warning("Need to select at least 1 object (except CenterOfMass joint)")
			cmds.select(clear = True)
			return

		self.CachedSelectedObjects = Locators.CreateAndBakeAsChildrenFromLastSelected(euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		return self.CachedSelectedObjects
	def BakeScenario3(self, *args):
		objects = self.BakeScenario2()
		if (objects == None):
			return None
		
		self.LinkCached(maintainOffset = False)
		
		return objects
	def BakeCached(self, *args):
		if (self.CachedSelectedObjects == None):
			cmds.warning("No cached objects yet, operation cancelled")
			return
		
		cmds.select(self.CachedSelectedObjects[0][0:-1])
		Baker.BakeSelected(euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		cmds.delete(self.CachedSelectedObjects[1][-1])
	
	def LinkCached(self, maintainOffset=False, *args):
		if (self.CachedSelectedObjects == None):
			cmds.warning("No cached objects yet, operation cancelled")
			return

		for i in range(len(self.CachedSelectedObjects[0])):
			if (i == len(self.CachedSelectedObjects[0]) - 1):
				return
			Constraints.ConstrainSecondToFirstObject(self.CachedSelectedObjects[1][i], self.CachedSelectedObjects[0][i], maintainOffset = maintainOffset)
	def SelectParent(self, *args):
		if (self.CachedSelectedObjects == None):
			cmds.warning("No cached objects yet, operation cancelled")
			return
		try:
			cmds.select(self.CachedSelectedObjects[1][-1])
		except:
			cmds.warning("Cached object not found")

