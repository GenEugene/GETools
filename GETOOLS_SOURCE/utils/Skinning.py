# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Selector

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
	skinClusterDestination = cmds.ls(cmds.listHistory(targetObject), type = "skinCluster")
	if (len(skinClusterDestination) == 0):
		print("{0} doesn't have skinCluster".format(targetObject))
		return False
	else:
		return True