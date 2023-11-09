# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

def MultipleObjects(minimalCount = 1):
	# Save selected objects to variable
	selectedList = cmds.ls(selection = True)

	# Check selected objects
	if (len(selectedList) < minimalCount):
		if (minimalCount == 1):
			ending = ""
		else:
			ending = "s"
		cmds.warning("You need to select at least {0} object{1} !!!".format(minimalCount, ending))
		return None
	else:
		return selectedList

def SelectTransformHierarchy():
	cmds.select(hierarchy = True)
	list = cmds.ls(selection = True, type = "transform", shapes = False)
	cmds.select(clear = True)
	for i in range(len(list)):
		cmds.select(list[i], add = True)