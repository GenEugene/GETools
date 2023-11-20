# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

def MultipleObjects(minimalCount = 1, transformsOnly = True):
	# Save selected objects to variable
	if (transformsOnly):
		selectedList = cmds.ls(selection = True, type = "transform", shapes = False)
	else:
		selectedList = cmds.ls(selection = True, shapes = False)

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

def SelectTransformHierarchy(*args):
	selected = MultipleObjects()
	if (selected == None):
		return None

	cmds.select(hierarchy = True)
	list = cmds.ls(selection = True, type = "transform", shapes = False)
	cmds.select(clear = True)
	
	for i in range(len(list)):
		cmds.select(list[i], add = True)
	
	return list

def PrintSelected(*args):
	selected = MultipleObjects(transformsOnly = False)
	if (selected == None):
		return

	print("\t##### {0} items printed below:".format(len(selected)))
	for item in selected:
		print(item)
	print("\t#####")
	
