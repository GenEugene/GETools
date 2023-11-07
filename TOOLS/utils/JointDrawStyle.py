import maya.cmds as cmds

def JointDrawStyle(mode=0):
	selected = cmds.ls(sl = 1)
	
	for i in range(len(selected)):
		cmds.setAttr(selected[i] + ".drawStyle", mode)