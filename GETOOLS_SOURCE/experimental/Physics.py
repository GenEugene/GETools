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
# import maya.mel as mel

# from ..utils import Selector
# from ..utils import Text


# nucleusTimeScale = 1


def CreateNucleus(name="myNucleus", parent=None, *args):
	nucleus = cmds.createNode("nucleus", name = name)
	
	cmds.connectAttr("time1.outTime", nucleus + ".currentTime")

	# Parent to specific object
	if (parent != None):
		cmds.parent(nucleus, parent)
	
	# self.sliderNTimeScale.startName = nucleus
	# cmds.setAttr(nucleus + ".gravity", 0)
	# cmds.setAttr(nucleus + ".timeScale", self.sliderNucleusTimeScale.Get())
	# cmds.setAttr(nucleus + ".startFrame", self.time.values[2])
	# cmds.setAttr(nucleus + ".visibility", 0)

	return nucleus

