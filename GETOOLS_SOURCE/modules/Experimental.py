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
# from functools import partial

from .. import Settings
from ..utils import File
from ..utils import Layers
from ..utils import Selector
# from ..utils import Blendshapes
# from ..experimental import Physics
# from ..experimental import PhysicsHair
from ..experimental import PhysicsParticle


class Experimental:
	_title = "EXPERIMENTAL"

	def __init__(self, options):
		self.optionsPlugin = options
		### Check Maya version to avoid cycle import, Maya 2020 and older can't use cycle import
		if cmds.about(version = True) in ["2022", "2023", "2024", "2025"]:
			from ..modules import Options
			if isinstance(options, Options.PluginVariables):
				self.optionsPlugin = options
	
	def UICreate(self, layoutMain):
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click test")
		# cmds.menuItem(dividerLabel = "label", divider = True)

		### MENU
		cmds.columnLayout("layoutMenuBar", parent = layoutMain, adjustableColumn = True, width = Settings.windowWidth)
		cmds.menuBarLayout()

		cmds.menu(label = "Layers", tearOff = True)
		cmds.menuItem(label = "Layer Create", command = self.LayerCreate)
		cmds.menuItem(label = "Layer Create For Selected", command = self.LayerCreateForSelected)
		cmds.menuItem(label = "Layer Delete", command = self.LayerDelete)
		cmds.menuItem(label = "Layer Get Selected", command = self.LayerGetSelected)
		cmds.menuItem(label = "Layer Move", command = self.LayerMove)

		### BUTTONS
		countOffsets = 4
		cmds.gridLayout(parent = layoutMain, numberOfColumns = countOffsets, cellWidth = Settings.windowWidth / countOffsets, cellHeight = Settings.lineHeight)
		# cmds.button(label = "**Nucleus", command = partial(Physics.CreateNucleus, "testNucleus", None))
		cmds.button(label = "Particle", command = PhysicsParticle.CreateOnSelected)
		cmds.button(label = "P Aim", command = PhysicsParticle.CreateAimOnSelected)
		cmds.button(label = "P Combo", command = PhysicsParticle.CreateComboOnSelected)
		# cmds.button(label = "**P Chain", command = PhysicsParticle.CreateAimChainOnSelected)
		# cmds.button(label = "Hair", command = partial(PhysicsHair.CreateNHairOnSelected, None))

		countOffsets = 2
		cmds.gridLayout(parent = layoutMain, numberOfColumns = countOffsets, cellWidth = Settings.windowWidth / countOffsets, cellHeight = Settings.lineHeight)
		def GetCheckboxEulerFilter(*args):
			self.optionsPlugin.PrintAllOptions()
		cmds.button(label = "Print General Options", command = GetCheckboxEulerFilter)

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

