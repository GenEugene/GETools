import maya.cmds as cmds
from utils import Colors
from utils import UI
from utils import Constraints
from utils import Baker
from utils import Locators
from utils import Skinning

class Tools:
	def __init__(self):
		### SETUP
		self.version = "v0.0.1"
		self.titleText = "TOOLS"
		self.windowWidth = 294
		self.windowHeight = 10
		self.lineHeight = 20
		self.minMaxWeight = (0, 100)
		self.marginWidthHeight = 5
		### WINDOW
		self.window_name = "windowTools"
		### CHECKBOXES
		self.checkboxLocatorHideParent = None
		self.checkboxLocatorSubLocator = None
		self.checkboxConstraintReverse = None
		self.checkboxConstraintMaintain = None

	def CreateUI(self):
		# WINDOW
		if cmds.window(self.window_name, exists = True):
			cmds.deleteUI(self.window_name)
		cmds.window(self.window_name, title = self.titleText + " " + self.version, maximizeButton = False, sizeable = False, widthHeight = (self.windowWidth, self.windowHeight))
		cmds.window(self.window_name, edit = True, resizeToFitChildren = True) # , widthHeight = (self.windowWidth, self.windowHeight)
		layoutMain = cmds.columnLayout(adjustableColumn = False, width = self.windowWidth) # , h = self.windowHeight
		uiResize = self.ResizeUI
		# cmds.separator(style = "none") # "none", "single", "double", "singleDash", "doubleDash", "in" and "out".


		# LOCATORS
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = "CREATE LOCATORS", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		# cmds.separator(style = "none")
		self.checkboxLocatorHideParent = UI.Checkbox(label = "Hide Parent", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass")
		self.checkboxLocatorSubLocator = UI.Checkbox(label = "Sub Locator", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass")
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Locator", command = self.CreateLocator, backgroundColor = Colors.green10)
		cmds.button(label = "Locators match", command = self.CreateLocatorMatch, backgroundColor = Colors.green10)
		cmds.button(label = "Locators parent", command = self.CreateLocatorParent, backgroundColor = Colors.green10)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Locators bake", command = self.CreateLocatorBake, backgroundColor = Colors.orange10)
		cmds.button(label = "Locators bake + reverse", command = self.CreateLocatorBakeReverse, backgroundColor = Colors.orange50)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Locators relative", command = self.BakeAsChildrenFromLastSelected, backgroundColor = Colors.blue10)
		cmds.button(label = "Locators relative + reverse", command = self.BakeAsChildrenFromLastSelectedReverse, backgroundColor = Colors.blue50)
		

		# CONSTRAINTS
		layoutConstraints = cmds.frameLayout(parent = layoutMain, label = "CONSTRAINTS ( children --> parent )", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutConstraints, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.separator(style = "none")
		self.checkboxConstraintReverse = UI.Checkbox(label = "Reverse", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass")
		self.checkboxConstraintMaintain = UI.Checkbox(label = "Maintain", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass")
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutConstraints, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Parent", command = self.ConstrainParent, backgroundColor = Colors.red10)
		cmds.button(label = "Point", command = self.ConstrainPoint, backgroundColor = Colors.red10)
		cmds.button(label = "Orient", command = self.ConstrainOrient, backgroundColor = Colors.red10)
		cmds.button(label = "Scale", command = self.ConstrainScale, backgroundColor = Colors.red10)
		
		
		# BAKE
		layoutBake = cmds.frameLayout(parent = layoutMain, label = "BAKE", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutBake, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Bake Classic", command = self.BakeSelectedClassic, backgroundColor = Colors.orange50)
		cmds.button(label = "Bake Classic Cut", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange50)
		cmds.button(label = "Bake Custom", command = self.BakeSelectedCustom, backgroundColor = Colors.orange100)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutBake, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Bake Selected By Last Object", command = self.BakeSelectedByLastObject, backgroundColor = Colors.orange100)


		# RIGGING
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = "RIGGING", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "Copy Skin Weight From Last Selected", command = self.CopySkinWeightsFromLastMesh, backgroundColor = Colors.blue50)


		# RUN WINDOW
		cmds.showWindow(self.window_name)
		self.ResizeUI()
	def ResizeUI(self, *args):
		cmds.window(self.window_name, edit = True, height = 1, resizeToFitChildren = True)


	# LOCATORS
	def CreateLocator(self, *args):
		Locators.Create(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorMatch(self, *args):
		Locators.CreateOnSelected(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorParent(self, *args):
		Locators.CreateOnSelectedWithParentConstrain(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorBake(self, *args):
		Locators.CreateOnSelectedAndBake(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorBakeReverse(self, *args):
		Locators.CreateOnSelectedReverseConstraint(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get()) # TODO constrain to sub locator if exists
	def BakeAsChildrenFromLastSelected(self, *args):
		Locators.BakeAsChildrenFromLastSelected()
	def BakeAsChildrenFromLastSelectedReverse(self, *args):
		Locators.BakeAsChildrenFromLastSelectedReverse()
	

	# CONSTRAINTS
	def ConstrainParent(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.checkboxConstraintReverse.Get(), maintainOffset = self.checkboxConstraintMaintain.Get(), parent = True, point = False, orient = False, scale = False)
	def ConstrainPoint(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.checkboxConstraintReverse.Get(), maintainOffset = self.checkboxConstraintMaintain.Get(), parent = False, point = True, orient = False, scale = False)
	def ConstrainOrient(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.checkboxConstraintReverse.Get(), maintainOffset = self.checkboxConstraintMaintain.Get(), parent = False, point = False, orient = True, scale = False)
	def ConstrainScale(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.checkboxConstraintReverse.Get(), maintainOffset = self.checkboxConstraintMaintain.Get(), parent = False, point = False, orient = False, scale = True)
	
	
	# BAKER
	def BakeSelectedClassic(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True)
	def BakeSelectedClassicCut(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = False)
	def BakeSelectedCustom(self, *args):
		Baker.BakeSelected(classic = False, preserveOutsideKeys = True)
	def BakeSelectedByLastObject(self, *args):
		Baker.BakeSelectedByLastObject()
	
	# RIGGING
	def CopySkinWeightsFromLastMesh(self, *args):
		Skinning.CopySkinWeightsFromLastMesh();


	# EXECUTION
	def RUN(self, *args):
		Tools().CreateUI()


# Tools().RUN()