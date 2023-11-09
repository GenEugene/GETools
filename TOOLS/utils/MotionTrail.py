# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from utils import Selector

def Create(self, *args):
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	_name = "MotionTrail_1"
	_step = 1
	_start = cmds.playbackOptions(query = True, minTime = True)
	_end = cmds.playbackOptions(query = True, maxTime = True)
	cmds.snapshot(name = _name, motionTrail = True, increment = _step, startTime = _start, endTime = _end)
	_trails = cmds.ls(type = "motionTrail")
	for item in _trails:
		cmds.setAttr(item + "Handle" + "Shape.trailDrawMode", 1)
		cmds.setAttr(item + "Handle" + "Shape.template", 1)

def Select(self, *args):
	_trails = cmds.ls(type = "motionTrail")
	if (len(_trails) == 0):
		return
	cmds.select(clear = True)
	for item in _trails:
		cmds.select(item + "Handle", add = True)

def Delete(self, *args):
	_trails = cmds.ls(type = "motionTrail")
	if (len(_trails) == 0):
		return
	for item in _trails:
		cmds.delete(item + "Handle")