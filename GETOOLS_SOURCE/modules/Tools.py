# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial

from GETOOLS_SOURCE.utils import Baker
from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.utils import Constraints
from GETOOLS_SOURCE.utils import Locators
from GETOOLS_SOURCE.utils import Other
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Skinning
from GETOOLS_SOURCE.utils import Timeline
from GETOOLS_SOURCE.utils import UI

from GETOOLS_SOURCE.modules import Settings

class ToolsAnnotations:
	# Other
	selectTransformHiererchy = "Select all children \"transform\" objects. \nWorks with multiple selected objects"
	printSelectedToConsole = "Just print all selected objects to console and count them"

	# Locators
	hideParent = "Deactivate vsibility on parent locator. \nUsually better o use with \"subLocator\" checkbox activated"
	subLocator = "Create an additional locator inside the main locator for additional local control"
	locator = "Create new locator on the world origin"
	locatorMatch = "Create and match locators to selected objects"
	locatorParent = "Create and parent constraint locators to selected objects"
	locatorsBake = "Create locators on selected objects and bake animation"
	_reverseConstraint = "After that parent constrain original objects back to locators"
	locatorsBakeReverse = "{bake}\n{reverse}".format(bake = locatorsBake, reverse = _reverseConstraint)
	locatorsRelative = "{bake}\nThe last locator becomes the parent of other locators".format(bake = locatorsBake)
	locatorsRelativeReverse = "{relative}\n{reverse}\nRight click allows you to bake the same operation but with constrained last object.".format(relative = locatorsRelative, reverse = _reverseConstraint)

	# Constraints
	_textAllSelectedConstrainToLast = "All selected objects will be constrained to last selected object"
	constraintReverse = "Reverse the direction of operation from last to first selected"
	constraintMaintain = "Use maintain offset"
	constraintParent = "Parent constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintPoint = "Point constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintOrient = "Orient constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintScale = "Scale constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintAim = "[IN DEVELOPMENT]\nAim constrain.".format(allToLast = _textAllSelectedConstrainToLast) # TODO

	# Rigging
	_rotateOrder = "rotate order attribute in channel box for all selected objects"
	rotateOrderShow = "Show {0}".format(_rotateOrder)
	rotateOrderHide = "Hide {0}".format(_rotateOrder)
	_scaleCompensate = "segment scale compensate attribute for all selected joints"
	scaleCompensateOn = "Activate {0}".format(_scaleCompensate)
	scaleCompensateOff = "Deactivate {0}".format(_scaleCompensate)
	_jointDrawStyle = "selected joints draw style"
	jointDrawStyleBone = "Bone {0}".format(_jointDrawStyle)
	jointDrawStyleHidden = "Hidden {0}".format(_jointDrawStyle)
	copySkinWeights = "Copy skin weights from last selected object to all other selected objects"

	# Bake
	bakeClassic = "Regular maya bake \"Edit/Keys/Bake Simulation\""
	bakeClassicCut = "{0}. Keys outside of time range will be removed".format(bakeClassic)
	bakeCustom = "Alternative way to bake.\nThe same if you just set key every frame on time range.\nAlso works with animation layers."
	bakeByLast = "Bake selected objects relative to the last selected object as if they were constrained"

	# Animation
	deleteNonkeyableKeys = "Delete animation on all nonkeyable attributes of selected objects"
	deleteAnimation = "Delete all animation from selected objects"
	deleteKeyRange = "Delete selected time range keys of selected objects. \nAlso works with selected attributes in Channel Box"

	timelineSetMinOuter = "Set minimal outer timeline value"
	timelineSetMinInner = "Set minimal inner timeline value"
	timelineSetMaxInner = "Set maximum inner timeline value"
	timelineSetMaxOuter = "Set maximum outer timeline value"
	timelineExpandOuter = "Expand timeline range to outer range"
	timelineExpandInner = "Expand timeline range to inner range"
	timelineFocusRange = "Set timeline inner range on selected range by mouse"

