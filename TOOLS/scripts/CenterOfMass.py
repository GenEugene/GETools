import maya.cmds as cmds
from functools import partial
from utils import Colors
from utils import Text
from utils import Selector
from utils import Baker
from utils import Constraints
from utils import Locators

class CenterOfMass:
	def __init__(self):
		### SETUP
		self.version = "v0.0.1"
		self.titleText = "CENTER OF MASS"
		self.windowWidth = 294
		self.windowHeight = 10
		self.lineHeight = 20
		self.minMaxWeight = (0, 100)

		### WINDOW
		self.window_name = "windowCenterOfMass"

		### CENTER OF MASS OBJECTS
		self.COMRadius = 10

		### BODYPARTS MAPPING PERCENTAGE
		self.partHead = ("head", 7.3)
		self.partChest = ("chest", 35.8)
		self.partAbdomen = ("abdomen", 10.1)
		self.partShoulder = ("shoulder", 3.1)
		self.partElbow = ("elbow", 1.7)
		self.partHand = ("hand ", 0.8)
		self.partThigh = ("thigh", 11.5)
		self.partKnee = ("knee", 4.4)
		self.partFoot = ("foot", 1.9)
		#
		self.partChestAbdomen = ("torso", 45.9)
		self.partShoulderElbow = ("arm", 4.8)
		self.partThighKnee = ("leg", 15.9)

		### OBJECTS
		self.COMObject = None
		self.CachedSelectedObjects = None
	def CreateUI(self):
		## WINDOW
		if cmds.window(self.window_name, exists = True):
			cmds.deleteUI(self.window_name)
		cmds.window(self.window_name, title = self.titleText + " " + self.version, maximizeButton = False, sizeable = False, widthHeight = (self.windowWidth, self.windowHeight))
		cmds.window(self.window_name, edit = True, resizeToFitChildren = True) # , widthHeight = (self.windowWidth, self.windowHeight)
		layoutMain = cmds.columnLayout(adjustableColumn = False, width = self.windowWidth) # , h = self.windowHeight

		self.UILayout(layoutMain)

		cmds.showWindow(self.window_name)

		return self.window_name # XXX
	
	def UILayout(self, layoutMain, mainWindow = None): # TODO get values from GeneralWindow
		print("*****")
		print(layoutMain)
		# print(mainWindow)
		print("*****")


		## CENTER OF MASS LOCATOR
		layoutCOM = cmds.frameLayout(parent = layoutMain, label = "SETUP", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10)
		#
		COMButtons1 = 4
		cmds.gridLayout(numberOfColumns = COMButtons1, cellWidth = self.windowWidth / COMButtons1)
		cmds.button(label = "CREATE", command = self.COMCreate, backgroundColor = Colors.green50)
		cmds.button(label = "ACTIVATE", command = self.COMActivate, backgroundColor = Colors.yellow50)
		cmds.button(label = "SELECT", command = self.COMSelect, backgroundColor = Colors.lightBlue50)
		cmds.button(label = "CLEAN", command = self.COMClean, backgroundColor = Colors.red50)
		#
		COMButtons2 = 3
		cmds.gridLayout(parent = layoutCOM, numberOfColumns = COMButtons2, cellWidth = self.windowWidth / COMButtons2)
		cmds.button(label = "PROJECTOR YZ", command = partial(self.COMFloorProjection, "x"), backgroundColor = Colors.red10)
		cmds.button(label = "PROJECTOR XZ", command = partial(self.COMFloorProjection, "y"), backgroundColor = Colors.green10)
		cmds.button(label = "PROJECTOR XY", command = partial(self.COMFloorProjection, "z"), backgroundColor = Colors.blue10)


		## WEIGHTS
		layoutWeights = cmds.frameLayout(parent = layoutMain, label = "WEIGHTS", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10)
		
		# CUSTOM WEIGHTS
		def PartButton(partInfo=("", 0), minMaxValue = self.minMaxWeight, onlyValue=False):
			value = partInfo[1]
			text = "{1}" if onlyValue else "{0} {1}"
			colorValue = 1 - (value / (minMaxValue[1] - minMaxValue[0]))
			colorFinal = (colorValue, colorValue, colorValue)
			cmds.button(label = text.format(partInfo[0], value), command = partial(self.COMConstrainToSelected, value), backgroundColor = colorFinal)

		countCustom = 14
		cmds.frameLayout(parent = layoutWeights, label = "Manual", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite40)
		cmds.gridLayout(numberOfColumns = countCustom, cellWidth = self.windowWidth / countCustom)
		def CustomButton(value):
			PartButton(("", value), onlyValue = True)
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
		countBodyparts = 3
		cmds.frameLayout(parent = layoutWeights, label = "Humanoid Bodyparts Percentage", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite40)
		layoutBodyGrid = cmds.gridLayout(numberOfColumns = countBodyparts, cellWidth = self.windowWidth / countBodyparts, cellHeight = 94)
		#
		cmds.columnLayout(parent = layoutBodyGrid, adjustableColumn = True, width = self.windowWidth)
		PartButton(self.partHead, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partChest, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partAbdomen, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partChestAbdomen, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		#
		cmds.columnLayout(parent = layoutBodyGrid, adjustableColumn = True, width = self.windowWidth)
		PartButton(self.partShoulder, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partElbow, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partHand, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partShoulderElbow, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		#
		cmds.columnLayout(parent = layoutBodyGrid, adjustableColumn = True, width = self.windowWidth)
		PartButton(self.partThigh, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partKnee, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partFoot, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))
		PartButton(self.partThighKnee, minMaxValue = (self.partHand[1], self.partChestAbdomen[1]))


		## BAKING
		countBaking1 = 3
		layoutBaking = cmds.frameLayout(parent = layoutMain, label = "BAKING", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10)
		cmds.gridLayout(numberOfColumns = countBaking1, cellWidth = self.windowWidth / countBaking1)
		#
		cmds.button(label = "BAKE TO LAST", command = self.BakeScenario1, backgroundColor = Colors.orange10)
		cmds.button(label = "BAKE TO COM", command = self.BakeScenario2, backgroundColor = Colors.orange50)
		cmds.button(label = "BAKE + LINK", command = self.BakeScenario3, backgroundColor = Colors.orange100)
		#
		countBaking2 = 2
		cmds.gridLayout(parent = layoutBaking, numberOfColumns = countBaking2, cellWidth = self.windowWidth / countBaking2)
		cmds.button(label = "LINK MATCH", command = partial(self.LinkCached, False), backgroundColor = Colors.yellow10)
		cmds.button(label = "LINK OFFSET", command = partial(self.LinkCached, True), backgroundColor = Colors.yellow10)
		#
		countBaking3 = 2
		cmds.gridLayout(parent = layoutBaking, numberOfColumns = countBaking3, cellWidth = self.windowWidth / countBaking3)
		cmds.button(label = "SELECT PARENT", command = self.SelectParent, backgroundColor = Colors.lightBlue50)
		cmds.button(label = "BAKE ORIGINAL", command = self.BakeCached, backgroundColor = Colors.red50)


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
		# self.COMObjectRef = cmds.polyPrimitive(name = "objCenterOfMass", radius = self.COMRadius, polyType = 0, constructionHistory = 0)
		# cmds.polySoftEdge(angle = 0, constructionHistory = 0)
		# self.COMGroupRef = cmds.group(name = "grpCenterOfMass")
		
		cmds.select(clear = True)
		self.COMObject = cmds.joint(name = Text.SetUniqueFromText("objCenterOfMass"), radius = self.COMRadius / 3)
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
		projection = cmds.polyPrimitive(name = Text.SetUniqueFromText(name), radius = self.COMRadius / 3, polyType = 0, constructionHistory = 0)
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
		Constraints.ConstrainListToLastElement(reverse = True, selectedList = selectedList, maintainOffset = False, parent = False, point = True, weight = weight)
	
	# def COMRemove(self, weight, *args): # TODO
	# 	if (self.COMObjectCheck()):
	# 		# Check selected objects
	# 		selectedList = Selector.MultipleObjects(1)
	# 		if (selectedList == None):
	# 			return
		
		# children = cmds.listRelatives(self.COMObjectRef, type = "constraint")
		# if (children > 0):
		# 	attributes = cmds.listAttr(children[0])
		# pass

	
	def BakeAsChildrenFromLastSelected(self, minSelectedCount = 2, *args):
		self.CachedSelectedObjects = Locators.BakeAsChildrenFromLastSelected(minSelectedCount = minSelectedCount)
		# self.CachedSelectedObjects = Locators.CreateOnSelectedAndBake("locBaked", minSelectedCount, parentToLastSelected = True)
		# if (self.CachedSelectedObjects == None):
		# 	return None
		# cmds.select(self.CachedSelectedObjects[1][-1])
		return self.CachedSelectedObjects
	
	def BakeScenario1(self, *args):
		return self.BakeAsChildrenFromLastSelected()
	def BakeScenario2(self, *args):
		if (not self.COMObjectCheck()):
			return
		
		cmds.select(self.COMObject, add = True)
		selectedList = cmds.ls(selection = True)

		if (len(selectedList) == 1):
			cmds.warning("Need to select at least 1 object (except CenterOfMass joint)")
			cmds.select(clear = True)
			return

		return self.BakeAsChildrenFromLastSelected(minSelectedCount = 1)
	def BakeScenario3(self, *args):
		objects = self.BakeScenario2()
		if (objects == None):
			return None
		
		self.LinkCached(maintainOffset = False)
		
		return objects
	
	def SelectParent(self, *args):
		if (self.CachedSelectedObjects == None):
			cmds.warning("No cached objects yet, operation cancelled")
			return
		cmds.select(self.CachedSelectedObjects[1][-1])
	
	def LinkCached(self, maintainOffset=False, *args):
		if (self.CachedSelectedObjects == None):
			cmds.warning("No cached objects yet, operation cancelled")
			return

		for i in range(len(self.CachedSelectedObjects[0])):
			if (i == len(self.CachedSelectedObjects[0]) - 1):
				return
			Constraints.ConstrainSecondToFirstObject(self.CachedSelectedObjects[1][i], self.CachedSelectedObjects[0][i], maintainOffset = maintainOffset)
	def BakeCached(self, *args):
		if (self.CachedSelectedObjects == None):
			cmds.warning("No cached objects yet, operation cancelled")
			return
		
		cmds.select(self.CachedSelectedObjects[0][0:-1])
		Baker.BakeSelected()
		cmds.delete(self.CachedSelectedObjects[1][-1])


	# EXECUTION
	def RUN(self, *args):
		return CenterOfMass().CreateUI()


# CenterOfMass().RUN()