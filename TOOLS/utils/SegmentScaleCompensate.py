import maya.cmds as cmds

def SegmentScaleCompensate(value=0):
	jointList = cmds.ls(sl = 1, typ = "joint")
	
	for i in jointList:
		cmds.setAttr(i + ".segmentScaleCompensate", value)