import maya.cmds as cmds

def RotateOrderVisibility(on=True, *args):
	selected = cmds.ls(sl=1, l=1)
	for i in range(len(selected)):
		cmds.setAttr(selected[i] + ".rotateOrder", cb = on)