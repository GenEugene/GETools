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

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds
# import maya.mel as mel

from ..utils import Selector


def GetBlendshapeNodeFromMesh(mesh):
	if (mesh == None):
		return None
	
	blendshape = ""

	# Get blendshape nodes
	relatives = cmds.listRelatives(mesh)
	blendshapes = []

	for relative in relatives:
		connections = cmds.listConnections(relative, type = "blendShape")
		if (connections == None):
			continue

		for connection in connections:
			if connection not in blendshapes:
				blendshape = connection
				blendshapes.append(connection)
				
	if (len(blendshape) == 0):
		return None
	
	print(blendshape)#
	return blendshape
def GetBlendshapeNodesFromMeshes(meshList):
	if (meshList == None):
		return None
	
	blendshapes = []

	# Get blendshape nodes
	print("\tBLENDSHAPES")#
	for mesh in meshList:
		blendshapes.append(GetBlendshapeNodeFromMesh(mesh))
	
	return blendshapes
def GetBlendshapeNodesFromSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return None

	return GetBlendshapeNodesFromMeshes(selectedList)

def GetBlendshapeWeights(blendshape):
	# Check blendshape node
	if (blendshape == None or len(blendshape) == 0):
		return None
	
	#  Get blendshape weights
	weightsNames = cmds.listAttr(blendshape + ".weight", multi = True)
	weightsNamesFull = []

	# Print result
	print("\tBLENDSHAPE \"{0}\" WEIGHTS".format(blendshape))#
	for weight in weightsNames:
		weightsNamesFull.append(blendshape + "." + weight)
		print(weightsNamesFull[-1])#
	
	return weightsNamesFull, weightsNames
def GetBlendshapeWeightsFromSelected(*args):
	blendshapes = GetBlendshapeNodesFromSelected()
	if (blendshapes == None):
		return None

	weightsNamesFull = []
	weightsNames = []

	for blendshape in blendshapes:
		weightsRaw = GetBlendshapeWeights(blendshape)
		if (weightsRaw == None):
			continue
		weightsNamesFull.append(weightsRaw[0])
		weightsNames.append(weightsRaw[1])
	
	return weightsNamesFull, weightsNames

def ZeroBlendshapeWeights(weights):
	for weight in weights:
		cmds.setAttr(weight, 0)
def ZeroBlendshapeWeightsOnSelected(*args):
	weights = GetBlendshapeWeightsFromSelected()
	if (weights == None):
		return
	
	for item in weights[0]:
		if (item == None):
			continue
		ZeroBlendshapeWeights(item)

def ExtractShapesFromBlendshape(blendshape):
	# Check blendshape node
	if (blendshape == None or len(blendshape) == 0):
		return None
	
	# Get blendshape weights and zero all of them
	weights = GetBlendshapeWeights(blendshape)
	ZeroBlendshapeWeights(weights[0])

	# Activate one by one and duplicate results
	originalMesh = cmds.listConnections(blendshape, type = "mesh", source = False, destination = True)
	duplicatedMeshes = []
	
	for i in range(len(weights[0])):
		cmds.setAttr(weights[0][i], 1)
		duplicate = cmds.duplicate(originalMesh, name = weights[1][i])
		duplicatedMeshes.append(duplicate)
		cmds.setAttr(weights[0][i], 0)

	return duplicatedMeshes
def ExtractShapesFromBlendshapes(blendshapes):
	if (blendshapes == None):
		return None

	meshes = []

	# Get blendshape nodes
	for blendshape in blendshapes:
		meshes.append(ExtractShapesFromBlendshape(blendshape))

	return meshes
def ExtractShapesFromSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return None
	
	blendshapes = GetBlendshapeNodesFromMeshes(selectedList)
	meshes = ExtractShapesFromBlendshapes(blendshapes)
	
	cmds.select(selectedList, replace = True)

	return meshes

