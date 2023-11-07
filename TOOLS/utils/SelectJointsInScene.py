import maya.cmds as cmds

def SelectJointsInScene():
	selectedJ = cmds.ls(typ = "joint")
	cmds.select(selectedJ)