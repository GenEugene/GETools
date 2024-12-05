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
# from functools import partial

from .. import Settings
# from ..utils import Animation
# from ..utils import Baker
# from ..utils import ChainDistributionRig
from ..utils import Colors
# from ..utils import Locators
# from ..utils import Selector
# from ..utils import Timeline
# from ..values import Enums


class TransformationsAnnotations:
	annotation = "xxxxxxxxxxxxxxxxxxx"

class TransformationsSettings:
	value = 0

class Transformations:
	_version = "v0.0"
	_name = "TRANSFORMATIONS"
	_title = _name + " " + _version

	def __init__(self, options):
		self.optionsPlugin = options
		### Check Maya version to avoid cycle import, Maya 2020 and older can't use cycle import
		if cmds.about(version = True) in ["2022", "2023", "2024", "2025"]:
			from . import Options
			if isinstance(options, Options.PluginVariables):
				self.optionsPlugin = options

		###
		# self.aimSpaceFloatField = None
		# self.aimSpaceRadioButtons = [None, None, None]
		# self.aimSpaceCheckbox = None

	def UICreate(self, layoutMain):
		self.UILayoutLocators(layoutMain)
		cmds.separator(parent = layoutMain, height = Settings.separatorHeight, style = "none")
	
	def UILayoutLocators(self, layoutMain):
		cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "MOVE", collapsable = True, backgroundColor = Settings.frames2Color, highlightColor = Colors.green100, marginWidth = 0, marginHeight = 0, borderVisible = True)
		layoutColumn = cmds.columnLayout(adjustableColumn = True) # , rowSpacing = Settings.columnLayoutRowSpacing

		cmds.radioButtonGrp(parent = layoutColumn, label = "Space: ", labelArray3 = ["World", "Local", "Object"], numberOfRadioButtons = 3, columnWidth4 = [60, 60, 60, 60], columnAlign = [(1, "right"), (2, "center"), (3, "center"), (4, "center")], height = Settings.lineHeight)
		
		rowLayout = cmds.rowLayout(adjustableColumn = 2, numberOfColumns = 2, columnWidth2 = (220, 30), columnAlign = [(1, "right"), (2, "center")], columnAttach = [(1, "both", 0), (2, "both", 0)], height = Settings.lineHeight)
		cmds.floatFieldGrp(parent = rowLayout, label = "Direction: ", numberOfFields = 3, columnWidth4 = [60, 50, 50, 50], value = (0, 0, 0, 0), columnAlign = [(1, "right"), (2, "center"), (3, "center"), (4, "center")])
		cmds.popupMenu()
		cmds.menuItem(label = "X = 1")
		cmds.menuItem(label = "Y = 1")
		cmds.menuItem(label = "Z = 1")
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1, 0, 0")
		cmds.menuItem(label = "0, 1, 0")
		cmds.menuItem(label = "0, 0, 1")
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "-1, 0, 0")
		cmds.menuItem(label = "0, -1, 0")
		cmds.menuItem(label = "0, 0, -1")
		cmds.button(parent = rowLayout, label = "Zero")

		cmds.rowLayout(parent = layoutColumn, numberOfColumns = 3, columnWidth3 = (60, 70, 110), columnAlign = [(1, "right"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)], height = Settings.lineHeight)
		cmds.text(label = "Multiplier: ")
		cmds.floatField(value = 1, precision = 3, minValue = 0)
		cmds.popupMenu()
		cmds.menuItem(label = "0.01")
		cmds.menuItem(label = "0.1")
		cmds.menuItem(label = "0.5")
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "1")
		cmds.menuItem(label = "2")
		cmds.menuItem(label = "5")
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "10")
		cmds.menuItem(label = "100")
		cmds.menuItem(label = "1000")
		cmds.checkBox(label = "Reverse Direction", value = False)

		cmds.rowLayout(parent = layoutColumn, numberOfColumns = 3, columnWidth3 = (140, 50, 80), columnAlign = [(1, "center"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)], height = Settings.lineHeight)
		cmds.checkBox(label = "Preserve Child Position", value = False)
		cmds.checkBox(label = "Pivot", value = False)
		cmds.button(label = "Show Pivot")

		cmds.rowLayout(parent = layoutColumn, numberOfColumns = 4, columnWidth4 = (60, 60, 60, 60), columnAlign = [(1, "right"), (2, "center"), (3, "center"), (4, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0), (4, "both", 0)], height = Settings.lineHeight)
		cmds.text(label = "Move: ")
		cmds.button(label = "X", backgroundColor = Colors.red10)
		cmds.button(label = "Y", backgroundColor = Colors.green10)
		cmds.button(label = "Z", backgroundColor = Colors.blue10)


	def MoveSelected(self, *args): # TODO
		vector = (0, 1, 0)
		selected = cmds.ls(selection = True)

		cmds.move(vector[0], vector[1], vector[2], selected, worldSpace = True, objectSpace = True, localSpace = True, relative = True)

		# preserveChildPosition

		# cmds.setAttr(item + "." + Enums.Attributes.rotatePivotX, channelBox = on)
		# cmds.setAttr(item + "." + Enums.Attributes.rotatePivotY, channelBox = on)
		# cmds.setAttr(item + "." + Enums.Attributes.rotatePivotZ, channelBox = on)

		# cmds.setAttr(item + "." + Enums.Attributes.scalePivotX, channelBox = on)
		# cmds.setAttr(item + "." + Enums.Attributes.scalePivotX, channelBox = on)
		# cmds.setAttr(item + "." + Enums.Attributes.scalePivotX, channelBox = on)

