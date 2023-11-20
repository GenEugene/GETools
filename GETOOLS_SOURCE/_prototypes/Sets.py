import maya.cmds as cmds

def CreateSets():
	set0 = cmds.sets(n="SETS")
	setE0 = cmds.sets(n="SET_EXPORT")
	setE1 = cmds.sets(n="SET_EXPORT_ALL")
	setE2 = cmds.sets(n="SET_EXPORT_ANIM_ALL")
	
	cmds.sets(setE0, e = 1, fe = set0)  # Привязка SET_EXPORT к SETS
	cmds.sets(setE1, e = 1, fe = setE0) # Привязка SET_EXPORT_ALL к SET_EXPORT
	cmds.sets(setE2, e = 1, fe = setE0) # Привязка SET_EXPORT_ANIM_ALL к SET_EXPORT