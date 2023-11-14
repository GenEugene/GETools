# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from utils import Selector

def FirstToSecond(child, parent, maintainOffset = True):
	cmds.parent(child, parent)
	if (not maintainOffset):
		cmds.matchTransform(child, parent, position = True, rotation = True)
	
def SelectedToLastObject():
	# Check selected objects
	selected = Selector.MultipleObjects(2)
	if (selected == None):
		return
	ListToLastObjects(selected)

def ListToLastObjects(selected, maintainOffset = True, reverse = False):
	for i in range(len(selected)):
		if (i == len(selected) - 1):
			break
		
		if (reverse):
			index1 = -1
			index2 = i
		else:
			index1 = i
			index2 = -1
		
		FirstToSecond(selected[index1], selected[index2], maintainOffset)