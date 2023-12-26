# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial

from GETOOLS_SOURCE.utils import Animation
from GETOOLS_SOURCE.utils import Baker
from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.utils import Locators
from GETOOLS_SOURCE.utils import Other
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Timeline
from GETOOLS_SOURCE.utils import UI

from GETOOLS_SOURCE.modules import Settings
from GETOOLS_SOURCE.values import Enums

class ToolsAnnotations:
	_onlyForTranslation = "Only for Translation"
	_onlyForRotation = "Only for Rotation"

	# Locators
	_rightClick = "Right click for more options."
	locatorScale = "Multiply scale of selected locators by"
	locatorScale50 = "{0} 0.5\n{1}".format(locatorScale, _rightClick)
	locatorScale90 = "{0} 0.9\n{1}".format(locatorScale, _rightClick)
	locatorScale110 = "{0} 1.1\n{1}".format(locatorScale, _rightClick)
	locatorScale200 = "{0} 2.0\n{1}".format(locatorScale, _rightClick)
	locatorSizeGet = "Get approximated size of all selected locators"
	locatorSizeSet = "Set size to all selected locators.\nRight click for specific scale values"
	locatorSize = "Size of locator"
	#
	hideParent = "Deactivate visibility on parent locator. \nUsually better to use with \"Sub Locator\" checkbox activated"
	subLocator = "Create an extra locator inside the main locator for additional local control"
	locator = "Create new locator on the world origin"
	locatorMatch = "Create and match locators to selected objects"
	locatorParent = "Create and parent constraint locators to selected objects"
	locatorsBake = "Create locators on selected objects and bake animation"
	_reverseConstraint = "After that parent constrain original objects back to locators"
	locatorsBakeReverse = "{bake}\n{reverse}".format(bake = locatorsBake, reverse = _reverseConstraint)
	locatorsBakeReversePos = "{0}.\n{1}".format(_onlyForTranslation, locatorsBakeReverse)
	locatorsBakeReverseRot = "{0}.\n{1}".format(_onlyForRotation, locatorsBakeReverse)
	#
	locatorsRelative = "{bake}\nThe last locator becomes the parent of other locators".format(bake = locatorsBake)
	locatorsRelativeReverse = "{relative}\n{reverse}\nRight click allows you to bake the same operation but with constrained last object.".format(relative = locatorsRelative, reverse = _reverseConstraint)
	locatorsBakeAim = "Bake locators for Aim Space Switching"
	locatorAimDistance = "Locator Aim distance from original object. Need to use non-zero value"

	# Bake
	bakeSamples = "Baking sample rate, keys will be baked with each N key.\nDefault value is 1.\nMinimal value is 0.001."
	_bakeCutOutside = "Keys outside of time range or selected range will be removed"
	bakeClassic = "Regular maya bake \"Edit/Keys/Bake Simulation\"."
	bakeClassicCut = "{0}.\n{1}".format(bakeClassic, _bakeCutOutside)
	# bakeCustom = "Alternative way to bake. Doesn't support Sample Rate.\nThe same if you just set key every frame on time range.\nAlso works with animation layers."
	# bakeCustomCut = "{0}\n{1}".format(bakeCustom, _bakeCutOutside)
	bakeByLast = "Bake selected objects relative to the last selected object as if they were constrained."
	bakeByLastPos = "{0}.\n{1}".format(_onlyForTranslation, bakeByLast)
	bakeByLastRot = "{0}.\n{1}".format(_onlyForRotation, bakeByLast)
	bakeByWorld = "Bake selected objects relative to the world."
	bakeByWorldPos = "{0}.\n{1}".format(_onlyForTranslation, bakeByWorld)
	bakeByWorldRot = "{0}.\n{1}".format(_onlyForRotation, bakeByWorld)

	# Animation
	deleteAnimation = "Delete animation from selected objects.\nHighligh channel box attributes to delete them.\nHighlight key range in timeline to delete only specific range.\nIf timeline is not highlighted then all animation will be removed"
	# deleteKeyRange = "Delete selected time range keys of selected objects. \nAlso works with selected attributes in Channel Box"
	deleteNonkeyableKeys = "Delete animation on all nonkeyable attributes of selected objects"
	deleteStaticCurves = "Delete all static curves on selected"
	filterCurve = "Filter curve by euler filter. Fix some curve issues"
	animationCurveInfinity = "Curve Infinity"

	timelineSetMinOut = "Set minimal outer timeline value"
	timelineSetMinIn = "Set minimal inner timeline value"
	timelineSetMaxIn = "Set maximum inner timeline value"
	timelineSetMaxOut = "Set maximum outer timeline value"
	timelineExpandOut = "Expand timeline range to outer range"
	timelineExpandIn = "Expand timeline range to inner range"
	timelineSetRange = "Set timeline inner range on selected range by mouse"

	animationOffset = "Move animation on selected objects in time.\nThe animation will move relative to the index of the selected object.\nThe best way to desync animation.\nWorks with selection in the channel box."

