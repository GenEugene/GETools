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
from ..utils import Animation
from ..utils import Baker
from ..utils import ChainDistributionRig
from ..utils import Colors
from ..utils import Locators
from ..utils import Selector
from ..utils import Timeline
from ..values import Enums


class ToolsAnnotations:
	_onlyForTranslation = "Only for Translation"
	_onlyForRotation = "Only for Rotation"

	### Locators
	_rightClick = "Right click for more options."
	locatorScale = "Multiply scale of selected locators by"
	locatorScale50 = "{0} 0.5\n{1}".format(locatorScale, _rightClick)
	locatorScale90 = "{0} 0.9\n{1}".format(locatorScale, _rightClick)
	locatorScale110 = "{0} 1.1\n{1}".format(locatorScale, _rightClick)
	locatorScale200 = "{0} 2.0\n{1}".format(locatorScale, _rightClick)
	locatorSizeGet = "Get approximated size of all selected locators"
	locatorSizeSet = "Set size to all selected locators.\nRight click for specific scale values"
	locatorSize = "Locator size on creation"
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
	#
	chainDistribution = "Create a chain with distributed rotation. Use the last locator to animate.\nWorks better with 3 selected objects.\nIf you select 4+ objects, the original animation will not be fully preserved.\n\nRight-click to use the alternate mode to preserve 100% of the original animation with any number of selected objects.\nIt is not as convenient to use as the default mode."
	
	# locatorAimSpace = "Locator Aim distance from original object. Need to use non-zero value"
	locatorAimSpace = "Aim Space offset from original object.\nNeed to use non-zero value to get best result"
	locatorAimSpaceBakeAll = "Create Aim Space locators for selected objects.\nOriginal object will be constrained back to locator."
	locatorAimSpaceBakeRotate = "{0}\n{1}".format(_onlyForRotation, locatorAimSpaceBakeAll)

	### Bake
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

	### Animation
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
	timelineFocusOut = "Focus outer timeline range"
	timelineFocusIn = "Focus inner timeline range"
	timelineSetRange = "Set timeline inner range on selected range by mouse"

	desync = "Desync animation curves on selected objects in the corresponding order.\nWorks with attributes in the channel box."
	desyncSetValue = "Set predefined step value"
	desyncIncrementValue = "Increment step value by 1"
	desyncValue = "Step value for animation desync"

class ToolsSettings:
	locatorSize = 10

	### Aim Space
	aimSpaceOffsetValue = 100
	aimSpaceRadioButtonDefault = 0

