# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
# import maya.mel as mel

# from GETOOLS_SOURCE.utils import Selector

def RotateOrderVisibility(on = True, *args):
	selected = cmds.ls(selection = True, type = "transform")
	for item in selected:
		cmds.setAttr(item + ".rotateOrder", channelBox = on)

def SegmentScaleCompensate(value = 0, *args):
	selected = cmds.ls(selection = True, type = "joint")
	for item in selected:
		cmds.setAttr(item + ".segmentScaleCompensate", value)

def JointDrawStyle(mode = 0, *args):
	selected = cmds.ls(selection = True, type = "joint")
	for item in selected:
		cmds.setAttr(item + ".drawStyle", mode)

def SelectJointsInScene(): # TODO make universal for other types
	selected = cmds.ls(type = "joint")
	cmds.select(selected)

def CheckShapeType(element, type):
	elementShape = element + "Shape"
	if (cmds.objExists(elementShape)):
		return cmds.objectType(elementShape) == type
	else:
		return False

