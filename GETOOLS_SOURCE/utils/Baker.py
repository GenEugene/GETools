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

from ..utils import Animation
from ..utils import Constraints
from ..utils import Selector
from ..utils import Timeline


def BakeSelected(classic=True, preserveOutsideKeys=True, sampleBy=1.0, selectedRange=False, channelBox=False, attributes=None, euler=False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	# Calculate time range if range highlighted
	if (selectedRange and Timeline.CheckHighlighting()):
		rangeCurrent = Timeline.GetSelectedTimeRange()
		timeRange = [rangeCurrent[0], rangeCurrent[1] - 1]
	else:
		rangeCurrent = Timeline.GetTimeMinMax()
		timeRange = [rangeCurrent[0], rangeCurrent[1]]

	cmds.refresh(suspend = True)
	if (classic):
		# Check channel box attributes
		# TODO move logic pattern to separate function
		bakeRegular = True
		selectedAttributes = Selector.GetChannelBoxSelectedAttributes()
		if (channelBox):
			bakeRegular = selectedAttributes == None
		if (bakeRegular):
			if (attributes == None):
				cmds.bakeResults(time = (timeRange[0], timeRange[1]), preserveOutsideKeys = preserveOutsideKeys, simulation = True, minimizeRotation = True, sampleBy = sampleBy)
			else:
				cmds.bakeResults(time = (timeRange[0], timeRange[1]), preserveOutsideKeys = preserveOutsideKeys, simulation = True, minimizeRotation = True, sampleBy = sampleBy, attribute = attributes)
		else:
			cmds.bakeResults(time = (timeRange[0], timeRange[1]), preserveOutsideKeys = preserveOutsideKeys, simulation = True, minimizeRotation = True, sampleBy = sampleBy, attribute = selectedAttributes)
	else:
		timeCurrent = Timeline.GetTimeCurrent()
		timeRange[1] = timeRange[1] + 1
		for i in range(int(timeRange[0]), int(timeRange[1])):
			Timeline.SetTimeCurrent(i)
			cmds.setKeyframe(respectKeyable = True, animated = False, preserveCurveShape = True)
		Timeline.SetTimeCurrent(timeCurrent)
		if (not preserveOutsideKeys):
			cmds.cutKey(time = (None, timeRange[0] - 1)) # to left
			cmds.cutKey(time = (timeRange[1], None)) # to right
	cmds.refresh(suspend = False)

	if (euler):
		Animation.EulerFilterOnObjects(selectedList)

def BakeSelectedByLastObject(pairOnly=False, sampleBy=1.0, selectedRange=False, channelBox=False, attributes=None, euler=False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	
	# Cut list by last 2 items
	if pairOnly:
		selectedList = (selectedList[-2], selectedList[-1])
	
	# Constrain objects to last object
	Constraints.ConstrainListToLastElement(selected = selectedList)
	
	# Bake objects
	cmds.select(selectedList)
	cmds.select(selectedList[-1], deselect = True)
	BakeSelected(sampleBy = sampleBy, selectedRange = selectedRange, channelBox = channelBox, attributes = attributes, euler = euler)

	# Delete constraints
	Constraints.DeleteConstraints(selectedList[:-1])

	cmds.select(selectedList)
	return selectedList

def BakeSelectedByWorld(sampleBy=1.0, selectedRange=False, channelBox=False, attributes=None, euler=False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	world = cmds.group(world = True, empty = True)
	selectedList.append(world)
	cmds.select(selectedList, replace = True)
	BakeSelectedByLastObject(sampleBy = sampleBy, selectedRange = selectedRange, channelBox = channelBox, attributes = attributes, euler = euler)
	cmds.delete(world)

# def BakeReverseParentOnPair(): # TODO add child locator on parent object (OPTIONAL)
# 	selectedList = BakeSelectedByLastObject(pairOnly = True)
# 	Constraints.ConstrainSecondToFirstObject(selectedList[0], selectedList[1], maintainOffset = True)

