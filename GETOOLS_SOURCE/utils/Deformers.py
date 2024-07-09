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

from ..utils import Blendshapes
from ..utils import Selector
# from ..values import Enums

nameWrap = "wrapTemp"
nameBlendshapePrefix = "bs_"
dropoff = 4
smoothness = 0

def WrapsCreateOnList(elements):
	if (len(elements) < 2):
		cmds.warning("Need at least 2 objects for Wrap")
		return

	wrapsList = []
	sourceDuplicate = cmds.duplicate(elements[-1], name = elements[-1] + "Wrap")

	for i in range(len(elements)):
		if (i >= len(elements) - 1):
			break
		
		# sourceTransform = elements[-1]
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
		cmds.setAttr(node + ".inflType[0]", 2)

		# Connect to other nodes
		cmds.connectAttr(sourceDuplicateShape + ".worldMesh[0]", node + ".basePoints[0]")
		cmds.connectAttr(sourceShape + ".worldMesh[0]", node + ".driverPoints[0]")
		# cmds.connectAttr(sourceTransform + ".inflType", node + ".inflType[0]")

	return wrapsList, sourceDuplicate
def WrapsCreateOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return

	cmds.select(clear = True)
	wraps = WrapsCreateOnList(selectedList)
	cmds.select(selectedList, replace = True)

	return selectedList, wraps[0], wraps[1]

def WrapConvertToBlendshapes(blendshape): # TODO create single conversion logic from Wrap to Blendshapes
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return

	# Get blendshape nodes
	relatives = cmds.listRelatives(selectedList[0])
	wraps = []

	for relative in relatives:
		connections = cmds.listConnections(relative, type = "wrap")
		if (connections == None):
			continue

		for connection in connections:
			if connection not in wraps:
				wraps.append(connection)
	
	print(wraps)
	
def WrapsConvertFromSelected(*args): # TODO
	pass

def WrapsDelete(wraps): # TODO move out from current script, looks like just a regular delete method
	for wrap in wraps:
		cmds.delete(wrap)

def BlendshapesReconstruction(*args): # TODO simplify function, split to smaller blocks
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	
	# Get blendshape node
	sourceMesh = selectedList[-1]
	blendshapeSource = Blendshapes.GetBlendshapeNodeFromModel(sourceMesh)
	
	# Check blendshape node
	if (blendshapeSource == None):
		cmds.warning("Last selected object has no blendShape node. Operation aborted")
		return

	# Create wraps
	result = WrapsCreateOnSelected()
	if (result == None):
		cmds.warning("No objects detected")
		return

	cmds.select(clear = True)

	# Map values
	wraps = result[1]
	sourceDuplicate = result[2]

	# Get blendshape weights and zero all of them
	weights = Blendshapes.GetBlendshapeWeights(blendshapeSource)
	Blendshapes.ZeroBlendshapeWeights(weights[0])

	# Activate one by one and duplicate results
	duplicatesList = []
	for i in range(len(selectedList) - 1):
		duplicates = []
		for y in range(len(weights[0])):
			cmds.setAttr(weights[0][y], 1)
			duplicate = cmds.duplicate(selectedList[i], name = weights[1][y])
			duplicates.append(duplicate)
			cmds.setAttr(weights[0][y], 0)
		duplicatesList.append(duplicates)

	# Wraps cleanup
	WrapsDelete(wraps)
	cmds.delete(sourceDuplicate)

	# Create blendshape nodes, add targets and delete duplicates
	for x in range(len(selectedList) - 1):
		blendshapeTarget = cmds.blendShape(selectedList[x], name = nameBlendshapePrefix + selectedList[x])
		for y in range(len(duplicatesList[x])):
			cmds.blendShape(blendshapeTarget, edit = True, target = (selectedList[x], y, duplicatesList[x][y][0], 1.0))
			cmds.delete(duplicatesList[x][y][0])
	
	cmds.select(selectedList, replace = True)

