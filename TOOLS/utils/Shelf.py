import maya.cmds as cmds

def GetCurrentShelf():
	return cmds.shelfTabLayout("ShelfLayout", query = True, selectTab = True)

def AddToShelf(function="", imagePath="pythonFamily.png", annotation=""):
	currentShelf = GetCurrentShelf()
	cmds.shelfButton(parent = currentShelf, command = function, image = imagePath, annotation = annotation)