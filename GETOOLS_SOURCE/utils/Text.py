# GETOOLS is under the terms of the MIT License

# Copyright (c) 2018-2024 Eugene Gataulin (GenEugene). All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene

import maya.cmds as cmds

def ConvertSymbols(text, direction=True):
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

def GetShortName(objectWithName, removeSpaces=False):
	result = objectWithName
	result = result.split(":")[-1]

	if (removeSpaces):
		result = result.replace("_", "")
	
	return result

