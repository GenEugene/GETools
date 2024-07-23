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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds

from .. import Settings
from GETOOLS_SOURCE.values import Icons


def GetCurrentShelf():
	return cmds.shelfTabLayout("ShelfLayout", query = True, selectTab = True)

def AddToCurrentShelf(command="", label="label", labelImage="", image="pythonFamily.png", imageHighlight="pythonFamily.png", annotation=""):
	cmds.shelfButton(
		command = command,
		label = label,
		imageOverlayLabel = labelImage,
		annotation = annotation,
		image = image,
		highlightImage = imageHighlight,
		parent = GetCurrentShelf(),
		sourceType = "Python",
		)

def GetButtonFromShelf(buttonName):
	currentShelf = GetCurrentShelf()
	shelfButtons = cmds.shelfLayout(currentShelf, query = True, childArray = True)
	result = []
	for item in shelfButtons:
		if (cmds.objectTypeUI(item) == "shelfButton"):
			if (cmds.shelfButton(item, query = True, label = True) == buttonName):
				result.append(item)
	return None if (len(result) == 0) else result

def ToggleButtonIcons(path, *args):
	buttons = GetButtonFromShelf(Settings.buttonLabel)

	for item in buttons:
		currentImage = cmds.shelfButton(item, query = True, image = True)
		currentImageHighlight = cmds.shelfButton(item, query = True, highlightImage = True)

		count = len(Icons.get1)
		for i in range(count):
			if (path + Icons.get1[i] == currentImage):
				if (i + 1 < count):
					currentImage = path + Icons.get1[i + 1]
					currentImageHighlight = path + Icons.get2[i + 1]
				else:
					currentImage = path + Icons.get1[0]
					currentImageHighlight = path + Icons.get2[0]
				break

		cmds.shelfButton(item, edit = True, image = currentImage, highlightImage = currentImageHighlight)
	
