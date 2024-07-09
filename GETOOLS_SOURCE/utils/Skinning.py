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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds

from ..utils import Selector
from ..values import Enums

def CopySkinWeightsFromLastMesh(*args):
	selected = Selector.MultipleObjects(2)
	if (selected == None):
		return
	
	if (not HasSkinCluster(selected[-1])):
		return

	for item in selected:
		if (item == selected[-1]):
			break
		if (not HasSkinCluster(item)):
			continue
		
		cmds.select(selected[-1], item)
		cmds.CopySkinWeights(surfaceAssociation = "closestPoint", influenceAssociation = "closestJoint", noMirror = True)
	
	cmds.select(selected)

def HasSkinCluster(targetObject):
	history = cmds.listHistory(targetObject)
	skinClusterDestination = cmds.ls(history, type = Enums.Types.skinCluster)
	if (len(skinClusterDestination) == 0):
		print("{0} doesn't have skinCluster".format(targetObject))
		return False
	else:
		return True

