# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
import maya.mel as mel

from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Timeline

def DeleteKeys(channelBox = False, *args):
	if (Selector.MultipleObjects(1) == None):
		return

	# Calculate time range if range highlighted
	timeRange = [None, None]
	if (Timeline.CheckHighlighting()):
		timeRange = [Timeline.GetSelectedTimeRange()[0], Timeline.GetSelectedTimeRange()[1] - 1]

	# Check channel box attributes
	selectedAttributes = Selector.GetChannelBoxAttributes()
	# TODO move logic pattern to separate function
	cutAll = True
	if (channelBox == True):
		cutAll = selectedAttributes == None
	if (cutAll):
		cmds.cutKey(time = (timeRange[0], timeRange[1]))
	else:
		cmds.cutKey(time = (timeRange[0], timeRange[1]), attribute = selectedAttributes)
	

def DeleteKeyRange(*args): # XXX unused function
	mel.eval('timeSliderClearKey')

def DeleteKeysNonkeyable(*args):
	selected = cmds.ls(selection = True)
	counter = 0
	for item in selected:
		attributes = cmds.listAttr(item, channelBox = 1)
		if attributes != None:
			for j in range(len(attributes)):
				cmds.cutKey(item + "." + attributes[j])
				counter += 1
	print ("\nNonkeyable attributes deleted: {0}".format(counter))

def DeleteStaticCurves(*args):
	cmds.delete(staticChannels = True)

def FilterCurve(*args):
	cmds.filterCurve()

def SetInfinity(mode, items = None, *args):
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
		cmds.setInfinity(preInfinite = result, postInfinite = result)
	else:
		cmds.setInfinity(items, preInfinite = result, postInfinite = result)
def SetInfinityConstant(selected):
	SetInfinity(mode = 1, items = selected)
def SetInfinityCycle(selected):
	SetInfinity(mode = 2, items = selected)

