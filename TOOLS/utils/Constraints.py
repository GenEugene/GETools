import maya.cmds as cmds
from utils import Selector

def ConstrainSelectedToLastObject(reverse=False, maintainOffset=True, parent=True, point=False, orient=False, scale=False, weight=1):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	ConstrainListToLastElement(reverse, selectedList, maintainOffset, parent, point, orient, scale, weight)

def ConstrainListToLastElement(reverse=False, selectedList=None, maintainOffset=True, parent=True, point=False, orient=False, scale=False, weight=1):
	if (selectedList == None):
		cmds.warning("### WARNING ### selectedList = None")
		return
	
	for i in range(len(selectedList)):
		if (i == len(selectedList) - 1):
			break
		
		if (reverse):
			index1 = i
			index2 = -1
		else:
			index1 = -1
			index2 = i
		
		ConstrainSecondToFirstObject(selectedList[index1], selectedList[index2], maintainOffset, parent, point, orient, scale, weight = weight)

def ConstrainSecondToFirstObject(objectParent, objectChild, maintainOffset=True, parent=True, point=False, orient=False, scale=False, weight=1):
	if parent:
		try: cmds.parentConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight)
		except: print("||||| Can't create parentConstraint on {0}".format(objectChild))
	
	else:
		if point:
			try: cmds.pointConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight)
			except: print("||||| Can't create pointConstraint on {0}".format(objectChild))
		
		if orient:
			try: cmds.orientConstraint(objectParent, objectChild, maintainOffset = maintainOffset, weight = weight)
			except: print("||||| Can't create orientConstraint on {0}".format(objectChild))

	if scale:
		try:
			# cmds.cutKey(objectChild, attribute = ("scaleX", "scaleY", "scaleZ"), clear = True, option = "keys")
			cmds.scaleConstraint(objectParent, objectChild, maintainOffset = maintainOffset) # weight = weight
		except: print("||||| Can't create scaleConstraint on {0}".format(objectChild))



