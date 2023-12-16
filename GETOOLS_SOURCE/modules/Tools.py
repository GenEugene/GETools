# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial

from GETOOLS_SOURCE.utils import Animation
from GETOOLS_SOURCE.utils import Baker
from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.utils import Locators
from GETOOLS_SOURCE.utils import Timeline
from GETOOLS_SOURCE.utils import UI

from GETOOLS_SOURCE.modules import Settings

class ToolsAnnotations:
	# Other
	# printSelectedToConsole = "Just print all selected objects to console and count them"
	# selectTransformHiererchy = "Select all children \"transform\" objects. \nWorks with multiple selected objects"

	# Locators
	hideParent = "Deactivate visibility on parent locator. \nUsually better to use with \"Sub Locator\" checkbox activated"
	subLocator = "Create an extra locator inside the main locator for additional local control"
	locatorSize = "Initial size of locator"
	locator = "Create new locator on the world origin"
	locatorMatch = "Create and match locators to selected objects"
	locatorParent = "Create and parent constraint locators to selected objects"
	locatorsBake = "Create locators on selected objects and bake animation"
	_reverseConstraint = "After that parent constrain original objects back to locators"
	locatorsBakeReverse = "{bake}\n{reverse}".format(bake = locatorsBake, reverse = _reverseConstraint)
	locatorsBakeReversePos = "Only for Translation\n{bake}".format(bake = locatorsBakeReverse)
	locatorsBakeReverseRot = "Only for Rotation\n{bake}".format(bake = locatorsBakeReverse)
	
	locatorsRelative = "{bake}\nThe last locator becomes the parent of other locators".format(bake = locatorsBake)
	locatorsRelativeReverse = "{relative}\n{reverse}\nRight click allows you to bake the same operation but with constrained last object.".format(relative = locatorsRelative, reverse = _reverseConstraint)
	locatorsBakeAim = "Bake locators for Aim Space Switching"
	locatorAimDistance = "Locator Aim distance from original object. Need to use non-zero value"

	# Bake
	bakeSamples = "Baking sample rate.\nDefault value is 1.\nMinimal value is 0.001"
	_bakeCutOutside = "Keys outside of time range or selected range will be removed"
	bakeClassic = "Regular maya bake \"Edit/Keys/Bake Simulation\".\nUse sample rate."
	bakeClassicCut = "{0}.\n{1}".format(bakeClassic, _bakeCutOutside)
	bakeCustom = "Alternative way to bake. Doesn't support Sample Rate.\nThe same if you just set key every frame on time range.\nAlso works with animation layers."
	bakeCustomCut = "{0}\n{1}".format(bakeCustom, _bakeCutOutside)
	bakeByLast = "Bake selected objects relative to the last selected object as if they were constrained.\nUse sample rate."

	# Animation
	deleteAnimation = "Delete all animation from selected objects"
	deleteKeyRange = "Delete selected time range keys of selected objects. \nAlso works with selected attributes in Channel Box"
	deleteNonkeyableKeys = "Delete animation on all nonkeyable attributes of selected objects"
	deleteStaticCurves = "Delete all static curves on selected"
	filterCurve = "Filter curve by euler filter. Fix some curve issues"
	animationCurveInfinity = "Curve Infinity"

	timelineSetMinOuter = "Set minimal outer timeline value"
	timelineSetMinInner = "Set minimal inner timeline value"
	timelineSetMaxInner = "Set maximum inner timeline value"
	timelineSetMaxOuter = "Set maximum outer timeline value"
	timelineExpandOuter = "Expand timeline range to outer range"
	timelineExpandInner = "Expand timeline range to inner range"
	timelineFocusRange = "Set timeline inner range on selected range by mouse"

class ToolsSettings:
	# SLIDERS (field min/max, slider min/max)
	rangeLocatorAimOffset = (0, float("inf"), 0, 200)

