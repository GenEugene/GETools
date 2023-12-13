# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial

from GETOOLS_SOURCE.utils import Baker
from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.utils import Constraints
from GETOOLS_SOURCE.utils import Locators
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Text

from GETOOLS_SOURCE.modules import Settings

class CenterOfMassAnnotations:
	# Setup
	create = "Create center of mass object. \nIt's just a simple joint that temporary stored in memory."
	activate = "Make selected center of mass object as active. \nUseful if you have more than one center of mass object or if you closed script or Maya.\
	\nCenter of mass must be activated if you want to use other features from script."
	select = "Select current activated center of mass object"
	clean = "Delete center of mass object"
	_projector = "Create extra object projected from center of mass to"
	projectorYZ = _projector + " YZ plane"
	projectorXZ = _projector + " XZ plane"
	projectorXY = _projector + " XY plane"

	# Weights
	disconnectTargets = "Disconnect selected objects from Center Of Mass"
	weightsCustom = "Custom weight"
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

	# Baking
	bakeToCOM = "Bake selected objects as locators relative to the center of mass object."
	bakeToCOMLink = "{0}\nAfter bake constrain selected objects back to locators.".format(bakeToCOM)
	bakeOriginal = "Bake animation back to original objects from locators."
	link = "Constrain cached objects to baked locators."
	linkOffset = "{0}\nUse maintain offset to keep transform difference".format(link)
	selectRoot = "Select root locator if exists"

