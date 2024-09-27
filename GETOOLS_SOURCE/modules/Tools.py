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
from ..utils import Colors
from ..utils import Locators
from ..utils import Selector
from ..utils import Timeline
from ..utils import UI
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

	animationOffset = "Move animation on selected objects in time.\nThe animation will move relative to the index of the selected object.\nThe best way to desync animation.\nWorks with selection in the channel box."

class ToolsSettings:
	### AIM SPACE
	aimSpaceName = "Offset"
	aimSpaceOffsetValue = 100
	aimSpaceRadioButtonDefault = 0

class Tools:
	_version = "v1.1"
	_name = "TOOLS"
	_title = _name + " " + _version

	# HACK use only for code editor # TODO try to find better way to get access to other classes with cross import
	# from ..modules import GeneralWindow
	# def __init__(self, generalInstance: GeneralWindow.GeneralWindow):
	def __init__(self, generalInstance):
		self.generalInstance = generalInstance

		self.checkboxLocatorHideParent = None
		self.checkboxLocatorSubLocator = None
		self.floatLocatorSize = None
		
		### Locator Aim Space
		self.aimSpaceFloatField = None
		self.aimSpaceRadioButtons = [None, None, None]
		self.aimSpaceCheckbox = None

		self.fieldBakingSamples = None

	def UICreate(self, layoutMain):
		self.UILayoutLocators(layoutMain)
		self.UILayoutBaking(layoutMain)
		self.UILayoutAnimation(layoutMain)
		self.UILayoutTimeline(layoutMain)
	def UILayoutLocators(self, layoutMain):
		layoutLocators = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "LOCATORS // SPACE SWITCHING", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = layoutLocators, adjustableColumn = True)
		#
		countOffsets = 6
		cellWidth = Settings.windowWidthMargin / countOffsets
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = cellWidth, cellHeight = Settings.lineHeight)
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
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		self.checkboxLocatorHideParent = UI.Checkbox(label = "Hide Parent", value = False, annotation = ToolsAnnotations.hideParent)
		self.checkboxLocatorSubLocator = UI.Checkbox(label = "Sub Locator", value = False, annotation = ToolsAnnotations.subLocator)
		self.floatLocatorSize = UI.FloatField(value = 10, precision = 3, annotation = ToolsAnnotations.locatorSize)
		#
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Locator", command = self.Locator, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locator)
		cmds.button(label = "Match", command = self.LocatorsMatch, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorMatch)
		cmds.button(label = "Parent", command = self.LocatorsParent, backgroundColor = Colors.green10, annotation = ToolsAnnotations.locatorParent)
		cmds.button(label = "Pin", command = partial(self.LocatorsBakeReverse, True, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "Without Reverse Constraint", command = self.LocatorsBake)
		cmds.button(label = "P-POS", command = partial(self.LocatorsBakeReverse, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReversePos)
		cmds.button(label = "P-ROT", command = partial(self.LocatorsBakeReverse, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.locatorsBakeReverseRot)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Relative", command = self.LocatorsRelativeReverse, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorsRelativeReverse)
		cmds.popupMenu()
		cmds.menuItem(label = "Skip Last Object Reverse Constraint", command = self.LocatorsRelativeReverseSkipLast)
		cmds.menuItem(label = "Without Reverse Constraint", command = self.LocatorsRelative)
		#
		
		### Aim Space
		layoutAimSpace = cmds.frameLayout(parent = layoutColumn, label = "Aim Space", labelIndent = 100, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)

		cmds.rowLayout(parent = layoutAimSpace, numberOfColumns = 6, columnWidth6 = (40, 55, 35, 35, 35, 60), columnAlign = [1, "center"], columnAttach = [(1, "both", 0)])
		cmds.text(label = ToolsSettings.aimSpaceName)
		self.aimSpaceFloatField = cmds.floatField(value = ToolsSettings.aimSpaceOffsetValue, precision = 3, minValue = 0, annotation = ToolsAnnotations.locatorAimSpace)
		cmds.radioCollection()
		self.aimSpaceRadioButtons[0] = cmds.radioButton(label = "X")
		self.aimSpaceRadioButtons[1] = cmds.radioButton(label = "Y")
		self.aimSpaceRadioButtons[2] = cmds.radioButton(label = "Z")
		self.aimSpaceCheckbox = cmds.checkBox(label = "Reverse", value = False)
		cmds.radioButton(self.aimSpaceRadioButtons[ToolsSettings.aimSpaceRadioButtonDefault], edit = True, select = True)
		
		cmds.rowLayout(parent = layoutAimSpace, numberOfColumns = 3, columnWidth3 = (50, 110, 110), columnAlign = [(1, "center"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)])
		cmds.text(label = "Bake")
		cmds.button(label = "Translate + Rotate", command = partial(self.LocatorsBakeAim, False), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorAimSpaceBakeAll)
		cmds.button(label = "Only Rotate", command = partial(self.LocatorsBakeAim, True), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.locatorAimSpaceBakeRotate)

	def UILayoutBaking(self, layoutMain):
		layoutBake = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "BAKING", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = layoutBake, adjustableColumn = True)
		#
		countOffsets = 6
		cellWidth = Settings.windowWidthMargin / countOffsets
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = cellWidth, cellHeight = Settings.lineHeight)
		cmds.button(label = "1", command = partial(self.BakeSamplesSet, 1), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "2", command = partial(self.BakeSamplesSet, 2), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "3", command = partial(self.BakeSamplesSet, 3), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		cmds.button(label = "4", command = partial(self.BakeSamplesSet, 4), backgroundColor = Colors.lightBlue10, annotation = ToolsAnnotations.bakeSamples)
		UI.ButtonLeftRight(width = cellWidth, height = Settings.lineHeight, commandLeft = partial(self.BakeSamplesAdd, -1), commandRight = partial(self.BakeSamplesAdd, 1), backgroundColor = Colors.lightBlue50, annotation = ToolsAnnotations.bakeSamples)
		self.fieldBakingSamples = UI.FloatField(value = 1, precision = 3, minValue = 0.001, annotation = ToolsAnnotations.bakeSamples)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Bake Classic", command = self.BakeSelectedClassic, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassic)
		cmds.popupMenu()
		cmds.menuItem(label = "Custom", command = self.BakeSelectedCustom)
		cmds.button(label = "Bake Classic Cut Out", command = self.BakeSelectedClassicCut, backgroundColor = Colors.orange10, annotation = ToolsAnnotations.bakeClassicCut)
		cmds.popupMenu()
		cmds.menuItem(label = "Custom", command = self.BakeSelectedCustomCut)
		#
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "By Last", command = partial(self.BakeSelectedByLastObject, True, True), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLast)
		cmds.button(label = "BL-POS", command = partial(self.BakeSelectedByLastObject, True, False), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLastPos)
		cmds.button(label = "BL-ROT", command = partial(self.BakeSelectedByLastObject, False, True), backgroundColor = Colors.orange100, annotation = ToolsAnnotations.bakeByLastRot)
		cmds.button(label = "World", command = partial(self.BakeSelectedByWorld, True, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorld)
		cmds.button(label = "W-POS", command = partial(self.BakeSelectedByWorld, True, False), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorldPos)
		cmds.button(label = "W-ROT", command = partial(self.BakeSelectedByWorld, False, True), backgroundColor = Colors.yellow50, annotation = ToolsAnnotations.bakeByWorldRot)
	def UILayoutAnimation(self, layoutMain):
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "ANIMATION", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = layoutRigging, adjustableColumn = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "DEL Animation", command = partial(Animation.DeleteKeys, True), backgroundColor = Colors.red100, annotation = ToolsAnnotations.deleteAnimation)
		cmds.button(label = "DEL Nonkeyable", command = Animation.DeleteKeysNonkeyable, backgroundColor = Colors.red50, annotation = ToolsAnnotations.deleteNonkeyableKeys)
		cmds.button(label = "DEL Static", command = Animation.DeleteStaticCurves, backgroundColor = Colors.red10, annotation = ToolsAnnotations.deleteStaticCurves)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Euler Filter", command = Animation.EulerFilterOnSelected, backgroundColor = Colors.yellow10, annotation = ToolsAnnotations.filterCurve)
		#
		countOffsets = 5
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Constant", command = partial(Animation.SetInfinity, 1, None), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Linear", command = partial(Animation.SetInfinity, 2, None), backgroundColor = Colors.blue10, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Cycle", command = partial(Animation.SetInfinity, 3, None), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Offset", command = partial(Animation.SetInfinity, 4, None), backgroundColor = Colors.blue50, annotation = ToolsAnnotations.animationCurveInfinity)
		cmds.button(label = "Oscillate", command = partial(Animation.SetInfinity, 5, None), backgroundColor = Colors.blue100, annotation = ToolsAnnotations.animationCurveInfinity)
		#
		countOffsets = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "<<<=", command = partial(self.AnimationOffset, -1, 3), backgroundColor = Colors.purple100, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "<<=", command = partial(self.AnimationOffset, -1, 2), backgroundColor = Colors.purple50, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "<=", command = partial(self.AnimationOffset, -1, 1), backgroundColor = Colors.purple10, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "=>", command = partial(self.AnimationOffset, 1, 1), backgroundColor = Colors.purple10, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "=>>", command = partial(self.AnimationOffset, 1, 2), backgroundColor = Colors.purple50, annotation = ToolsAnnotations.animationOffset)
		cmds.button(label = "=>>>", command = partial(self.AnimationOffset, 1, 3), backgroundColor = Colors.purple100, annotation = ToolsAnnotations.animationOffset)
	def UILayoutTimeline(self, layoutMain):
		layoutRigging = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "TIMELINE", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = layoutRigging, adjustableColumn = True)
		#
		countOffsets = 7
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "<<", command = partial(Timeline.SetTime, 3), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMinOut)
		cmds.button(label = "<-", command = partial(Timeline.SetTime, 1), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMinIn)
		cmds.button(label = "->", command = partial(Timeline.SetTime, 2), backgroundColor = Colors.green50, annotation = ToolsAnnotations.timelineSetMaxIn)
		cmds.button(label = ">>", command = partial(Timeline.SetTime, 4), backgroundColor = Colors.green10, annotation = ToolsAnnotations.timelineSetMaxOut)
		cmds.button(label = "<->", command = partial(Timeline.SetTime, 5), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineFocusOut)
		cmds.button(label = ">-<", command = partial(Timeline.SetTime, 6), backgroundColor = Colors.orange10, annotation = ToolsAnnotations.timelineFocusIn)
		cmds.button(label = "|<->|", command = partial(Timeline.SetTime, 7), backgroundColor = Colors.orange50, annotation = ToolsAnnotations.timelineSetRange)


	### LOCATORS
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
		self.floatLocatorSize.Set(value = result)
	def SelectedLocatorsSizeSetValue(self, *args):
		Locators.SelectedLocatorsSizeSet(value = self.floatLocatorSize.Get())
		
	def Locator(self, *args):
		Locators.Create(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def LocatorsMatch(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get())
	def LocatorsParent(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraint = True)
	
	def LocatorsBake(self, *args):
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraint = True, bake = True)
	def LocatorsBakeReverse(self, translate=True, rotate=True, *args): # TODO , channelBox = False
		Locators.CreateOnSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraint = True, bake = True, constrainReverse = True, constrainTranslate = translate, constrainRotate = rotate)
	
	def LocatorsRelative(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def LocatorsRelativeReverseSkipLast(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraintReverse = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def LocatorsRelativeReverse(self, *args):
		Locators.CreateAndBakeAsChildrenFromLastSelected(scale = self.floatLocatorSize.Get(), hideParent = self.checkboxLocatorHideParent.Get(), subLocator = self.checkboxLocatorSubLocator.Get(), constraintReverse = True, skipLastReverse = False, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	
	def LocatorsBakeAim(self, rotateOnly=False, *args):
		scale = self.floatLocatorSize.Get()
		distance = cmds.floatField(self.aimSpaceFloatField, query = True, value = True)
		hideParent = self.checkboxLocatorHideParent.Get()
		subLocators = self.checkboxLocatorSubLocator.Get()
		reverse = cmds.checkBox(self.aimSpaceCheckbox, query = True, value = True)

		### Compile value and return
		valueAimTarget = 1 * (-1 if reverse else 1)
		if (cmds.radioButton(self.aimSpaceRadioButtons[0], query = True, select = True)):
			axisVector = [valueAimTarget, 0, 0]
		if (cmds.radioButton(self.aimSpaceRadioButtons[1], query = True, select = True)):
			axisVector = [0, valueAimTarget, 0]
		if (cmds.radioButton(self.aimSpaceRadioButtons[2], query = True, select = True)):
			axisVector = [0, 0, valueAimTarget]

		Locators.CreateOnSelectedAim(scale = scale, hideParent = hideParent, subLocator = subLocators, rotateOnly = rotateOnly, aimVector = axisVector, distance = distance, reverse = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())

		if (distance == 0):
			cmds.warning("Aim distance is 0. Highly recommended to use non-zero value.")


	### BAKING
	def BakeSamplesSet(self, value=1, *args):
		self.fieldBakingSamples.Set(value)
	def BakeSamplesAdd(self, direction=1, *args):
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
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def BakeSelectedClassicCut(self, *args):
		Baker.BakeSelected(classic = True, preserveOutsideKeys = False, sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def BakeSelectedCustom(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = True, selectedRange = True, channelBox = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def BakeSelectedCustomCut(self, *args): # TODO , sampleBy = self.fieldBakingStep.Get()
		Baker.BakeSelected(classic = False, preserveOutsideKeys = False, selectedRange = True, channelBox = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def BakeSelectedByLastObject(self, translate=True, rotate=True, *args):
		if (translate and rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		elif (translate and not rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.translateLong, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		elif (not translate and rotate):
			Baker.BakeSelectedByLastObject(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.rotateLong, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
	def BakeSelectedByWorld(self, translate=True, rotate=True, *args):
		if (translate and rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		elif (translate and not rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.translateLong, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		elif (not translate and rotate):
			Baker.BakeSelectedByWorld(sampleBy = self.fieldBakingSamples.Get(), selectedRange = True, channelBox = False, attributes = Enums.Attributes.rotateLong, euler = self.generalInstance.menuCheckboxEulerFilter.Get())


	### ANIMATION
	def AnimationOffset(self, direction=1, step=1, *args):
		Animation.OffsetSelected(direction, step)

