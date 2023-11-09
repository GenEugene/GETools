# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

def ConvertSymbols(text, direction = True):
	replaceSymbol1 = ("|", "_RS1_")
	replaceSymbol2 = (":", "_RS2_")

	if (direction):
		_text = text.replace(replaceSymbol1[0], replaceSymbol1[1])
		_text = _text.replace(replaceSymbol2[0], replaceSymbol2[1])
		return _text
	else:
		_text = text.replace(replaceSymbol1[1], replaceSymbol1[0])
		_text = _text.replace(replaceSymbol2[1], replaceSymbol2[0])
		return _text

def SetUniqueFromText(baseName):
	resultName = baseName
	counter = 0
	while (cmds.objExists(resultName)):
		resultName = baseName + str(counter + 1)
		counter += 1
	return resultName

def GetShortName(objectWithName, removeSpaces = False):
	result = objectWithName
	result = result.split(":")[-1]

	if (removeSpaces):
		result = result.replace("_", "")
	
	return result