import maya.cmds as cmds
from utils import Selector

def FirstToSecond(child, parent, maintainOffset = True):
	cmds.parent(child, parent)
	if (not maintainOffset):
		cmds.matchTransform(child, parent, position = True, rotation = True)
	
def SelectedToLastObject():
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	ListToLastObjects(selectedList)

def ListToLastObjects(selectedList, maintainOffset = True, reverse = False):
	for i in range(len(selectedList)):
		if (i == len(selectedList) - 1):
			break
		
		if (reverse):
			index1 = -1
			index2 = i
		else:
			index1 = i
			index2 = -1
		
		FirstToSecond(selectedList[index1], selectedList[index2], maintainOffset)