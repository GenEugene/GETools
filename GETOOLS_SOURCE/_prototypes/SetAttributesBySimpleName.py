import maya.cmds as cmds

def FindAllObjects(objName):
	objects = cmds.ls(type = "transform", long = True)
	result = []
	for item in objects:
		if (item.endswith("|" + objName) or item.endswith(":" + objName)):
			result.append(item)
	return result

def SetAttributes(objectList):
	for item in objectList:
		cmds.setAttr(item + ".translateX", 0)
		cmds.setAttr(item + ".translateY", 0)
		cmds.setAttr(item + ".translateZ", 0)

def SetAttributesUnique(objectList):
	for item in objectList:
		cmds.setAttr(item + ".translateY", 0.5)

objNameL = "testL"
objNameR = "testR"
SetAttributes(FindAllObjects(objNameL))
SetAttributes(FindAllObjects(objNameR))
SetAttributesUnique(FindAllObjects(objNameR))