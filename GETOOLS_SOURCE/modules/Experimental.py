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
# from ..utils import Blendshapes
# from ..experimental import Physics
# from ..experimental import PhysicsHair
from ..experimental import PhysicsParticle


class Experimental:
	_title = "EXPERIMENTAL"

	def __init__(self):
		pass
	
	def UICreate(self, layoutMain):
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click test")
		
		countOffsets = 4
		cmds.gridLayout(parent = layoutMain, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		
		# cmds.button(label = "**Nucleus", command = partial(Physics.CreateNucleus, "testNucleus", None))
		cmds.button(label = "Particle", command = PhysicsParticle.CreateOnSelected)
		cmds.button(label = "P Aim", command = PhysicsParticle.CreateAimOnSelected)
		cmds.button(label = "P Combo", command = PhysicsParticle.CreateComboOnSelected)
		# cmds.button(label = "**P Chain", command = PhysicsParticle.CreateAimChainOnSelected)
		# cmds.button(label = "Hair", command = partial(PhysicsHair.CreateNHairOnSelected, None))