class Tools:
	version = "v0.1.5"
	name = "TOOLS"
	title = name + " " + version

	def __init__(self):
		self.checkboxLocatorHideParent = None
		self.checkboxLocatorSubLocator = None
		self.floatLocatorSize = None
		self.floatLocatorAimOffset = None
		self.fieldBakingSamples = None
	def UICreate(self, layoutMain):
		windowWidthMargin = Settings.windowWidthMargin
		lineHeight = Settings.lineHeight
		sliderWidth = Settings.sliderWidth
		sliderWidthMarker = Settings.sliderWidthMarker

		self.UILayoutLocators(layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker)
		self.UILayoutBaking(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutAnimation(layoutMain, windowWidthMargin, lineHeight)
	def UILayoutLocators(self, layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker):
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = "LOCATORS / SPACE SWITCHING", collapsable = True)
		layoutColumn = cmds.columnLayout(parent = layoutLocators, adjustableColumn = True)
		#
		countOffsets = 3
		cellWidth = windowWidthMargin / countOffsets
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = cellWidth, cellHeight = lineHeight)
		self.checkboxLocatorHideParent = UI.Checkbox(label = "Hide Parent", value = False, annotation = ToolsAnnotations.hideParent)
		self.checkboxLocatorSubLocator = UI.Checkbox(label = "Sub Locator", value = False, annotation = ToolsAnnotations.subLocator)
		self.floatLocatorSize = UI.FloatField(value = 10, precision = 3, annotation = ToolsAnnotations.locatorSize)
		# self.floatLocatorSize = UI.FloatFieldButtons(value = 5, precision = 3, annotation = ToolsAnnotations.locatorSize, width = cellWidth * 0.9, height = lineHeight, commandUp = "", commandDown = "") # TODO
		#
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Locator", command = self.CreateLocator, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locator)
		cmds.button(label = "Match", command = self.CreateLocatorMatch, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorMatch)
		cmds.button(label = "Parent", command = self.CreateLocatorParent, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorParent)
		cmds.button(label = "PIN", command = partial(self.CreateLocatorBakeReverse, True, True), backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.locatorsBakeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "without reverse constraint", command = self.CreateLocatorBake)
		cmds.button(label = "Pin\nPOS", command = partial(self.CreateLocatorBakeReverse, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReversePos)
		cmds.button(label = "Pin\nROT", command = partial(self.CreateLocatorBakeReverse, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverseRot)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Relative", command = self.BakeAsChildrenFromLastSelectedReverse, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorsRelativeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "skip last object reverse constraint", command = self.BakeAsChildrenFromLastSelectedReverseSkipLast)
		cmds.menuItem(label = "without reverse constraint", command = self.BakeAsChildrenFromLastSelected)
		#
		layoutAim = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = windowWidthMargin, cellHeight = lineHeight)
		countOffsets = 6
		labelLocalSpace = "without reverse constraint"
		cmds.gridLayout(parent = layoutAim, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "-X", command = partial(self.CreateLocatorBakeAim, 1, True), backgroundColor = Colors.red10, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.CreateLocatorBakeAim, 1, False))
		cmds.button(label = "+X", command = partial(self.CreateLocatorBakeAim, 2, True), backgroundColor = Colors.red50, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.CreateLocatorBakeAim, 2, False))
		cmds.button(label = "-Y", command = partial(self.CreateLocatorBakeAim, 3, True), backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.CreateLocatorBakeAim, 3, False))
		cmds.button(label = "+Y", command = partial(self.CreateLocatorBakeAim, 4, True), backgroundColor = Colors.green50, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.CreateLocatorBakeAim, 4, False))
		cmds.button(label = "-Z", command = partial(self.CreateLocatorBakeAim, 5, True), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.CreateLocatorBakeAim, 5, False))
		cmds.button(label = "+Z", command = partial(self.CreateLocatorBakeAim, 6, True), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.CreateLocatorBakeAim, 6, False))
		self.floatLocatorAimOffset = UI.Slider(
			parent = layoutAim,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			# command = ,
			label = "Distance",
			annotation = ToolsAnnotations.locatorAimDistance,
			value = 100,
			minMax = ToolsSettings.rangeLocatorAimOffset,
			precision = 3,
			menuReset = True,
		)
	def UILayoutBaking(self, layoutMain, windowWidthMargin, lineHeight):
		layoutBake = cmds.frameLayout(parent = layoutMain, label = "BAKING", collapsable = True)
		layoutColumn = cmds.columnLayout(parent = layoutBake, adjustableColumn = True)
		#
		countOffsets = 6
		cellWidth = windowWidthMargin / countOffsets
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = cellWidth, cellHeight = lineHeight)
		cmds.button(label = "1", command = partial(self.BakeSamplesSet, 1), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "2", command = partial(self.BakeSamplesSet, 2), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "3", command = partial(self.BakeSamplesSet, 3), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "4", command = partial(self.BakeSamplesSet, 4), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		UI.ButtonLeftRight(width = cellWidth, height = lineHeight, commandLeft = partial(self.BakeSamplesAdd, -1), commandRight = partial(self.BakeSamplesAdd, 1), backgroundColor = Colors.lightBlue50, annotation = ToolsAnnotations.bakeSamples)
		self.fieldBakingSamples = UI.FloatField(value = 1, precision = 3, minValue = 0.001, annotation = ToolsAnnotations.bakeSamples)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Bake Classic", command = self.BakeSelectedClassic, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassic)
		cmds.button(label = "Bake Classic\nCut Outer", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassicCut)
		cmds.button(label = "Bake Custom", command = self.BakeSelectedCustom, backgroundColor = Colors.orange50, annotation = ToolsAnnotations.bakeCustom)
		cmds.button(label = "Bake Custom\nCut Outer", command = self.BakeSelectedCustomCut, backgroundColor = Colors.orange50, annotation = ToolsAnnotations.bakeCustomCut)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Bake Selected\nBy Last Object", command = self.BakeSelectedByLastObject, backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLast) # TODO rework
	def UILayoutAnimation(self, layoutMain, windowWidthMargin, lineHeight):
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = "ANIMATION", collapsable = True)
		layoutColumn = cmds.columnLayout(parent = layoutRigging, adjustableColumn = True)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Delete\nAnimation", command = Animation.DeleteKeys, backgroundColor = Colors.red100, annotation = ToolsAnnotations.deleteAnimation)
		cmds.button(label = "Delete\nKey Range", command = Animation.DeleteKeyRange, backgroundColor = Colors.red50, annotation = ToolsAnnotations.deleteKeyRange)
		cmds.button(label = "Delete\nNonkeyable", command = Animation.DeleteKeysNonkeyable, backgroundColor = Colors.red10, annotation = ToolsAnnotations.deleteNonkeyableKeys)
		cmds.button(label = "Delete\nStatic", command = Animation.DeleteStaticCurves, backgroundColor = Colors.blackWhite80, annotation = ToolsAnnotations.deleteStaticCurves)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Euler Filter", command = Animation.FilterCurve, backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.filterCurve)
		#
		countOffsets = 5
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Constant", command = partial(Animation.SetInfinity, 1, None), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Linear", command = partial(Animation.SetInfinity, 2, None), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Cycle", command = partial(Animation.SetInfinity, 3, None), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Offset", command = partial(Animation.SetInfinity, 4, None), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Oscillate", command = partial(Animation.SetInfinity, 5, None), backgroundColor = Colors.blue100, annotation = ToolsAnnotations.animationCurveInfinity)
		#
		countOffsets = 7
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "<<", command = partial(Timeline.SetTime, 3), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMinOuter)
		cmds.button(label = "<", command = partial(Timeline.SetTime, 1), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMinInner)
		cmds.button(label = ">", command = partial(Timeline.SetTime, 2), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMaxInner)
		cmds.button(label = ">>", command = partial(Timeline.SetTime, 4), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMaxOuter)
		cmds.button(label = "OUTER", command = partial(Timeline.SetTime, 5), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineExpandOuter)
		cmds.button(label = "INNER", command = partial(Timeline.SetTime, 6), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineExpandInner)
		cmds.button(label = "FOCUS", command = partial(Timeline.SetTime, 7), backgroundColor = Colors.orange50, annotation = ToolsAnnotations.timelineFocusRange)


	# LOCATORS
	def CreateLocator(self, *args):
		Locators.Create(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorMatch(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorParent(self, *args):
		Locators.CreateOnSelectedWithParentConstrain(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	
	def CreateLocatorBake(self, *args):
		Locators.CreateOnSelectedAndBake(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def CreateLocatorBakeReverse(self, translate = True, rotate = True, *args): # TODO , channelBox = False
		Locators.CreateOnSelectedReverseConstrain(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constrainTranslate = translate, constrainRotate = rotate)
	
	def BakeAsChildrenFromLastSelected(self, *args):
		Locators.BakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def BakeAsChildrenFromLastSelectedReverseSkipLast(self, *args):
		Locators.BakeAsChildrenFromLastSelectedReverse(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), skipLastReverse = True)
	def BakeAsChildrenFromLastSelectedReverse(self, *args):
		Locators.BakeAsChildrenFromLastSelectedReverse(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), skipLastReverse = False)
	
	def CreateLocatorBakeAim(self, axis, reverse, *args):
		scale = self.floatLocatorSize.Get()
		distance = self.floatLocatorAimOffset.Get()
		hideParent = self.checkboxLocatorHideParent.Get()
		subLocators = self.checkboxLocatorSubLocator.Get()

		if (axis == 1): axisVector = (-1, 0, 0)
		elif (axis == 2): axisVector = (1, 0, 0)
		elif (axis == 3): axisVector = (0, -1, 0)
		elif (axis == 4): axisVector = (0, 1, 0)
		elif (axis == 5): axisVector = (0, 0, -1)
		elif (axis == 6): axisVector = (0, 0, 1)

		Locators.CreateOnSelectedAim(scale = scale, hideParent = hideParent, subLocator = subLocators, aimVector = axisVector, distance = distance, reverse = reverse)

		if (distance == 0):
			cmds.warning("Aim distance is 0. Hihgly recomended to use non-zero value.")


	# BAKING
	def BakeSamplesSet(self, value = 1, *args):
		self.fieldBakingSamples.Set(value)
	def BakeSamplesAdd(self, direction = 1, *args):
		value = self.fieldBakingSamples.Get()

		addition = 0
		if (direction == 1):
			if (value < 1):
				addition = 0.1
			else:
				addition = 1
		else:
			if (value <= 1):
				addition = -0.1
			else:
				addition = -1

		value = self.fieldBakingSamples.Get() + addition

		if (value <= 0.1):
			value = 0.1
			cmds.warning("Baking sample rate can't be zero or less. To use values below 0.1 type it manually.")
		
		self.fieldBakingSamples.Set(value)
	def BakeSelectedClassic(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, sampleBy = self.fieldBakingSamples.Get(), channelBox = True)
	def BakeSelectedClassicCut(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = False, sampleBy = self.fieldBakingSamples.Get(), channelBox = True)
	def BakeSelectedCustom(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = True, channelBox = True)
	def BakeSelectedCustomCut(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = False, channelBox = True)
	def BakeSelectedByLastObject(self, *args):
		Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get())

