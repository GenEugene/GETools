# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

def HelpPopupActivate(*args): # turn on help popups to show descriptions when buttons hovered by mouse
	cmds.help(popupMode = True)

def CachedPlaybackDeactivate(*args):
	if (cmds.evaluator(query = True, name = "cache")):
		cmds.evaluator(name = "cache", enable = False)
		cmds.warning("GETools: Cached Playback turned off")

