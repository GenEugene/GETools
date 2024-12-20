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

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene https://discord.gg/heMxJhTqCz
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds
from functools import partial

from .. import Settings
from ..utils import Colors
# from ..utils import Selector
# from ..values import Enums


class TransformationsAnnotations:
	space = "WORLD SPACE uses global axes orientations.\nLOCAL SPACE uses parent space, useful when selected object is a child of other object.\nOBJECT SPACE uses selected objects' axes and move accordingly arrows."
	relative = "Current position used as a start point resulting move addition each step.\nDeactivate to use absolute mode to set specific coordinates."
	preserveChildPosition = "Child object will stay on the same position while selected object will be moved.\nVery useful when you need to tweak object's position in the middle of hierarchy."
	pivot = "Move pivot of selected objects instead of moving objects transform nodes"
	multiplier = "Extra multiplier for DIRECTION and DISTANCE values."

	editPivot = "Toggle pivot editing for selected objects.\nThe same action as 'D' hotkey on keyboard."
	pivotOn = "Show pivot attributes in channel box"
	pivotOff = "Hide pivot attributes in channel box"

	_negativePositive = "-+ symbols mean negative and positive directions"
	direction = "XYZ values for directional movement"
	moveDirection = "Apply XYZ movement with direction values.\n{0}.".format(_negativePositive)
	distance = "Distance value for separate axes movement"
	moveDistance = "Apply axis movement using distance.\n{0}.".format(_negativePositive)

