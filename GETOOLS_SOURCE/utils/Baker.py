# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Constraints
from GETOOLS_SOURCE.utils import Locators
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Timeline

def BakeSelected(classic = True, preserveOutsideKeys = True, sampleBy = 1.0, selectedRange = False, channelBox = False, attributes = None):
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
		selectedAttributes = Selector.GetChannelBoxAttributes()
		if (channelBox == True):
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

def BakeSelectedByLastObject(pairOnly = False, sampleBy = 1.0, selectedRange = False, channelBox = False, attributes = None):
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
	BakeSelected(sampleBy = sampleBy, selectedRange = selectedRange, channelBox = channelBox, attributes = attributes)

	# Delete constraints
	Constraints.DeleteConstraints(selectedList[:-1])

	cmds.select(selectedList)
	return selectedList

def BakeSelectedByWorld(sampleBy = 1.0, selectedRange = False, channelBox = False, attributes = None):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	world = Locators.Create()
	selectedList.append(world)
	cmds.select(selectedList, replace = True)
	BakeSelectedByLastObject(sampleBy = sampleBy, selectedRange = selectedRange, channelBox = channelBox, attributes = attributes)
	cmds.delete(world)

# def BakeReverseParentOnPair(): # TODO add child locator on parent object (OPTIONAL)
# 	selectedList = BakeSelectedByLastObject(pairOnly = True)
# 	Constraints.ConstrainSecondToFirstObject(selectedList[0], selectedList[1], maintainOffset = True)