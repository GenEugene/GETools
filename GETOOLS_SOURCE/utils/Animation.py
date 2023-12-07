# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
import maya.mel as mel

from GETOOLS_SOURCE.utils import Selector


def DeleteKeys(*args):
	if (Selector.MultipleObjects(1) == None):
		return
	cmds.cutKey()

def DeleteKeyRange(*args):
	mel.eval('timeSliderClearKey')

def KeysNonkeyableDelete(*args):
	selected = cmds.ls(selection = True)
	counter = 0
	for item in selected:
		attributes = cmds.listAttr(item, channelBox = 1)
		if attributes != None:
			for j in range(len(attributes)):
				cmds.cutKey(item + "." + attributes[j])
				counter += 1
	print ("\nNonkeyable attributes deleted: {0}".format(counter))


def SetInfinity(mode, items = None, *args):
	result = ""
	if (mode == 1):
		result = "constant"
	elif (mode == 2):
		result = "linear"
	elif (mode == 3):
		result = "cycle"
	elif (mode == 4):
		result = "cycleRelative"
	elif (mode == 5):
		result = "oscillate"
	if (items == None):
		cmds.setInfinity(preInfinite = result, postInfinite = result)
	else:
		cmds.setInfinity(items, preInfinite = result, postInfinite = result)
def SetInfinityConstant(selected):
	SetInfinity(mode = 1, items = selected)
def SetInfinityCycle(selected):
	SetInfinity(mode = 2, items = selected)

