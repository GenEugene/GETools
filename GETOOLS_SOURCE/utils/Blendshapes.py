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


def GetBlendshapeNodesFromList(selectedList):
	if (selectedList == None):
		return None
	
	result = []

	# Get blendshape nodes
	for element in selectedList:
		relatives = cmds.listRelatives(element)
		blendshapes = []

		for relative in relatives:
			connections = cmds.listConnections(relative, type = "blendShape")
			if (connections == None):
				continue

			for connection in connections:
				if connection not in blendshapes:
					blendshapes.append(connection)

		result.append(blendshapes)
	
	# Print result
	print("\tBLENDSHAPES")#
	for item in result:
		if (len(item) == 0):
			continue
		print(item[0])#
	
	return result
def GetBlendshapeNodesFromSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return None

	return GetBlendshapeNodesFromList(selectedList)

def GetBlendshapeWeights(blendshape):
	# Check blendshape node
	if (blendshape == None or len(blendshape) == 0):
		return None
	
	#  Get blendshape weights
	blendshapeNode = blendshape[0]
	weights = cmds.listAttr(blendshapeNode + ".weight", multi = True)

	result = []

	# Print result
	print("\tBLENDSHAPE \"{0}\" WEIGHTS".format(blendshape[0]))#
	for weight in weights:
		result.append(blendshapeNode + "." + weight)
		print(result[-1])#
	
	return result
def GetBlendshapeWeightsFromSelected(*args):
	blendshapes = GetBlendshapeNodesFromSelected()
	if (blendshapes == None):
		return None

	result = []

	for blendshape in blendshapes:
		result.append(GetBlendshapeWeights(blendshape))
	
	return result

def ZeroBlendshapeWeights(weights):
	for weight in weights:
		cmds.setAttr(weight, 0)
def ZeroBlendshapeWeightsOnSelected(*args):
	weights = GetBlendshapeWeightsFromSelected()
	if (weights == None):
		return
	
	for item in weights:
		if (item == None):
			continue
		ZeroBlendshapeWeights(item)

