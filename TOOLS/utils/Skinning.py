import maya.cmds as cmds
from utils import Selector

def CopySkinWeightsFromLastMesh(minSelectedCount=2):
	# Check selected objects
	selectedList = Selector.MultipleObjects(minSelectedCount)
	if (selectedList == None):
		return
	if (not HasSkinCluster(selectedList[-1])):
		return

	for item in selectedList:
		if (item == selectedList[-1]):
			break
		if (not HasSkinCluster(item)):
			continue
		
		cmds.select(selectedList[-1], item)
		cmds.CopySkinWeights(surfaceAssociation = "closestPoint", influenceAssociation = "closestJoint", noMirror = True)
		# print("{0} copied to {1}".format(selectedList[-1], item))
	
	# Select objects and return
	cmds.select(selectedList)


def HasSkinCluster(targetObject):
	skinClusterDestination = cmds.ls(cmds.listHistory(targetObject), type = "skinCluster")
	if (len(skinClusterDestination) == 0):
		print("{0} doesn't have skinCluster".format(targetObject))
		return False
	else:
		return True