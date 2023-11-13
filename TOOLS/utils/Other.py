# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
import maya.mel as mel
from utils import Selector

def RotateOrderVisibility(on = True, *args):
	selected = cmds.ls(selection = 1, long = 1)
	for i in range(len(selected)):
		cmds.setAttr(selected[i] + ".rotateOrder", channelBox = on)

def SegmentScaleCompensate(value = 0, *args):
	jointList = cmds.ls(selection = 1, type = "joint")
	for i in jointList:
		cmds.setAttr(i + ".segmentScaleCompensate", value)

def JointDrawStyle(mode = 0, *args):
	selected = cmds.ls(selection = 1)
	for i in range(len(selected)):
		cmds.setAttr(selected[i] + ".drawStyle", mode)

def DeleteKeys(*args):
	if (Selector.MultipleObjects(1) == None):
		return
	cmds.cutKey()
	print("Animation deleted")

def DeleteKeyRange(*args):
	mel.eval('timeSliderClearKey')

def KeysNonkeyableDelete(*args):
	objects = cmds.ls(selection = 1)
	counter = 0
	for i in range(len(objects)):
		attributes = cmds.listAttr(objects[i], channelBox = 1)
		if attributes != None:
			for j in range(len(attributes)):
				cmds.cutKey(objects[i] + "." + attributes[j])
				counter += 1
	print ("\t{} nonkeyable detected and deleted".format(counter))

def SelectJointsInScene():
	selectedJoints = cmds.ls(type = "joint")
	cmds.select(selectedJoints)

def SetInfinityConstant(selected):
	cmds.setInfinity(selected, preInfinite = "constant", postInfinite = "constant")

def SetInfinityCycle(selected):
	cmds.setInfinity(selected, preInfinite = "cycle", postInfinite = "cycle")