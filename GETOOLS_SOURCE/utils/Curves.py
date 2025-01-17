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


_curveName = "newCurve"
_curveDegree = 1


def CreateCurveFromSelectedObjects(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return None

	positions = []

	for item in selectedList:
		position = cmds.xform(item, query = True, translation = True, worldSpace = True)
		positions.append(position)

	curve = cmds.curve(name = _curveName, degree = _curveDegree, point = positions)
	return curve

def CreateCurveFromTrajectory(*args): # TODO rework
	### Variables
	step = 1
	degree = 3
	
	### Names
	mtName = "newMotionTrail"
	mtFinalName = mtName + Enums.MotionTrail.handle
	curveName = "testCurve"


	### Get time start/end
	start = cmds.playbackOptions(query = 1, min = 1)
	end = cmds.playbackOptions(query = 1, max = 1)
	
	### Create motion trail
	cmds.snapshot(name = mtName, motionTrail = 1, increment = step, startTime = start, endTime = end)

	### Get points from motion trail
	cmds.select(mtFinalName, replace = 1)
	selected = cmds.ls(selection = 1, dagObjects = 1, exactType = Enums.MotionTrail.snapshotShape)
	pts = cmds.getAttr(selected[0] + "." + Enums.MotionTrail.pts)
	size = len(pts)
	for i in range(size):
		pts[i] = pts[i][0:3]
		#print "{0}: {1}".format(i, pts[i])

	### Create curve
	newCurve = cmds.curve(name = curveName, degree = degree, point = pts)

	### End
	cmds.delete(mtFinalName)
	cmds.select(clear = 1)

	return newCurve

def SetupSpaceDeformation(curves=None, *args):
	if curves is None:
		cmds.warning("No curves provided")
		return None
	
	# 1. Get curves list
	# 2. Get latest curve from list as a deformation curve
	# 3. Create a "Sweep Mesh" on deformation curve with "Line" profile, interpolation mode "Start To End" and steps
	# 4. Connect other curves to "Sweep Mesh" with "Wrap" deformer using "Volume" falloff mode

