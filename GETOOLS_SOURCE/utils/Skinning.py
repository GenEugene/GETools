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

def GetSkinCluster(targetObject):
	history = cmds.listHistory(targetObject)
	skinClusterDestination = cmds.ls(history, type = Enums.Types.skinCluster)
	
	if (len(skinClusterDestination) == 0):
		print("{0} doesn't have skinCluster".format(targetObject))
		return None
	else:
		return skinClusterDestination

def HasSkinCluster(targetObject):
	skinCluster = GetSkinCluster(targetObject)
	if (skinCluster == None):
		print("{0} doesn't have skinCluster".format(targetObject))
		return False
	else:
		return True


def GetJointsSkinnedToMesh(mesh):
	cluster = GetSkinCluster(mesh)
	if (cluster == None):
		return None

	joints = cmds.listConnections(cluster[0] + ".matrix")
	if (joints == None):
		cmds.warning("No joints")
		return None

	for joint in joints:
		print(joint)
	
	return joints

def SelectSkinnedMeshesOrJoints(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return None
	
	if (cmds.nodeType(selectedList[0]) == Enums.Types.joint):
		resultClusters = []
		for selected in selectedList:
			clusters = cmds.listConnections(selected + ".worldMatrix")
			if (clusters == None):
				continue
			for cluster in clusters:
				if (cluster not in resultClusters):
					resultClusters.append(cluster)
		
		if (len(resultClusters)) == 0:
			cmds.warning("No clusters found")
			return None
		
		resultMeshes = []
		for cluster in resultClusters:
			meshes = cmds.listConnections(cluster, type = Enums.Types.mesh)
			if (meshes != None):
				for mesh in meshes:
					if (mesh not in resultMeshes):
						resultMeshes.append(mesh)

		print(resultMeshes)
		cmds.select(resultMeshes, replace = True)
	else:
		resultJoints = []
		for selected in selectedList:
			joints = GetJointsSkinnedToMesh(selected)
			if (joints != None):
				resultJoints.append(GetJointsSkinnedToMesh(selected))
		
		if (len(resultJoints)) == 0:
			cmds.warning("No joints found")
			return None
		
		resultJoints = resultJoints[0]
		cmds.select(resultJoints, replace = True)

