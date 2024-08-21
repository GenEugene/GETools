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
import maya.mel as mel

from ..utils import Attributes
from ..utils import Selector
from ..utils import Timeline


def DeleteKeys(channelBox=False, *args):
	if (Selector.MultipleObjects(1) == None):
		return

	# Calculate time range if range highlighted
	timeRange = [None, None]
	if (Timeline.CheckHighlighting()):
		timeRange = [Timeline.GetSelectedTimeRange()[0], Timeline.GetSelectedTimeRange()[1] - 1]

	# Check channel box attributes
	selectedAttributes = Attributes.GetAttributesSelectedFromChannelBox()
	# TODO move logic pattern to separate function
	cutAll = True
	if (channelBox):
		cutAll = selectedAttributes == None
	if (cutAll):
		cmds.cutKey(time = (timeRange[0], timeRange[1]))
	else:
		cmds.cutKey(time = (timeRange[0], timeRange[1]), attribute = selectedAttributes)
def DeleteKeyRange(*args): # TODO unused, check if redundant
	mel.eval('timeSliderClearKey')
def DeleteKeysNonkeyable(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return

	counter = 0
	for item in selectedList:
		attributes = cmds.listAttr(item, channelBox = 1)
		if attributes != None:
			for j in range(len(attributes)):
				cmds.cutKey(item + "." + attributes[j])
				counter += 1
	print ("\nNonkeyable attributes deleted: {0}".format(counter))
def DeleteStaticCurves(*args):
	# Check selected objects
	Selector.MultipleObjects(1)
	cmds.delete(staticChannels = True)

def EulerFilterOnObject(obj):
	cmds.filterCurve(obj)
	cmds.selectKey(clear = True)
	print("######## Euler Filtered {0}".format(obj))
def EulerFilterOnObjects(objects):
	if (objects == None):
		return None
	for item in objects:
		EulerFilterOnObject(item)
def EulerFilterOnSelected(*args):
	# Check selected objects
	selected = Selector.MultipleObjects(1)
	if (selected == None):
		return None
	EulerFilterOnObjects(selected)
	
def SetInfinity(mode, items=None, *args):
	result = ""
	if (mode == 1):
		result = "constant"
	elif (mode == 2):
		result = "linear"
	elif (mode == 3):
		result = "cycle"
	elif (mode == 4):
		result = "cycleRelative"
	elif (mode == 5):
		result = "oscillate"
	
	if (items == None):
		if (Selector.MultipleObjects(1) == None):
			return
		cmds.setInfinity(preInfinite = result, postInfinite = result)
	else:
		cmds.setInfinity(items, preInfinite = result, postInfinite = result)

def SetInfinityConstant(selected):
	SetInfinity(mode = 1, items = selected)
def SetInfinityLinear(selected):
	SetInfinity(mode = 2, items = selected)
def SetInfinityCycle(selected):
	SetInfinity(mode = 3, items = selected)
def SetInfinityCycleRelative(selected):
	SetInfinity(mode = 4, items = selected)
def SetInfinityOscillate(selected):
	SetInfinity(mode = 5, items = selected)

def Offset(selected, time, attributes=None):
	if (attributes == None):
		cmds.keyframe(selected, edit = True, relative = True, option = "over", includeUpperBound = True, timeChange = time)
	else:
		cmds.keyframe(selected, edit = True, relative = True, option = "over", includeUpperBound = True, timeChange = time, attribute = attributes)
def OffsetSelected(direction=1, step=1): # use if needed later # , channelBox = False
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	time = step * direction
	selectedAttributes = Attributes.GetAttributesSelectedFromChannelBox()

	count = len(selectedList)
	for i in range(count):
		if (count == 1):
			timeCurrent = time
		else:
			timeCurrent = i * time
		
		Offset(selectedList[i], timeCurrent, selectedAttributes)

