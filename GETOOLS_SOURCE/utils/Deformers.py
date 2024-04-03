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

import maya.cmds as cmds
# import maya.mel as mel

from ..utils import Selector
# from ..values import Enums


nameWrap = "wrapTemp"
dropoff = 4
smoothness = 0


def WrapsCreate(elements, *args):
	if (len(elements) < 2):
		cmds.warning("Need at least 2 objects for Wrap")
		return

	wrapsList = []
	sourceDuplicate = cmds.duplicate(elements[-1], name = elements[-1] + "Wrap")

	for i in range(len(elements)):
		if (i >= len(elements) - 1):
			break
		
		sourceTransform = elements[-1]
		sourceDuplicateShape = cmds.listRelatives(sourceDuplicate, shapes = True, noIntermediate = True)[0]
		sourceShape = cmds.listRelatives(elements[-1], shapes = True, noIntermediate = True)[0]
		targetShape = cmds.listRelatives(elements[i], shapes = True, noIntermediate = True)[0]

		# Create wrap node
		node = cmds.deformer(targetShape, name = nameWrap, type = "wrap")[0]
		wrapsList.append(node)

		# Set wrap parameters
		cmds.setAttr(node + ".falloffMode", 1)
		cmds.setAttr(node + ".autoWeightThreshold", 1)
		cmds.setAttr(node + ".dropoff[0]", dropoff)
		cmds.setAttr(node + ".smoothness[0]", smoothness)

		# Connect to other nodes
		cmds.connectAttr(sourceDuplicateShape + ".worldMesh[0]", node + ".basePoints[0]")
		cmds.connectAttr(sourceShape + ".worldMesh[0]", node + ".driverPoints[0]")
		cmds.connectAttr(sourceTransform + ".inflType", node + ".inflType[0]")

	return wrapsList, sourceDuplicate
def WrapsCreateOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return

	cmds.select(clear = True)
	wraps = WrapsCreate(selectedList)
	cmds.select(selectedList, replace = True)

	return selectedList, wraps[0], wraps[1]

def WrapsDelete(wrapsList, *args):
	for wrap in wrapsList:
		cmds.delete(wrap)

def BlendshapesProjecting(*args): # TODO
	result = WrapsCreateOnSelected()
	if (result == None):
		cmds.warning("No objects detected")
		return

	cmds.select(clear = True)

	# Map values
	selectedList = result[0]
	sourceMesh = selectedList[-1]
	wraps = result[1]
	sourceDuplicate = result[2]

	# Get blendshape node and weights
	shape = cmds.listRelatives(sourceMesh, shapes = True)[1] # weak solution, what if index is not always the same?
	blendshape = cmds.listConnections(shape, type = "blendShape")[0]
	weights = cmds.listAttr(blendshape + ".weight", multi = True)

	# Zero all weights
	for item in weights:
		cmds.setAttr(blendshape + "." + item, 0)
	
	# Activate one by one and duplicate results
	duplicatesList = []
	for i in range(len(selectedList) - 1):
		duplicates = []
		for item in weights:
			cmds.setAttr(blendshape + "." + item, 1)
			duplicate = cmds.duplicate(selectedList[i], name = item)
			duplicates.append(duplicate)
			cmds.setAttr(blendshape + "." + item, 0)
		duplicatesList.append(duplicates)
	
	# TODO create blendshape nodes to targets
	# TODO connect new blendshapes to targets
	
	WrapsDelete(wraps)
	cmds.delete(sourceDuplicate)

	cmds.select(selectedList, replace = True)

