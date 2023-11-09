# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from utils import Selector
from utils import Timeline
from utils import Constraints

def BakeSelected(classic = True, preserveOutsideKeys = True):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	selectedRange = Timeline.GetSelectedTimeRange()
	if (selectedRange[1] - selectedRange[0] > 1):
		timeMinMax = selectedRange
		timeMinMax[1] = timeMinMax[1] - 1
	else:
		timeMinMax = list(Timeline.GetTimeMinMax())
	
	print(timeMinMax)
	
	if (classic):
		cmds.bakeResults(time = (timeMinMax[0], timeMinMax[1]), preserveOutsideKeys = preserveOutsideKeys, simulation = True)
	else:
		timeCurrent = Timeline.GetTimeCurrent()
		timeMinMax[1] = timeMinMax[1] + 1
		for i in range(int(timeMinMax[0]), int(timeMinMax[1])):
			Timeline.SetTimeCurrent(i)
			cmds.setKeyframe(respectKeyable = True, animated = False, preserveCurveShape = True)
		Timeline.SetTimeCurrent(timeCurrent)

def BakeSelectedByLastObject(pairOnly = False):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	
	# Cut list by last 2 items
	if pairOnly:
		selectedList = (selectedList[-2], selectedList[-1])
	
	# Constrain objects to last object
	Constraints.ConstrainListToLastElement(selectedList = selectedList)
	
	# Bake objects
	cmds.select(selectedList)
	cmds.select(selectedList[-1], deselect = True)
	BakeSelected()

	# Delete constraints
	for i in range(len(selectedList)):
		if (i == len(selectedList) - 1):
			break
		children = cmds.listRelatives(selectedList[i], type = "constraint")
		for child in children:
			cmds.delete(child)

	cmds.select(selectedList)
	return selectedList


# def BakeReverseParentOnPair(): # TODO add child locator on parent object (OPTIONAL)
# 	selectedList = BakeSelectedByLastObject(pairOnly = True)
# 	Constraints.ConstrainSecondToFirstObject(selectedList[0], selectedList[1], maintainOffset = True)