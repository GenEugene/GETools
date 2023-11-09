# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial
from utils import UI
from utils import Other
from utils import Baker
from utils import Colors
from utils import Constraints
from utils import Locators
from utils import Skinning
from utils import Timeline
from modules import GeneralWindow

class ToolsAnnotations:
	_textReverseConstraint = "After that parent constrain original objects back to locators"

	# Locators
	hideParent = "Deactivate vsibility on parent locator. \nUsually better o use with \"subLocator\" checkbox activated"
	subLocator = "Create an additional locator inside the main locator for additional local control"
	locator = "Create new locator on the world origin"
	locatorMatch = "Create and match locators to selected objects"
	locatorParent = "Create and parent constraint locators to selected objects"
	locatorsBake = "Create locators on selected objects and bake animation"
	locatorsBakeReverse = "{bake}\n{reverse}".format(bake = locatorsBake, reverse = _textReverseConstraint)
	locatorsRelative = "{bake}\nThe last locator becomes the parent of other locators".format(bake = locatorsBake)
	locatorsRelativeReverse = "{relative}\n{reverse}".format(relative = locatorsRelative, reverse = _textReverseConstraint)

	# Constraints
	_textAllSelectedConstrainToLast = "All selected objects will be constrained to last selected object"
	constraintReverse = "Reverse the direction of operation from last to first selected"
	constraintMaintain = "Use maintain offset"
	constraintParent = "Parent constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintPoint = "Point constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintOrient = "Orient constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintScale = "Scale constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)

class Tools:
	version = "v0.1.0"
	title = "TOOLS" + " " + version
	
	def __init__(self):
		self.checkboxLocatorHideParent = None
		self.checkboxLocatorSubLocator = None
		self.checkboxConstraintReverse = None
		self.checkboxConstraintMaintain = None
	def UILayout(self, layoutMain):
		settings = GeneralWindow.GeneralWindowSettings
		windowWidthMargin = settings.windowWidthMargin


		# LOCATORS
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = "CREATE LOCATORS", collapsable = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		self.checkboxLocatorHideParent = UI.Checkbox(label = "Hide Parent", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass", annotation = ToolsAnnotations.hideParent)
		self.checkboxLocatorSubLocator = UI.Checkbox(label = "Sub Locator", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass", annotation = ToolsAnnotations.subLocator)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Locator", command = self.CreateLocator, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locator)
		cmds.button(label = "Locators match", command = self.CreateLocatorMatch, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorMatch)
		cmds.button(label = "Locators parent", command = self.CreateLocatorParent, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorParent)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Locators bake", command = self.CreateLocatorBake, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorsBake)
		cmds.button(label = "Locators bake + reverse", command = self.CreateLocatorBakeReverse, backgroundColor = Colors.orange50, annotation = ToolsAnnotations.locatorsBakeReverse)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Locators relative", command = self.BakeAsChildrenFromLastSelected, backgroundColor = Colors.blue10, annotation = ToolsAnnotations.locatorsRelative)
		cmds.button(label = "Locators relative + reverse", command = self.BakeAsChildrenFromLastSelectedReverse, backgroundColor = Colors.blue50, annotation = ToolsAnnotations.locatorsRelativeReverse)
		

		# CONSTRAINTS
		layoutConstraints = cmds.frameLayout(parent = layoutMain, label = "CONSTRAINTS ( children --> parent )", collapsable = True)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutConstraints, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.separator(style = "none")
		self.checkboxConstraintReverse = UI.Checkbox(label = "Reverse", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass", annotation = ToolsAnnotations.constraintReverse)
		self.checkboxConstraintMaintain = UI.Checkbox(label = "Maintain", value = False, command = "pass", menuReset = False, enabled = True, ccResetAll = "pass", annotation = ToolsAnnotations.constraintMaintain)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutConstraints, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Parent", command = self.ConstrainParent, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintParent)
		cmds.button(label = "Point", command = self.ConstrainPoint, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintPoint)
		cmds.button(label = "Orient", command = self.ConstrainOrient, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintOrient)
		cmds.button(label = "Scale", command = self.ConstrainScale, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintScale)


		# RIGGING
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = "RIGGING", collapsable = True)
		#
		# countOffsets = 1
		# cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Copy Skin Weight From Last Selected", command = self.CopySkinWeightsFromLastMesh, backgroundColor = Colors.blue50)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Rotate order - SHOW", command = partial(Other.RotateOrderVisibility, True), backgroundColor = Colors.green10)
		cmds.button(label = "Rotate order - HIDE", command = partial(Other.RotateOrderVisibility, False), backgroundColor = Colors.green10)
		cmds.button(label = "Scale Compensate - ON", command = partial(Other.SegmentScaleCompensate, True), backgroundColor = Colors.lightBlue10)
		cmds.button(label = "Scale Compensate - OFF", command = partial(Other.SegmentScaleCompensate, False), backgroundColor = Colors.lightBlue10)
		cmds.button(label = "Joint - BONE", command = partial(Other.JointDrawStyle, 0), backgroundColor = Colors.yellow10)
		cmds.button(label = "Joint - HIDDEN", command = partial(Other.JointDrawStyle, 2), backgroundColor = Colors.yellow10)
		
		
		# BAKE
		layoutBake = cmds.frameLayout(parent = layoutMain, label = "BAKE", collapsable = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutBake, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Bake Classic", command = self.BakeSelectedClassic, backgroundColor = Colors.orange50)
		cmds.button(label = "Bake Classic Cut", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange50)
		cmds.button(label = "Bake Custom", command = self.BakeSelectedCustom, backgroundColor = Colors.orange100)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutBake, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Bake Selected By Last Object", command = self.BakeSelectedByLastObject, backgroundColor = Colors.orange100)
		
		
		# ANIMATION
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = "ANIMATION", collapsable = True)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Delete Nonkeyable Keys", command = Other.KeysNonkeyableDelete, backgroundColor = Colors.red10)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "Delete Animation", command = Other.DeleteKeys, backgroundColor = Colors.red100)
		cmds.button(label = "Delete Key Range", command = Other.DeleteKeyRange, backgroundColor = Colors.red50)
		#
		countOffsets = 7
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
		cmds.button(label = "<<", command = partial(Timeline.SetTime, 3), backgroundColor = Colors.green10)
		cmds.button(label = "<", command = partial(Timeline.SetTime, 1), backgroundColor = Colors.lightBlue10)
		cmds.button(label = ">", command = partial(Timeline.SetTime, 2), backgroundColor = Colors.lightBlue10)
		cmds.button(label = ">>", command = partial(Timeline.SetTime, 4), backgroundColor = Colors.green10)
		cmds.button(label = "OUTER", command = partial(Timeline.SetTime, 5), backgroundColor = Colors.blue10)
		cmds.button(label = "INNER", command = partial(Timeline.SetTime, 6), backgroundColor = Colors.blue10)
		cmds.button(label = "FOCUS", command = partial(Timeline.SetTime, 7), backgroundColor = Colors.orange10)


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

