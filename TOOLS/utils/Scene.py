import maya.cmds as cmds

def Reload():
	currentScene = cmds.file(q = True, sceneName = True)
	if(currentScene):
		cmds.file(currentScene, open = True, force = True)
	else:
		cmds.file(new = 1, f = 1)

def Close():
	cmds.quit(force = True)