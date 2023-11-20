# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

def GetCurrentShelf():
	return cmds.shelfTabLayout("ShelfLayout", query = True, selectTab = True)

def AddToCurrentShelf(command = "", label = "label", imagePath = "pythonFamily.png", annotation = "description"):
	cmds.shelfButton(
		command = command,
		label = label,
		annotation = annotation,
		image = imagePath,
		parent = GetCurrentShelf(),
		sourceType = "Python",
		)