class ToolsSettings:
	# SLIDERS (field min/max, slider min/max)
	rangeLocatorAimOffset = (0, float("inf"), 0, 200)

class Tools:
	version = "v0.1.6"
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
		self.UILayoutTimeline(layoutMain, windowWidthMargin, lineHeight)
	def UILayoutLocators(self, layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker):
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "LOCATORS / SPACE SWITCHING", collapsable = True, backgroundColor = Settings.frames2Color)
		layoutColumn = cmds.columnLayout(parent = layoutLocators, adjustableColumn = True)
		#
		countOffsets = 6
		cellWidth = windowWidthMargin / countOffsets
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = cellWidth, cellHeight = lineHeight)
		cmds.button(label = "50%", command = partial(self.SelectedLocatorsScaleSize, 0.5), backgroundColor = Colors.blackWhite50, annotation = ToolsAnnotations.locatorScale50)
		cmds.popupMenu()
		cmds.menuItem(label = "10%", command = partial(self.SelectedLocatorsScaleSize, 0.1))
		cmds.menuItem(label = "20%", command = partial(self.SelectedLocatorsScaleSize, 0.2))
		cmds.menuItem(label = "30%", command = partial(self.SelectedLocatorsScaleSize, 0.3))
		cmds.menuItem(label = "40%", command = partial(self.SelectedLocatorsScaleSize, 0.4))
		cmds.button(label = "90%", command = partial(self.SelectedLocatorsScaleSize, 0.9), backgroundColor = Colors.blackWhite50, annotation = ToolsAnnotations.locatorScale90)
		cmds.popupMenu()
		cmds.menuItem(label = "99%", command = partial(self.SelectedLocatorsScaleSize, 0.99))
		cmds.button(label = "110%", command = partial(self.SelectedLocatorsScaleSize, 1.1), backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.locatorScale110)
		cmds.popupMenu()
		cmds.menuItem(label = "101%", command = partial(self.SelectedLocatorsScaleSize, 1.01))
		cmds.button(label = "200%", command = partial(self.SelectedLocatorsScaleSize, 2), backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.locatorScale200)
		cmds.popupMenu()
		cmds.menuItem(label = "500%", command = partial(self.SelectedLocatorsScaleSize, 5))
		cmds.menuItem(label = "1000%", command = partial(self.SelectedLocatorsScaleSize, 10))
		cmds.menuItem(label = "2000%", command = partial(self.SelectedLocatorsScaleSize, 20))
		cmds.button(label = "GET", command = self.GetLocatorSize, backgroundColor = Colors.blackWhite100, annotation = ToolsAnnotations.locatorSizeGet)
		cmds.button(label = "SET", command = self.SelectedLocatorsSetScaleValue, backgroundColor = Colors.blackWhite100, annotation = ToolsAnnotations.locatorSizeSet)
		cmds.popupMenu()
		cmds.menuItem(label = "0.1", command = partial(self.SelectedLocatorsSetScale, 0.1))
		cmds.menuItem(label = "0.5", command = partial(self.SelectedLocatorsSetScale, 0.5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1", command = partial(self.SelectedLocatorsSetScale, 1))
		cmds.menuItem(label = "5", command = partial(self.SelectedLocatorsSetScale, 5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "10", command = partial(self.SelectedLocatorsSetScale, 10))
		cmds.menuItem(label = "50", command = partial(self.SelectedLocatorsSetScale, 50))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "100", command = partial(self.SelectedLocatorsSetScale, 100))
		cmds.menuItem(label = "500", command = partial(self.SelectedLocatorsSetScale, 500))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1000", command = partial(self.SelectedLocatorsSetScale, 1000))
		cmds.menuItem(label = "5000", command = partial(self.SelectedLocatorsSetScale, 5000))
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		self.checkboxLocatorHideParent = UI.Checkbox(label = "Hide Parent", value = False, annotation = ToolsAnnotations.hideParent)
		self.checkboxLocatorSubLocator = UI.Checkbox(label = "Sub Locator", value = False, annotation = ToolsAnnotations.subLocator)
		self.floatLocatorSize = UI.FloatField(value = 10, precision = 3, annotation = ToolsAnnotations.locatorSize)
		# self.floatLocatorSize = UI.FloatFieldButtons(value = 5, precision = 3, annotation = ToolsAnnotations.locatorSize, width = cellWidth * 0.9, height = lineHeight, commandUp = "", commandDown = "") # TODO
		#
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Locator", command = self.Locator, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locator)
		cmds.button(label = "Match", command = self.LocatorsMatch, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorMatch)
		cmds.button(label = "Parent", command = self.LocatorsParent, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorParent)
		cmds.button(label = "Pin", command = partial(self.LocatorsBakeReverse, True, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "without reverse constraint", command = self.LocatorsBake)
		cmds.button(label = "P-POS", command = partial(self.LocatorsBakeReverse, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReversePos)
		cmds.button(label = "P-ROT", command = partial(self.LocatorsBakeReverse, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverseRot)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "Relative", command = self.LocatorsRelativeReverse, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorsRelativeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "skip last object reverse constraint", command = self.LocatorsRelativeReverseSkipLast)
		cmds.menuItem(label = "without reverse constraint", command = self.LocatorsRelative)
		#
		layoutAim = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = windowWidthMargin, cellHeight = lineHeight)
		countOffsets = 6
		labelLocalSpace = "without reverse constraint"
		cmds.gridLayout(parent = layoutAim, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "-X", command = partial(self.LocatorsBakeAim, 1, True), backgroundColor = Colors.red10, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.LocatorsBakeAim, 1, False))
		cmds.button(label = "+X", command = partial(self.LocatorsBakeAim, 2, True), backgroundColor = Colors.red50, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.LocatorsBakeAim, 2, False))
		cmds.button(label = "-Y", command = partial(self.LocatorsBakeAim, 3, True), backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.LocatorsBakeAim, 3, False))
		cmds.button(label = "+Y", command = partial(self.LocatorsBakeAim, 4, True), backgroundColor = Colors.green50, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.LocatorsBakeAim, 4, False))
		cmds.button(label = "-Z", command = partial(self.LocatorsBakeAim, 5, True), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.LocatorsBakeAim, 5, False))
		cmds.button(label = "+Z", command = partial(self.LocatorsBakeAim, 6, True), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.locatorsBakeAim)
		cmds.popupMenu()
		cmds.menuItem(label = labelLocalSpace, command = partial(self.LocatorsBakeAim, 6, False))
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
		layoutBake = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "BAKING", collapsable = True, backgroundColor = Settings.frames2Color)
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
		cmds.popupMenu()
		cmds.menuItem(label = "Custom", command = self.BakeSelectedCustom)
		cmds.button(label = "Bake Classic Cut Out", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassicCut)
		cmds.popupMenu()
		cmds.menuItem(label = "Custom", command = self.BakeSelectedCustomCut)
		#
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "By Last", command = partial(self.BakeSelectedByLastObject, True, True), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLast)
		cmds.button(label = "BL-POS", command = partial(self.BakeSelectedByLastObject, True, False), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLastPos)
		cmds.button(label = "BL-ROT", command = partial(self.BakeSelectedByLastObject, False, True), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLastRot)
		cmds.button(label = "World", command = partial(self.BakeSelectedByWorld, True, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorld)
		cmds.button(label = "W-POS", command = partial(self.BakeSelectedByWorld, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorldPos)
		cmds.button(label = "W-ROT", command = partial(self.BakeSelectedByWorld, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorldRot)
	def UILayoutAnimation(self, layoutMain, windowWidthMargin, lineHeight):
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "ANIMATION", collapsable = True, backgroundColor = Settings.frames2Color)
		layoutColumn = cmds.columnLayout(parent = layoutRigging, adjustableColumn = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "DEL Animation", command = partial(Animation.DeleteKeys, True), backgroundColor = Colors.red100, annotation = ToolsAnnotations.deleteAnimation)
		cmds.button(label = "DEL Nonkeyable", command = Animation.DeleteKeysNonkeyable, backgroundColor = Colors.red50, annotation = ToolsAnnotations.deleteNonkeyableKeys)
		cmds.button(label = "DEL Static", command = Animation.DeleteStaticCurves, backgroundColor = Colors.red10, annotation = ToolsAnnotations.deleteStaticCurves)
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
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "<<<=", command = partial(self.AnimationOffset, -1, 3), backgroundColor = Colors.purple100, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "<<=", command = partial(self.AnimationOffset, -1, 2), backgroundColor = Colors.purple50, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "<=", command = partial(self.AnimationOffset, -1, 1), backgroundColor = Colors.purple10, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "=>", command = partial(self.AnimationOffset, 1, 1), backgroundColor = Colors.purple10, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "=>>", command = partial(self.AnimationOffset, 1, 2), backgroundColor = Colors.purple50, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "=>>>", command = partial(self.AnimationOffset, 1, 3), backgroundColor = Colors.purple100, annotation = ToolsAnnotations.animationOffset)
	def UILayoutTimeline(self, layoutMain, windowWidthMargin, lineHeight):
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "TIMELINE", collapsable = True, backgroundColor = Settings.frames2Color)
		layoutColumn = cmds.columnLayout(parent = layoutRigging, adjustableColumn = True)
		#
		countOffsets = 7
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets, cellHeight = lineHeight)
		cmds.button(label = "<<", command = partial(Timeline.SetTime, 3), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMinOut)
		cmds.button(label = "<-", command = partial(Timeline.SetTime, 1), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMinIn)
		cmds.button(label = "->", command = partial(Timeline.SetTime, 2), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMaxIn)
		cmds.button(label = ">>", command = partial(Timeline.SetTime, 4), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMaxOut)
		cmds.button(label = "<->", command = partial(Timeline.SetTime, 5), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineExpandOut)
		cmds.button(label = ">-<", command = partial(Timeline.SetTime, 6), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineExpandIn)
		cmds.button(label = "|<->|", command = partial(Timeline.SetTime, 7), backgroundColor = Colors.orange50, annotation = ToolsAnnotations.timelineSetRange)


	# LOCATORS
	def GetLocatorSize(self, *args):
		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return None

		values = []
		for item in selectedList:
			check = Other.CheckShapeType(element = item, type = Enums.Types.locator)
			if (check):
				values.append(Locators.GetSize(item))
		
		count = len(values)
		approximate = [0, 0, 0]
		for i in range(count):
			approximate[0] = approximate[0] + values[i][0]
			approximate[1] = approximate[1] + values[i][1]
			approximate[2] = approximate[2] + values[i][2]
			pass

		approximate[0] = approximate[0] / count
		approximate[1] = approximate[1] / count
		approximate[2] = approximate[2] / count

		result = (approximate[0] + approximate[1] + approximate[2]) / 3
		self.floatLocatorSize.Set(value = result)
	def SelectedLocatorsScaleSize(self, value, *args):
		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return None
		for item in selectedList:
			check = Other.CheckShapeType(element = item, type = Enums.Types.locator)
			if (check):
				Locators.ScaleSize(item, value, value, value)
	def SelectedLocatorsSetScale(self, value, *args):
		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return None

		for item in selectedList:
			check = Other.CheckShapeType(element = item, type = Enums.Types.locator)
			if (check):
				Locators.SetSize(item, value, value, value)
	def SelectedLocatorsSetScaleValue(self, *args):
		self.SelectedLocatorsSetScale(value = self.floatLocatorSize.Get())
		
	def Locator(self, *args):
		Locators.Create(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def LocatorsMatch(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def LocatorsParent(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraint = True)
	
	def LocatorsBake(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraint = True, bake = True)
	def LocatorsBakeReverse(self, translate = True, rotate = True, *args): # TODO , channelBox = False
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraint = True, bake = True, constrainReverse = True, constrainTranslate = translate, constrainRotate = rotate)
	
	def LocatorsRelative(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def LocatorsRelativeReverseSkipLast(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraintReverse = True)
	def LocatorsRelativeReverse(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraintReverse = True, skipLastReverse = False)
	
	def LocatorsBakeAim(self, axis, reverse, *args):
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
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True)
	def BakeSelectedClassicCut(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = False, sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True)
	def BakeSelectedCustom(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = True, selectedRange = True, channelBox = True)
	def BakeSelectedCustomCut(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = False, selectedRange = True, channelBox = True)
	def BakeSelectedByLastObject(self, translate = True, rotate = True, *args):
		if (translate and rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True)
		elif (translate and not rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.translateShort)
		elif (not translate and rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.rotateShort)
	def BakeSelectedByWorld(self, translate = True, rotate = True, *args):
		if (translate and rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True)
		elif (translate and not rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.translateShort)
		elif (not translate and rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.rotateShort)


	# ANIMATION
	def AnimationOffset(self, direction = 1, step = 1, *args):
		Animation.OffsetObjects(direction, step)

