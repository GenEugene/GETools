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

from ..utils import Selector
from ..values import Enums


def Create(*args):
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	name = "MotionTrail_1"
	step = 1
	start = cmds.playbackOptions(query = True, minTime = True)
	end = cmds.playbackOptions(query = True, maxTime = True)
	cmds.snapshot(name = name, motionTrail = True, increment = step, startTime = start, endTime = end)
	selected = cmds.ls(type = Enums.Types.motionTrail)
	
	for item in selected:
		cmds.setAttr(item + Enums.MotionTrail.handle + "Shape." + Enums.MotionTrail.trailDrawMode, 1)
		cmds.setAttr(item + Enums.MotionTrail.handle + "Shape." + Enums.MotionTrail.template, 1)

def Select(*args):
	selected = cmds.ls(type = Enums.Types.motionTrail)
	if (len(selected) == 0):
		return
	
	cmds.select(clear = True)
	for item in selected:
		cmds.select(item + Enums.MotionTrail.handle, add = True)

def Delete(*args):
	selected = cmds.ls(type = Enums.Types.motionTrail)
	if (len(selected) == 0):
		return
	
	for item in selected:
		cmds.delete(item + Enums.MotionTrail.handle)