class CenterOfMassSettings:
	COMRadius = 10 / 3
	weightMinMax = (0, 100)

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
	version = "v0.1.2"
	name = "CENTER OF MASS"
	title = name + " " + version

	def __init__(self):
		self.COMObject = None
		self.CachedSelectedObjects = None

		self.layoutSetup = None
		self.layoutWeights = None
		self.layoutBaking = None
	def UICreate(self, layoutMain):
		windowWidthMargin = Settings.windowWidthMargin
		lineHeight = Settings.lineHeight

		self.UILayoutSetup(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutWeights(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutBaking(layoutMain, windowWidthMargin, lineHeight)
	def UILayoutSetup(self, layoutMain, windowWidthMargin, lineHeight):
		self.layoutSetup = cmds.frameLayout(parent = layoutMain, label = "SETUP", collapsable = True) # , backgroundColor = Colors.blackWhite10
		layoutColumn = cmds.columnLayout(parent = self.layoutSetup, adjustableColumn = True)
		#
		COMButtons1 = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = COMButtons1, cellWidth = windowWidthMargin / COMButtons1, cellHeight = lineHeight)
		cmds.button(label = "CREATE", command = self.COMCreate, backgroundColor = Colors.green50, annotation = CenterOfMassAnnotations.create)
		cmds.button(label = "ACTIVATE", command = self.COMActivate, backgroundColor = Colors.yellow50, annotation = CenterOfMassAnnotations.activate)
		cmds.button(label = "SELECT", command = self.COMSelect, backgroundColor = Colors.lightBlue50, annotation = CenterOfMassAnnotations.select)
		cmds.button(label = "CLEAN", command = self.COMClean, backgroundColor = Colors.red50, annotation = CenterOfMassAnnotations.clean)
		#
		COMButtons2 = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = COMButtons2, cellWidth = windowWidthMargin / COMButtons2, cellHeight = lineHeight)
		cmds.button(label = "PROJECTOR YZ", command = partial(self.COMFloorProjection, "x"), backgroundColor = Colors.red10, annotation = CenterOfMassAnnotations.projectorYZ)
		cmds.button(label = "PROJECTOR XZ", command = partial(self.COMFloorProjection, "y"), backgroundColor = Colors.green10, annotation = CenterOfMassAnnotations.projectorXZ)
		cmds.button(label = "PROJECTOR XY", command = partial(self.COMFloorProjection, "z"), backgroundColor = Colors.blue10, annotation = CenterOfMassAnnotations.projectorXY)
	def UILayoutWeights(self, layoutMain, windowWidthMargin, lineHeight):
		self.layoutWeights = cmds.frameLayout(parent = layoutMain, label = "WEIGHTS", collapsable = True)
		layoutColumn = cmds.columnLayout(parent = self.layoutWeights, adjustableColumn = True)

		count = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		cmds.button(label = "Disconnect from Center Of Mass", command = self.COMDisconnectTargets, backgroundColor = Colors.red10, annotation = CenterOfMassAnnotations.disconnectTargets)
		
		def PartButton(partInfo = ("", 0), minMaxValue = CenterOfMassSettings.weightMinMax, onlyValue = False, annotation = ""):
			value = partInfo[1]
			text = "{1}" if onlyValue else "{0} {1}"
			colorValue = 1 - (value / (minMaxValue[1] - minMaxValue[0]))
			colorFinal = (colorValue, colorValue, colorValue)
			cmds.button(label = text.format(partInfo[0], value), command = partial(self.COMConstrainToSelected, value), backgroundColor = colorFinal, annotation = annotation)

		# WEIGHTS PALETTE
		count = 14
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		
		def CustomButton(value):
			PartButton(("", value), onlyValue = True, annotation = CenterOfMassAnnotations.weightsCustom)
		CustomButton(0)
		CustomButton(1)
		CustomButton(2)
		CustomButton(5)
		CustomButton(10)
		CustomButton(20)
		CustomButton(30)
		CustomButton(40)
		CustomButton(50)
		CustomButton(60)
		CustomButton(70)
		CustomButton(80)
		CustomButton(90)
		CustomButton(100)

		# BODYPARTS
		count = 3
		layoutBodyGrid = cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = 70) # 23.5 per 1 button
		
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
	def UILayoutBaking(self, layoutMain, windowWidthMargin, lineHeight):
		self.layoutBaking = cmds.frameLayout(parent = layoutMain, label = "BAKING", collapsable = True)

		count = 3
		cmds.gridLayout(numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)

		cmds.button(label = "BAKE TO COM", command = self.BakeScenario2, backgroundColor = Colors.orange10, annotation = CenterOfMassAnnotations.bakeToCOM)
		cmds.button(label = "BAKE + LINK", command = self.BakeScenario3, backgroundColor = Colors.orange50, annotation = CenterOfMassAnnotations.bakeToCOMLink)
		cmds.button(label = "BAKE ORIGINAL", command = self.BakeCached, backgroundColor = Colors.orange100, annotation = CenterOfMassAnnotations.bakeOriginal)
		
		cmds.button(label = "LINK", command = partial(self.LinkCached, False), backgroundColor = Colors.yellow10, annotation = CenterOfMassAnnotations.link)
		cmds.button(label = "LINK OFFSET", command = partial(self.LinkCached, True), backgroundColor = Colors.yellow10, annotation = CenterOfMassAnnotations.linkOffset)
		cmds.button(label = "SELECT ROOT", command = self.SelectParent, backgroundColor = Colors.lightBlue50, annotation = CenterOfMassAnnotations.selectRoot)


	# Center of mass functions
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
	def COMFloorProjection(self, skipAxis = "y", *args):
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
		Constraints.ConstrainListToLastElement(reverse = True, selected = selectedList, maintainOffset = False, parent = False, point = True, weight = weight)
	def COMDisconnectTargets(self, *args):
		if (self.COMObject == None or cmds.objExists(self.COMObject) == False):
			cmds.warning("Center Of Mass object is not connected to script. Please select Center Of Mass object and press Activate button before")
			return

		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return
		
		selectedList.append(self.COMObject)
		Constraints.DisconnectTargetsFromConstraint(selectedList)


	# Baking
	def BakeScenario2(self, *args):
		if (not self.COMObjectCheck()):
			return
		
		cmds.select(self.COMObject, add = True)
		selectedList = cmds.ls(selection = True)

		if (len(selectedList) == 1):
			cmds.warning("Need to select at least 1 object (except CenterOfMass joint)")
			cmds.select(clear = True)
			return

		# return self.BakeAsChildrenFromLastSelected(minSelectedCount = 1)
		self.CachedSelectedObjects = Locators.BakeAsChildrenFromLastSelected()
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
		Baker.BakeSelected()
		cmds.delete(self.CachedSelectedObjects[1][-1])
	
	def LinkCached(self, maintainOffset = False, *args):
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

