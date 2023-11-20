# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Selector

def Create(*args):
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	name = "MotionTrail_1"
	step = 1
	start = cmds.playbackOptions(query = True, minTime = True)
	end = cmds.playbackOptions(query = True, maxTime = True)
	cmds.snapshot(name = name, motionTrail = True, increment = step, startTime = start, endTime = end)
	selected = cmds.ls(type = "motionTrail")
	
	for item in selected:
		cmds.setAttr(item + "Handle" + "Shape.trailDrawMode", 1)
		cmds.setAttr(item + "Handle" + "Shape.template", 1)

def Select(*args):
	selected = cmds.ls(type = "motionTrail")
	if (len(selected) == 0):
		return
	
	cmds.select(clear = True)
	for item in selected:
		cmds.select(item + "Handle", add = True)

def Delete(*args):
	selected = cmds.ls(type = "motionTrail")
	if (len(selected) == 0):
		return
	
	for item in selected:
		cmds.delete(item + "Handle")

def CreateCurveFromTrajectory(): # TODO rework tool and add to module
	# Variables
	step = 1
	degree = 3
	# Names
	mtName = "newMotionTrail"
	mtFinalName = mtName + "Handle"
	curveName = "testCurve"


	# Get time start/end
	start = cmds.playbackOptions(q=1, min=1)
	end = cmds.playbackOptions(q=1, max=1)
	# Create motion trail
	cmds.snapshot(n = mtName, mt=1, i=step, st = start, et = end)

	# Get points from motion trail
	cmds.select(mtFinalName, r=1)
	selected = cmds.ls(sl=1, dag=1, et="snapshotShape")
	pts = cmds.getAttr(selected[0] + ".pts")
	size = len(pts)
	for i in range(size):
		pts[i] = pts[i][0:3]
		#print "{0}: {1}".format(i, pts[i])

	# Create curve
	newCurve = cmds.curve(n = curveName, d = degree, p = pts)

	# End
	cmds.delete(mtFinalName)
	cmds.select(cl=1)