class Tools:
	_version = "v1.5"
	_name = "TOOLS"
	_title = _name + " " + _version

	def __init__(self, options):
		self.optionsPlugin = options
		### Check Maya version to avoid cycle import, Maya 2020 and older can't use cycle import
		if cmds.about(version = True) in ["2022", "2023", "2024", "2025"]:
			from ..modules import Options
			if isinstance(options, Options.PluginVariables):
				self.optionsPlugin = options

		self.checkboxLocatorHideParent = None
		self.checkboxLocatorSubLocator = None
		self.floatLocatorSize = None
		### Locator Aim Space
		self.aimSpaceFloatField = None
		self.aimSpaceRadioButtons = [None, None, None]
		self.aimSpaceCheckbox = None
		### Desync
		self.desyncFloatField = None

		self.bakingSamplesValue = None

	def UICreate(self, layoutMain):
		# layoutColumn = cmds.columnLayout(parent = layoutMain, adjustableColumn = True) # TODO remove ghost empty spacing when collapse
		self.UILayoutLocators(layoutMain)
		self.UILayoutBaking(layoutMain)
		self.UILayoutAnimation(layoutMain)
		self.UILayoutTimeline(layoutMain)
	def UILayoutLocators(self, layoutMain):
		cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "LOCATORS // SPACE SWITCHING", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		layoutColumn = cmds.columnLayout(adjustableColumn = True, rowSpacing = 2)
		
		### LOCATORS SIZE
		countCells1 = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countCells1, cellWidth = Settings.windowWidth / countCells1, cellHeight = Settings.lineHeight)
		cmds.button(label = "50%", command = partial(Locators.SelectedLocatorsSizeScale, 0.5), backgroundColor = Colors.blackWhite50, annotation = ToolsAnnotations.locatorScale50)
		cmds.popupMenu()
		cmds.menuItem(label = "10%", command = partial(Locators.SelectedLocatorsSizeScale, 0.1))
		cmds.menuItem(label = "20%", command = partial(Locators.SelectedLocatorsSizeScale, 0.2))
		cmds.menuItem(label = "30%", command = partial(Locators.SelectedLocatorsSizeScale, 0.3))
		cmds.menuItem(label = "40%", command = partial(Locators.SelectedLocatorsSizeScale, 0.4))
		cmds.button(label = "90%", command = partial(Locators.SelectedLocatorsSizeScale, 0.9), backgroundColor = Colors.blackWhite50, annotation = ToolsAnnotations.locatorScale90)
		cmds.popupMenu()
		cmds.menuItem(label = "99%", command = partial(Locators.SelectedLocatorsSizeScale, 0.99))
		cmds.button(label = "110%", command = partial(Locators.SelectedLocatorsSizeScale, 1.1), backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.locatorScale110)
		cmds.popupMenu()
		cmds.menuItem(label = "101%", command = partial(Locators.SelectedLocatorsSizeScale, 1.01))
		cmds.button(label = "200%", command = partial(Locators.SelectedLocatorsSizeScale, 2), backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.locatorScale200)
		cmds.popupMenu()
		cmds.menuItem(label = "500%", command = partial(Locators.SelectedLocatorsSizeScale, 5))
		cmds.menuItem(label = "1000%", command = partial(Locators.SelectedLocatorsSizeScale, 10))
		cmds.menuItem(label = "2000%", command = partial(Locators.SelectedLocatorsSizeScale, 20))
		cmds.button(label = "GET", command = self.GetLocatorSize, backgroundColor = Colors.blackWhite100, annotation = ToolsAnnotations.locatorSizeGet)
		cmds.button(label = "SET", command = self.SelectedLocatorsSizeSetValue, backgroundColor = Colors.blackWhite100, annotation = ToolsAnnotations.locatorSizeSet)
		cmds.popupMenu()
		cmds.menuItem(label = "0.1", command = partial(Locators.SelectedLocatorsSizeSet, 0.1))
		cmds.menuItem(label = "0.5", command = partial(Locators.SelectedLocatorsSizeSet, 0.5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1", command = partial(Locators.SelectedLocatorsSizeSet, 1))
		cmds.menuItem(label = "5", command = partial(Locators.SelectedLocatorsSizeSet, 5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "10", command = partial(Locators.SelectedLocatorsSizeSet, 10))
		cmds.menuItem(label = "50", command = partial(Locators.SelectedLocatorsSizeSet, 50))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "100", command = partial(Locators.SelectedLocatorsSizeSet, 100))
		cmds.menuItem(label = "500", command = partial(Locators.SelectedLocatorsSizeSet, 500))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1000", command = partial(Locators.SelectedLocatorsSizeSet, 1000))
		cmds.menuItem(label = "5000", command = partial(Locators.SelectedLocatorsSizeSet, 5000))
		# cmds.setParent("..")

		### OPTIONS
		cmds.rowLayout(parent = layoutColumn, adjustableColumn = 4, numberOfColumns = 4, columnWidth4 = (80, 80, 35, 40), columnAlign = [(1, "center"), (2, "center"), (3, "right"), (4, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0), (4, "both", 0)])
		self.checkboxLocatorHideParent = cmds.checkBox(label = "Hide Parent", value = False, annotation = ToolsAnnotations.hideParent)
		self.checkboxLocatorSubLocator = cmds.checkBox(label = "Sub Locator", value = False, annotation = ToolsAnnotations.subLocator)
		cmds.text(label = "Size:", annotation = ToolsAnnotations.locatorSize)
		self.floatLocatorSize = cmds.floatField(value = ToolsSettings.locatorSize, precision = 3, annotation = ToolsAnnotations.locatorSize)
		# cmds.setParent("..")

		### LOCATORS ROW 1
		countCells2 = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countCells2, cellWidth = Settings.windowWidth / countCells2, cellHeight = Settings.lineHeight)
		cmds.button(label = "Locator", command = self.Locator, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locator)
		cmds.button(label = "Match", command = self.LocatorsMatch, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorMatch)
		cmds.button(label = "Parent", command = self.LocatorsParent, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorParent)
		cmds.button(label = "Pin", command = partial(self.LocatorsBakeReverse, True, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "Without Reverse Constraint", command = self.LocatorsBake)
		cmds.button(label = "P-POS", command = partial(self.LocatorsBakeReverse, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReversePos)
		cmds.button(label = "P-ROT", command = partial(self.LocatorsBakeReverse, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverseRot)
		# cmds.setParent("..")

		### LOCATORS ROW 2
		cmds.rowLayout(parent = layoutColumn, adjustableColumn = 1, numberOfColumns = 2, columnWidth2 = (50, 150), columnAlign = [(1, "center"), (2, "center")], columnAttach = [(1, "both", 0), (2, "both", 0)])
		cmds.button(label = "Relative", command = self.LocatorsRelativeReverse, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorsRelativeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "Skip Last Object Reverse Constraint", command = self.LocatorsRelativeReverseSkipLast)
		cmds.menuItem(label = "Without Reverse Constraint", command = self.LocatorsRelative)
		cmds.button(label = "Chain Distribution", command = partial(self.CreateChainDistributionRig, 1), backgroundColor = Colors.purple10, annotation = ToolsAnnotations.chainDistribution)
		cmds.popupMenu()
		cmds.menuItem(label = "Alternative Mode", command = partial(self.CreateChainDistributionRig, 2))
		# cmds.setParent("..")

		### AIM SPACE SWITCHING
		layoutAimSpace = cmds.frameLayout(parent = layoutColumn, label = "Aim Space Switching", labelIndent = 75, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		#
		cmds.rowLayout(parent = layoutAimSpace, adjustableColumn = 2, numberOfColumns = 6, columnWidth6 = (40, 40, 28, 28, 28, 60), columnAlign = [1, "center"], columnAttach = [(1, "both", 0)])
		cmds.text(label = "Offset")
		self.aimSpaceFloatField = cmds.floatField(value = ToolsSettings.aimSpaceOffsetValue, precision = 3, minValue = 0, annotation = ToolsAnnotations.locatorAimSpace)
		cmds.radioCollection()
		self.aimSpaceRadioButtons[0] = cmds.radioButton(label = "X")
		self.aimSpaceRadioButtons[1] = cmds.radioButton(label = "Y")
		self.aimSpaceRadioButtons[2] = cmds.radioButton(label = "Z")
		self.aimSpaceCheckbox = cmds.checkBox(label = "Reverse", value = False)
		cmds.radioButton(self.aimSpaceRadioButtons[ToolsSettings.aimSpaceRadioButtonDefault], edit = True, select = True)
		# cmds.setParent("..")
		#
		cmds.rowLayout(parent = layoutAimSpace, adjustableColumn = 1, numberOfColumns = 3, columnWidth3 = (30, 105, 105), columnAlign = [(1, "center"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)])
		cmds.text(label = "Create")
		cmds.button(label = "Translate + Rotate", command = partial(self.LocatorsBakeAim, False), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorAimSpaceBakeAll)
		cmds.button(label = "Only Rotate", command = partial(self.LocatorsBakeAim, True), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorAimSpaceBakeRotate)
		# cmds.setParent("..")
	def UILayoutBaking(self, layoutMain):
		cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "BAKING", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		layoutColumn = cmds.columnLayout(adjustableColumn = True, rowSpacing = 2)

		rowLayout = cmds.rowLayout(parent = layoutColumn, adjustableColumn = 2, numberOfColumns = 3, columnWidth3 = (80, 40, 120), height = Settings.lineHeight, columnAlign = [(1, "right"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)])
		cmds.text(parent = rowLayout, label = "Set Bake Step", annotation = ToolsAnnotations.locatorSize)
		self.bakingSamplesValue = cmds.floatField(parent = rowLayout, value = 1, precision = 3, minValue = 0.001, annotation = ToolsAnnotations.bakeSamples)
		cmds.gridLayout(parent = rowLayout, numberOfColumns = 6, cellWidth = 20, cellHeight = Settings.lineHeight)
		cmds.button(label = "-", command = partial(self.BakeSamplesAdd, -1), backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "+", command = partial(self.BakeSamplesAdd, 1), backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "1", command = partial(self.BakeSamplesSet, 1), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "2", command = partial(self.BakeSamplesSet, 2), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "3", command = partial(self.BakeSamplesSet, 3), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "4", command = partial(self.BakeSamplesSet, 4), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		
		countCells1 = 2
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countCells1, cellWidth = Settings.windowWidth / countCells1, cellHeight = Settings.lineHeight)
		cmds.button(label = "Bake Classic", command = self.BakeSelectedClassic, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassic)
		cmds.popupMenu()
		cmds.menuItem(label = "Custom", command = self.BakeSelectedCustom)
		cmds.button(label = "Bake Classic Cut Out", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassicCut)
		cmds.popupMenu()
		cmds.menuItem(label = "Custom", command = self.BakeSelectedCustomCut)

		countCells2 = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countCells2, cellWidth = Settings.windowWidth / countCells2, cellHeight = Settings.lineHeight)
		cmds.button(label = "By Last", command = partial(self.BakeSelectedByLastObject, True, True), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLast)
		cmds.button(label = "BL-POS", command = partial(self.BakeSelectedByLastObject, True, False), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLastPos)
		cmds.button(label = "BL-ROT", command = partial(self.BakeSelectedByLastObject, False, True), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLastRot)
		cmds.button(label = "World", command = partial(self.BakeSelectedByWorld, True, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorld)
		cmds.button(label = "W-POS", command = partial(self.BakeSelectedByWorld, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorldPos)
		cmds.button(label = "W-ROT", command = partial(self.BakeSelectedByWorld, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorldRot)
	def UILayoutAnimation(self, layoutMain):
		cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "ANIMATION", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		layoutColumn = cmds.columnLayout(adjustableColumn = True, rowSpacing = 2)
		
		cmds.rowLayout(parent = layoutColumn, adjustableColumn = 1, numberOfColumns = 4, columnWidth4 = (60, 35, 75, 50), columnAlign = [(1, "center"), (2, "center"), (3, "center"), (4, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0), (4, "both", 0)])
		cmds.text(label = "Delete Keys")
		cmds.button(label = "All", command = partial(Animation.DeleteKeys, True), backgroundColor = Colors.red100, annotation = ToolsAnnotations.deleteAnimation)
		cmds.button(label = "Nonkeyable", command = Animation.DeleteKeysNonkeyable, backgroundColor = Colors.red50, annotation = ToolsAnnotations.deleteNonkeyableKeys)
		cmds.button(label = "Static", command = Animation.DeleteStaticCurves, backgroundColor = Colors.red10, annotation = ToolsAnnotations.deleteStaticCurves)
		#
		countCellsEuler = 1 # TODO remove grid logic
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countCellsEuler, cellWidth = Settings.windowWidth / countCellsEuler, cellHeight = Settings.lineHeight)
		cmds.button(label = "Euler Filter", command = Animation.EulerFilterOnSelected, backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.filterCurve)
		#
		countCellsInfinity = 5
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countCellsInfinity, cellWidth = Settings.windowWidth / countCellsInfinity, cellHeight = Settings.lineHeight)
		cmds.button(label = "Constant", command = partial(Animation.SetInfinity, 1, None), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Linear", command = partial(Animation.SetInfinity, 2, None), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Cycle", command = partial(Animation.SetInfinity, 3, None), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Offset", command = partial(Animation.SetInfinity, 4, None), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Oscillate", command = partial(Animation.SetInfinity, 5, None), backgroundColor = Colors.blue100, annotation = ToolsAnnotations.animationCurveInfinity)
		#

		### Desync
		cmds.frameLayout(parent = layoutColumn, label = "Desync", labelIndent = 110, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		rowLayout = cmds.rowLayout(adjustableColumn = 2, numberOfColumns = 4, columnWidth4 = (120, 30, 30, 70), columnAlign = [(1, "center"), (2, "center"), (3, "right"), (4, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0), (4, "both", 0)])
		# 1
		cmds.gridLayout(parent = rowLayout, numberOfColumns = 6, cellWidth = 20, cellHeight = Settings.lineHeight)
		cmds.button(label = "0.1", command = partial(self.AnimationOffsetSetValue, 0.1), backgroundColor = Colors.blackWhite90, annotation = ToolsAnnotations.desyncSetValue)
		cmds.button(label = "0.5", command = partial(self.AnimationOffsetSetValue, 0.5), backgroundColor = Colors.blackWhite90, annotation = ToolsAnnotations.desyncSetValue)
		cmds.button(label = "1", command = partial(self.AnimationOffsetSetValue, 1), backgroundColor = Colors.blackWhite90, annotation = ToolsAnnotations.desyncSetValue)
		cmds.button(label = "4", command = partial(self.AnimationOffsetSetValue, 4), backgroundColor = Colors.blackWhite90, annotation = ToolsAnnotations.desyncSetValue)
		cmds.button(label = "-", command = self.AnimationOffsetAddValueNegative, backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.desyncIncrementValue)
		cmds.button(label = "+", command = self.AnimationOffsetAddValuePositive, backgroundColor = Colors.blackWhite70, annotation = ToolsAnnotations.desyncIncrementValue)
		# 2
		self.desyncFloatField = cmds.floatField(parent = rowLayout, value = 1, precision = 3, minValue = 0, annotation = ToolsAnnotations.desyncValue)
		# 3
		cmds.text(parent = rowLayout, label = "Move", annotation = ToolsAnnotations.desync)
		# 4
		cmds.gridLayout(parent = rowLayout, numberOfColumns = 2, cellWidth = 35, cellHeight = Settings.lineHeight)
		cmds.button(label = "Left", command = self.AnimationOffsetMoveLeft, backgroundColor = Colors.red50, annotation = ToolsAnnotations.desync)
		cmds.button(label = "Right", command = self.AnimationOffsetMoveRight, backgroundColor = Colors.green50, annotation = ToolsAnnotations.desync)
	def UILayoutTimeline(self, layoutMain):
		cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "TIMELINE", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		layoutColumn = cmds.columnLayout(adjustableColumn = True, rowSpacing = 2)
		
		countOffsets = 7
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidth / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "<<", command = partial(Timeline.SetTime, 3), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMinOut)
		cmds.button(label = "<-", command = partial(Timeline.SetTime, 1), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMinIn)
		cmds.button(label = "->", command = partial(Timeline.SetTime, 2), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMaxIn)
		cmds.button(label = ">>", command = partial(Timeline.SetTime, 4), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMaxOut)
		cmds.button(label = "<->", command = partial(Timeline.SetTime, 5), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineFocusOut)
		cmds.button(label = ">-<", command = partial(Timeline.SetTime, 6), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineFocusIn)
		cmds.button(label = "|<->|", command = partial(Timeline.SetTime, 7), backgroundColor = Colors.orange50, annotation = ToolsAnnotations.timelineSetRange)


	### LOCATORS
	def GetFloatLocatorSize(self):
		return cmds.floatField(self.floatLocatorSize, query = True, value = True)

	def GetLocatorSize(self, *args):
		selectedList = Selector.MultipleObjects(1)
		if (selectedList == None):
			return None

		values = []
		for item in selectedList:
			shape = cmds.listRelatives(item, shapes = True, type = Enums.Types.locator)[0]
			if (shape != None):
				values.append(Locators.GetSize(item))
		
		count = len(values)
		if (count == 0):
			cmds.warning("Locators are not detected in selected objects")
			return

		approximate = [0, 0, 0]
		for i in range(count):
			approximate[0] = approximate[0] + values[i][0]
			approximate[1] = approximate[1] + values[i][1]
			approximate[2] = approximate[2] + values[i][2]

		approximate[0] = approximate[0] / count
		approximate[1] = approximate[1] / count
		approximate[2] = approximate[2] / count

		result = (approximate[0] + approximate[1] + approximate[2]) / 3
		cmds.floatField(self.floatLocatorSize, edit = True, value = result)
	def SelectedLocatorsSizeSetValue(self, *args):
		Locators.SelectedLocatorsSizeSet(value = self.GetFloatLocatorSize())

	def GetCheckboxLocatorHideParent(self):
		return cmds.checkBox(self.checkboxLocatorHideParent, query = True, value = True)
	def GetCheckboxLocatorSubLocator(self):
		return cmds.checkBox(self.checkboxLocatorSubLocator, query = True, value = True)

	def Locator(self, *args):
		Locators.Create(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator())
	def LocatorsMatch(self, *args):
		Locators.CreateOnSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator())
	def LocatorsParent(self, *args):
		Locators.CreateOnSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator(), constraint = True)
	
	def LocatorsBake(self, *args):
		Locators.CreateOnSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator(), constraint = True, bake = True)
	def LocatorsBakeReverse(self, translate=True, rotate=True, *args): # TODO , channelBox = False
		Locators.CreateOnSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator(), constraint = True, bake = True, constrainReverse = True, constrainTranslate = translate, constrainRotate = rotate)
	
	def LocatorsRelative(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator(), euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def LocatorsRelativeReverseSkipLast(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator(), constraintReverse = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def LocatorsRelativeReverse(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.GetFloatLocatorSize(), hideParent = self.GetCheckboxLocatorHideParent(), subLocator = self.GetCheckboxLocatorSubLocator(), constraintReverse = True, skipLastReverse = False, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	
	def LocatorsBakeAim(self, rotateOnly=False, *args):
		scale = self.GetFloatLocatorSize()
		distance = cmds.floatField(self.aimSpaceFloatField, query = True, value = True)
		hideParent = self.GetCheckboxLocatorHideParent()
		subLocators = self.GetCheckboxLocatorSubLocator()
		reverse = cmds.checkBox(self.aimSpaceCheckbox, query = True, value = True)

		### Compile value and return
		valueAimTarget = 1 * (-1 if reverse else 1)
		if (cmds.radioButton(self.aimSpaceRadioButtons[0], query = True, select = True)):
			axisVector = [valueAimTarget, 0, 0]
		if (cmds.radioButton(self.aimSpaceRadioButtons[1], query = True, select = True)):
			axisVector = [0, valueAimTarget, 0]
		if (cmds.radioButton(self.aimSpaceRadioButtons[2], query = True, select = True)):
			axisVector = [0, 0, valueAimTarget]

		Locators.CreateOnSelectedAim(scale = scale, hideParent = hideParent, subLocator = subLocators, rotateOnly = rotateOnly, vectorAim = axisVector, distance = distance, reverse = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())

		if (distance == 0):
			cmds.warning("Aim distance is 0. Highly recommended to use non-zero value.")

	### CHAIN DISTRIBUTION RIG
	def CreateChainDistributionRig(self, mode=1, *args):
		if mode == 1:
			ChainDistributionRig.CreateRigVariant1(locatorSize = self.GetFloatLocatorSize())
		if mode == 2:
			ChainDistributionRig.CreateRigVariant2(locatorSize = self.GetFloatLocatorSize())


	### BAKING
	def BakeSampleGet(self):
		return cmds.floatField(self.bakingSamplesValue, query = True, value = True)
	def BakeSamplesSet(self, value=1, *args):
		cmds.floatField(self.bakingSamplesValue, edit = True, value = value)
	def BakeSamplesAdd(self, direction=1, *args): # TODO use FloatValueAdd() instead
		value = self.BakeSampleGet()

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

		value = value + addition

		if (value <= 0.1):
			value = 0.1
			cmds.warning("Baking sample rate can't be zero or less. To use values below 0.1 type it manually.")
		
		self.BakeSamplesSet(value)
	def BakeSelectedClassic(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def BakeSelectedClassicCut(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = False, sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def BakeSelectedCustom(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = True, selectedRange = True, channelBox = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def BakeSelectedCustomCut(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = False, selectedRange = True, channelBox = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def BakeSelectedByLastObject(self, translate=True, rotate=True, *args):
		if (translate and rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
		elif (translate and not rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.translateLong, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
		elif (not translate and rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.rotateLong, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
	def BakeSelectedByWorld(self, translate=True, rotate=True, *args):
		if (translate and rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = True, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
		elif (translate and not rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.translateLong, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())
		elif (not translate and rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.BakeSampleGet(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.rotateLong, euler = self.optionsPlugin.menuCheckboxEulerFilter.Get())


	### ANIMATION
	def FloatValueAdd(self, value, direction=1, *args):
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

		result = value + addition

		if (result <= 0.1):
			result = 0.1
			cmds.warning("Value can't be zero or less. To use values below 0.1 type it manually.")
		
		return result
	def AnimationOffsetSetValue(self, value, *args):
		cmds.floatField(self.desyncFloatField, edit = True, value = value)
	def AnimationOffsetAddValue(self, direction):
		value = cmds.floatField(self.desyncFloatField, query = True, value = True)
		valueNew = self.FloatValueAdd(value, direction)
		self.AnimationOffsetSetValue(valueNew)
	def AnimationOffsetAddValueNegative(self, *args):
		self.AnimationOffsetAddValue(direction = -1)
	def AnimationOffsetAddValuePositive(self, *args):
		self.AnimationOffsetAddValue(direction = 1)
	def AnimationOffsetMove(self, direction=1):
		value = cmds.floatField(self.desyncFloatField, query = True, value = True)
		self.AnimationOffset(direction, value)
	def AnimationOffsetMoveLeft(self, *args):
		self.AnimationOffsetMove(direction = -1)
	def AnimationOffsetMoveRight(self, *args):
		self.AnimationOffsetMove(direction = 1)
	def AnimationOffset(self, direction=1, step=1, *args):
		Animation.OffsetSelected(direction, step)

