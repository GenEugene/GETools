# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

def Reload(*args):
	currentScene = cmds.file(query = True, sceneName = True)
	if(currentScene):
		cmds.file(currentScene, open = True, force = True)
	else:
		cmds.file(newFile = 1, force = 1)

def ExitMaya(*args):
	cmds.quit(force = True)