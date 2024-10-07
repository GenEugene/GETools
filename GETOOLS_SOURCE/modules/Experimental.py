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

import os
import ast # For safely converting strings to Python objects
import maya.cmds as cmds
# from functools import partial

from .. import Settings
from ..utils import Layers
from ..utils import Selector
# from ..utils import Blendshapes
# from ..experimental import Physics
# from ..experimental import PhysicsHair
from ..experimental import PhysicsParticle


class Experimental:
	_title = "EXPERIMENTAL"

	# from ..modules import GeneralWindow
	# def __init__(self, generalInstance: GeneralWindow.GeneralWindow):
	# def __init__(self, generalInstance):
	# def __init__(self):
		# self.generalInstance = generalInstance
	
	def UICreate(self, layoutMain):
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click test")
		# cmds.menuItem(dividerLabel = "label", divider = True)

		### MENU
		cmds.columnLayout("layoutMenuBar", parent = layoutMain, adjustableColumn = True, width = Settings.windowWidthScroll)
		cmds.menuBarLayout()

		cmds.menu(label = "Layers", tearOff = True)
		cmds.menuItem(label = "Layer Create", command = self.LayerCreate)
		cmds.menuItem(label = "Layer Create For Selected", command = self.LayerCreateForSelected)
		cmds.menuItem(label = "Layer Delete", command = self.LayerDelete)
		cmds.menuItem(label = "Layer Get Selected", command = self.LayerGetSelected)
		cmds.menuItem(label = "Layer Move", command = self.LayerMove)

		cmds.menu(label = "Presets", tearOff = True)
		cmds.menuItem(label = "Save", command = self.PresetSaveTEST)
		cmds.menuItem(label = "Read", command = self.PresetReadTEST)
		
		### BUTTONS
		countOffsets = 4
		cmds.gridLayout(parent = layoutMain, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		# cmds.button(label = "**Nucleus", command = partial(Physics.CreateNucleus, "testNucleus", None))
		cmds.button(label = "Particle", command = PhysicsParticle.CreateOnSelected)
		cmds.button(label = "P Aim", command = PhysicsParticle.CreateAimOnSelected)
		cmds.button(label = "P Combo", command = PhysicsParticle.CreateComboOnSelected)
		# cmds.button(label = "**P Chain", command = PhysicsParticle.CreateAimChainOnSelected)
		# cmds.button(label = "Hair", command = partial(PhysicsHair.CreateNHairOnSelected, None))

		# countOffsets = 2
		# cmds.gridLayout(parent = layoutMain, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		# commandGet = GeneralWindow.GetCheckboxEulerFilter()
		# cmds.button(label = "Check General Window", command = commandGet)
		# self.generalInstance.GetCheckboxEulerFilter()

	### TEST LEAYER METHODS
	def LayerCreate(*args):
		Layers.Create("testLayer")
	
	def LayerCreateForSelected(*args):
		selected = Selector.MultipleObjects()
		if (selected == None):
			return
		Layers.CreateForSelected(selected)
	
	def LayerDelete(*args):
		Layers.Delete("testLayer")
	
	def LayerGetSelected(*args):
		Layers.GetSelected()
	
	def LayerMove(*args):
		selected = Layers.GetSelected()
		if (selected == None or len(selected) < 2):
			cmds.warning("Need to select at least 2 layers")
			return
		Layers.MoveChildrenToParent(selected[:-1], selected[-1]) # FIXME main problem is layers have no selection order, they just listed from top to bottom


	### SAVE/LOAD TXT FILE
	filepathTest = "C:/Users/egataulin/Documents/_EugeneFiles/GETools/GETOOLS_SOURCE/SETTINGS/test.txt"

	def PresetSaveLogic(filepath, variables_dict, *args):
		with open(filepath, 'w') as line:
			for var_name, var_value in variables_dict.items():
				line.write("{0} = {1}\n".format(var_name, var_value))
	def PresetSaveTEST(*args): # HACK
		# Store the variables in a dictionary
		variables_dict = {
			"var1": "string one",
			"var2": 3.7,
			"var3": (0, 1, 1.3),
			"var4": "qweqwe"
		}

		Experimental.PresetSaveLogic(Experimental.filepathTest, variables_dict)
		print("Preset Saved")

	# Function to load variables from a text file
	def PresetReadLogic(filepath, *args):
		variables_dict = {}

		# Check if file exists
		if not os.path.exists(filepath):
			print(f"File '{filepath}' not found!")
			return variables_dict

		# Open the file in read mode
		with open(filepath, 'r') as f:
			for line in f:
				# Parse each line in the format "name = value"
				if '=' in line:
					var_name, var_value = line.strip().split(' = ', 1)
					
					try:
						# Use ast.literal_eval to convert strings to proper Python objects (int, float, list, etc.)
						var_value = ast.literal_eval(var_value)
					except (ValueError, SyntaxError):
						# If literal_eval fails, keep it as a string
						pass
					
					# Store the variable in the dictionary
					variables_dict[var_name] = var_value

		# Set the variables in the global namespace
		globals().update(variables_dict)
		print(f"Variables loaded from {filepath}")
		return variables_dict
	def PresetReadTEST(*args): # HACK
		result = Experimental.PresetReadLogic(Experimental.filepathTest)
		print(result)