class Tools:
	version = "v0.1.2"
	name = "TOOLS"
	title = name + " " + version
	
	def __init__(self):
		self.checkboxLocatorHideParent = None
		self.checkboxLocatorSubLocator = None
		self.checkboxConstraintReverse = None
		self.checkboxConstraintMaintain = None
	
	def UICreate(self, layoutMain):
		windowWidthMargin = Settings.windowWidthMargin
		lineHeight = Settings.lineHeight


		# SELECT
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = "SELECT", collapsable = True)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Print Selected\nTo Console", command = Selector.PrintSelected, backgroundColor = Colors.blackWhite90, annotation = ToolsAnnotations.printSelectedToConsole)
		cmds.button(label = "Select Transform\nHiererchy", command = Selector.SelectTransformHierarchy, backgroundColor = Colors.blue10, annotation = ToolsAnnotations.selectTransformHiererchy)
		
		# LOCATORS
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = "LOCATORS", collapsable = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		self.checkboxLocatorHideParent = UI.Checkbox(label = "Hide Parent", value = False, menuReset = False, enabled = True, annotation = ToolsAnnotations.hideParent)
		self.checkboxLocatorSubLocator = UI.Checkbox(label = "Sub Locator", value = False, menuReset = False, enabled = True, annotation = ToolsAnnotations.subLocator)
		cmds.separator(style = "none")
		#
		cmds.button(label = "Locator", command = self.CreateLocator, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locator)
		cmds.button(label = "Locators match", command = self.CreateLocatorMatch, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorMatch)
		cmds.button(label = "Locators parent", command = self.CreateLocatorParent, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorParent)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutLocators, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Locators bake", command = self.CreateLocatorBake, backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.locatorsBake)
		cmds.button(label = "Locators bake + reverse", command = self.CreateLocatorBakeReverse, backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverse)
		cmds.button(label = "Locators relative", command = self.BakeAsChildrenFromLastSelected, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorsRelative)
		cmds.button(label = "Locators relative + reverse", command = self.BakeAsChildrenFromLastSelectedReverse, backgroundColor = Colors.orange50, annotation = ToolsAnnotations.locatorsRelativeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "skip last object constrain", command = self.BakeAsChildrenFromLastSelectedReverseSkipLast)
		

		# CONSTRAINTS
		layoutConstraints = cmds.frameLayout(parent = layoutMain, label = "CONSTRAINTS", collapsable = True)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutConstraints, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.separator(style = "none")
		self.checkboxConstraintReverse = UI.Checkbox(label = "Reverse", value = False, menuReset = False, enabled = True, annotation = ToolsAnnotations.constraintReverse)
		self.checkboxConstraintMaintain = UI.Checkbox(label = "Maintain", value = False, menuReset = False, enabled = True, annotation = ToolsAnnotations.constraintMaintain)
		cmds.separator(style = "none")
		#
		countOffsets = 5
		cmds.gridLayout(parent = layoutConstraints, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Parent", command = self.ConstrainParent, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintParent)
		cmds.button(label = "Point", command = self.ConstrainPoint, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintPoint)
		cmds.button(label = "Orient", command = self.ConstrainOrient, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintOrient)
		cmds.button(label = "Scale", command = self.ConstrainScale, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintScale)
		cmds.button(label = "Aim", command = self.ConstrainParent, backgroundColor = Colors.red10, annotation = ToolsAnnotations.constraintAim, enable = False) # TODO


		# RIGGING
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = "RIGGING", collapsable = True)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Rotate order\nSHOW", command = partial(Other.RotateOrderVisibility, True), backgroundColor = Colors.green10, annotation = ToolsAnnotations.rotateOrderShow)
		cmds.button(label = "Rotate order\nHIDE", command = partial(Other.RotateOrderVisibility, False), backgroundColor = Colors.green10, annotation = ToolsAnnotations.rotateOrderHide)
		cmds.button(label = "Segment Scale\nCompensate ON", command = partial(Other.SegmentScaleCompensate, True), backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.scaleCompensateOn)
		cmds.button(label = "Segment Scale\nCompensate OFF", command = partial(Other.SegmentScaleCompensate, False), backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.scaleCompensateOff)
		cmds.button(label = "Joint\nBONE", command = partial(Other.JointDrawStyle, 0), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.jointDrawStyleBone)
		cmds.button(label = "Joint\nHIDDEN", command = partial(Other.JointDrawStyle, 2), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.jointDrawStyleHidden)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Copy Skin Weights\nFrom Last Selected", command = self.CopySkinWeightsFromLastMesh, backgroundColor = Colors.blue10, annotation = ToolsAnnotations.copySkinWeights)
		# cmds.separator(style = "none")
		
		
		# BAKE
		layoutBake = cmds.frameLayout(parent = layoutMain, label = "BAKE", collapsable = True)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutBake, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Bake Classic", command = self.BakeSelectedClassic, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassic)
		cmds.button(label = "Bake Classic\nCut Outer", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassicCut)
		cmds.button(label = "Bake Custom", command = self.BakeSelectedCustom, backgroundColor = Colors.orange50, annotation = ToolsAnnotations.bakeCustom)
		cmds.button(label = "Bake Selected\nBy Last Object", command = self.BakeSelectedByLastObject, backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLast)
		
		
		# ANIMATION
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = "ANIMATION", collapsable = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Delete\nAnimation", command = Other.DeleteKeys, backgroundColor = Colors.red100, annotation = ToolsAnnotations.deleteAnimation)
		cmds.button(label = "Delete\nKey Range", command = Other.DeleteKeyRange, backgroundColor = Colors.red50, annotation = ToolsAnnotations.deleteKeyRange)
		cmds.button(label = "Delete\nNonkeyable Keys", command = Other.KeysNonkeyableDelete, backgroundColor = Colors.red10, annotation = ToolsAnnotations.deleteNonkeyableKeys)
		#
		countOffsets = 7
		cmds.gridLayout(parent = layoutRigging, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "<<", command = partial(Timeline.SetTime, 3), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMinOuter)
		cmds.button(label = "<", command = partial(Timeline.SetTime, 1), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.timelineSetMinInner)
		cmds.button(label = ">", command = partial(Timeline.SetTime, 2), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.timelineSetMaxInner)
		cmds.button(label = ">>", command = partial(Timeline.SetTime, 4), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMaxOuter)
		cmds.button(label = "OUTER", command = partial(Timeline.SetTime, 5), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.timelineExpandOuter)
		cmds.button(label = "INNER", command = partial(Timeline.SetTime, 6), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.timelineExpandInner)
		cmds.button(label = "FOCUS", command = partial(Timeline.SetTime, 7), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineFocusRange)


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
		Locators.CreateOnSelectedReverseConstrain(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get())
	def BakeAsChildrenFromLastSelected(self, *args):
		Locators.BakeAsChildrenFromLastSelected(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get())
	def BakeAsChildrenFromLastSelectedReverseSkipLast(self, *args):
		Locators.BakeAsChildrenFromLastSelectedReverse(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get(), skipLastReverse = True)
	def BakeAsChildrenFromLastSelectedReverse(self, *args):
		Locators.BakeAsChildrenFromLastSelectedReverse(hideParent = self.checkboxLocatorHideParent.Get(), subLocators = self.checkboxLocatorSubLocator.Get(), skipLastReverse = False)
	

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