class Transformations:
	_version = "v1.0"
	_name = "TRANSFORMATIONS"
	_title = _name + " " + _version

	def __init__(self, options):
		self.optionsPlugin = options
		### Check Maya version to avoid cycle import, Maya 2020 and older can't use cycle import
		if cmds.about(version = True) in ["2022", "2023", "2024", "2025"]:
			from . import Options
			if isinstance(options, Options.PluginVariables):
				self.optionsPlugin = options

		### UI elements with values
		self.radioButtonGrpSpace = None
		self.checkBoxRelative = None
		self.checkBoxPreserveChildPosition = None
		self.checkBoxPivot = None
		self.floatFieldMultiplier = None
		self.floatFieldGrpDirection = None
		self.floatFieldDistance = None
	def UICreate(self, layoutMain):
		self.UILayoutLocators(layoutMain)
		cmds.separator(parent = layoutMain, height = Settings.separatorHeight, style = "none")
	def UILayoutLocators(self, layoutMain):
		cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "MOVE", collapsable = True, backgroundColor = Settings.frames2Color, highlightColor = Colors.green100, marginWidth = 0, marginHeight = 0, borderVisible = True)
		layoutColumn = cmds.columnLayout(adjustableColumn = True)

		self.radioButtonGrpSpace = cmds.radioButtonGrp(parent = layoutColumn, label = "Space: ", labelArray3 = ["World", "Local", "Object"], select = 1, numberOfRadioButtons = 3, columnWidth4 = (60, 50, 50, 50), columnAlign = [(1, "right"), (2, "center"), (3, "center"), (4, "center")], height = Settings.lineHeight, annotation = TransformationsAnnotations.space)
		self.radioButtonGrpSpace = self.radioButtonGrpSpace.replace(Settings.windowName + "|", "") # HACK fix for docked window only. Don't know how to avoid issue

		cmds.rowLayout(parent = layoutColumn, numberOfColumns = 3, columnWidth3 = (70, 150, 50), columnAlign = [(1, "center"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)], height = Settings.lineHeight)
		self.checkBoxRelative = cmds.checkBox(label = "Relative", value = True, annotation = TransformationsAnnotations.relative)
		self.checkBoxPreserveChildPosition = cmds.checkBox(label = "Preserve Child Position", value = False, annotation = TransformationsAnnotations.preserveChildPosition)
		self.checkBoxPivot = cmds.checkBox(label = "Pivot", value = False, annotation = TransformationsAnnotations.pivot)

		cmds.rowLayout(parent = layoutColumn, adjustableColumn = 2, numberOfColumns = 5, columnWidth5 = (60, 50, 60, 50, 50), columnAlign = [(1, "right"), (2, "center"), (3, "center"), (4, "center"), (5, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0), (4, "both", 0), (5, "both", 0)], height = Settings.lineHeight)
		cmds.text(label = "Multiplier: ", annotation = TransformationsAnnotations.multiplier)
		self.floatFieldMultiplier = cmds.floatField(value = 1, precision = 3, annotation = TransformationsAnnotations.multiplier)
		cmds.popupMenu()
		cmds.menuItem(label = "0.001", command = partial(self.SetMultiplier, 0.001))
		cmds.menuItem(label = "0.01", command = partial(self.SetMultiplier, 0.01))
		cmds.menuItem(label = "0.1", command = partial(self.SetMultiplier, 0.1))
		cmds.menuItem(label = "0.2", command = partial(self.SetMultiplier, 0.1))
		cmds.menuItem(label = "0.5", command = partial(self.SetMultiplier, 0.5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1", command = partial(self.SetMultiplier, 1))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1.05", command = partial(self.SetMultiplier, 1.05))
		cmds.menuItem(label = "1.1", command = partial(self.SetMultiplier, 1.1))
		cmds.menuItem(label = "1.5", command = partial(self.SetMultiplier, 1.5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "2", command = partial(self.SetMultiplier, 2))
		cmds.menuItem(label = "3", command = partial(self.SetMultiplier, 3))
		cmds.menuItem(label = "4", command = partial(self.SetMultiplier, 4))
		cmds.menuItem(label = "5", command = partial(self.SetMultiplier, 5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "10", command = partial(self.SetMultiplier, 10))
		cmds.menuItem(label = "100", command = partial(self.SetMultiplier, 100))
		cmds.menuItem(label = "1000", command = partial(self.SetMultiplier, 1000))
		cmds.button(label = "Edit Pivot", command = cmds.EnterEditModePress, backgroundColor = Colors.yellow10, annotation = TransformationsAnnotations.editPivot)
		cmds.button(label = "Pivot On", command = partial(self.SetPivotAttributes, True), backgroundColor = Colors.blackWhite80, annotation = TransformationsAnnotations.pivotOn)
		cmds.button(label = "Pivot Off", command = partial(self.SetPivotAttributes, False), backgroundColor = Colors.blackWhite80, annotation = TransformationsAnnotations.pivotOff)

		rowLayoutDirection = cmds.rowLayout(parent = layoutColumn, adjustableColumn = 2, numberOfColumns = 2, columnWidth2 = (188, 60), columnAlign = [(1, "right"), (2, "center")], columnAttach = [(1, "both", 0), (2, "both", 0)], height = Settings.lineHeight)
		self.floatFieldGrpDirection = cmds.floatFieldGrp(parent = rowLayoutDirection, label = "Direction: ", numberOfFields = 3, columnWidth4 = (60, 40, 40, 40), value = [0, 0, 0, 0], columnAlign = [(1, "right"), (2, "center"), (3, "center"), (4, "center")], annotation = TransformationsAnnotations.direction)
		self.floatFieldGrpDirection = self.floatFieldGrpDirection.replace(Settings.windowName + "|", "") # HACK fix for docked window only. Don't know how to avoid issue
		cmds.popupMenu()
		cmds.menuItem(label = "0, 0, 0", command = partial(self.SetDirection, [0, 0, 0]))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1, 0, 0", command = partial(self.SetDirection, [1, 0, 0]))
		cmds.menuItem(label = "0, 1, 0", command = partial(self.SetDirection, [0, 1, 0]))
		cmds.menuItem(label = "0, 0, 1", command = partial(self.SetDirection, [0, 0, 1]))
		cmds.gridLayout(parent = rowLayoutDirection, numberOfColumns = 2, cellWidth = 44, cellHeight = Settings.lineHeight)
		cmds.button(label = "-XYZ", command = partial(self.MoveSelected, 0, True), backgroundColor = Colors.orange10, annotation = TransformationsAnnotations.moveDirection)
		cmds.button(label = "+XYZ", command = partial(self.MoveSelected, 0, False), backgroundColor = Colors.orange50, annotation = TransformationsAnnotations.moveDirection)
		
		cmds.rowLayout(parent = layoutColumn, adjustableColumn = 2, numberOfColumns = 3, columnWidth3 = (60, 50, 156), columnAlign = [(1, "right"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)], height = Settings.lineHeight)
		cmds.text(label = "Distance: ", annotation = TransformationsAnnotations.distance)
		self.floatFieldDistance = cmds.floatField(value = 1, precision = 3, annotation = TransformationsAnnotations.distance)
		cmds.popupMenu()
		cmds.menuItem(label = "0", command = partial(self.SetDistance, 0))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "0.01", command = partial(self.SetDistance, 0.01))
		cmds.menuItem(label = "0.1", command = partial(self.SetDistance, 0.1))
		cmds.menuItem(label = "0.5", command = partial(self.SetDistance, 0.5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1", command = partial(self.SetDistance, 1))
		cmds.menuItem(label = "2", command = partial(self.SetDistance, 2))
		cmds.menuItem(label = "3", command = partial(self.SetDistance, 3))
		cmds.menuItem(label = "5", command = partial(self.SetDistance, 5))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "10", command = partial(self.SetDistance, 10))
		cmds.menuItem(label = "100", command = partial(self.SetDistance, 100))
		cmds.menuItem(label = "1000", command = partial(self.SetDistance, 1000))
		cmds.gridLayout(numberOfColumns = 6, cellWidth = 26, cellHeight = Settings.lineHeight)
		cmds.button(label = "-X", command = partial(self.MoveSelected, 1, True), backgroundColor = Colors.red10, annotation = TransformationsAnnotations.moveDistance)
		cmds.button(label = "+X", command = partial(self.MoveSelected, 1, False), backgroundColor = Colors.red50, annotation = TransformationsAnnotations.moveDistance)
		cmds.button(label = "-Y", command = partial(self.MoveSelected, 2, True), backgroundColor = Colors.green10, annotation = TransformationsAnnotations.moveDistance)
		cmds.button(label = "+Y", command = partial(self.MoveSelected, 2, False), backgroundColor = Colors.green50, annotation = TransformationsAnnotations.moveDistance)
		cmds.button(label = "-Z", command = partial(self.MoveSelected, 3, True), backgroundColor = Colors.blue10, annotation = TransformationsAnnotations.moveDistance)
		cmds.button(label = "+Z", command = partial(self.MoveSelected, 3, False), backgroundColor = Colors.blue50, annotation = TransformationsAnnotations.moveDistance)

	def SetMultiplier(self, value, *args):
		cmds.floatField(self.floatFieldMultiplier, edit = True, value = value)
	def SetDirection(self, value, *args):
		cmds.floatFieldGrp(self.floatFieldGrpDirection, edit = True, value = [value[0], value[1], value[2], 0])
	def SetDistance(self, value, *args):
		cmds.floatField(self.floatFieldDistance, edit = True, value = value)
	def SetPivotAttributes(self, value, *args):
		selected = cmds.ls(selection = True)
		for i in range(len(selected)):
			cmds.setAttr(selected[i] + ".rotatePivotX", channelBox = value)
			cmds.setAttr(selected[i] + ".rotatePivotY", channelBox = value)
			cmds.setAttr(selected[i] + ".rotatePivotZ", channelBox = value)
			cmds.setAttr(selected[i] + ".scalePivotX", channelBox = value)
			cmds.setAttr(selected[i] + ".scalePivotY", channelBox = value)
			cmds.setAttr(selected[i] + ".scalePivotZ", channelBox = value)

	def MoveSelected(self, axis, reverse=False, *args):
		space = cmds.radioButtonGrp(self.radioButtonGrpSpace, query = True, select = True)
		isWorldSpace = space == 1
		isLocalSpace = space == 2
		isObjectSpace = space == 3

		relative = cmds.checkBox(self.checkBoxRelative, query = True, value = True)
		preserveChildPosition = cmds.checkBox(self.checkBoxPreserveChildPosition, query = True, value = True)
		pivot = cmds.checkBox(self.checkBoxPivot, query = True, value = True)

		direction = [0, 0, 0]
		if axis == 0:
			direction = cmds.floatFieldGrp(self.floatFieldGrpDirection, query = True, value = True)
		else:
			distance = cmds.floatField(self.floatFieldDistance, query = True, value = True)
			if axis == 1:
				direction = [distance, 0, 0]
			if axis == 2:
				direction = [0, distance, 0]
			if axis == 3:
				direction = [0, 0, distance]

		multiplier = cmds.floatField(self.floatFieldMultiplier, query = True, value = True)
		multiplier = multiplier * (-1 if reverse else 1)
		direction[0] = direction[0] * multiplier
		direction[1] = direction[1] * multiplier
		direction[2] = direction[2] * multiplier

		selected = cmds.ls(selection = True)
		selectedFinal = []
		if (pivot):
			for i in range (len(selected)):
				selectedFinal.append(selected[i] + ".scalePivot")
				selectedFinal.append(selected[i] + ".rotatePivot")
		else:
			selectedFinal = selected;

		cmds.move(direction[0], direction[1], direction[2], selectedFinal, worldSpace = isWorldSpace, objectSpace = isObjectSpace, localSpace = isLocalSpace, relative = relative, preserveChildPosition = preserveChildPosition)

