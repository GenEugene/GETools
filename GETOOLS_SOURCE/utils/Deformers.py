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
# import maya.mel as mel

from ..utils import Selector
from ..values import Enums


NameWrap = "wrapTemp"


def WrapsCreate(elements, *args):
	wrapList = []

	for i in range(len(elements)):
		if (i >= len(elements) - 1):
			break
		
		targetShape = elements[i] + Enums.Types.shape
		sourceShape = elements[-1] + Enums.Types.shape
		sourceTransform = elements[-1]

		# Create wrap node and connect
		node = cmds.deformer(targetShape, name = NameWrap, type = "wrap")
		wrapList.append(node)
		cmds.connectAttr(NameWrap + ".input[0].inputGeometry", NameWrap + ".basePoints[0]")
		cmds.connectAttr(sourceShape + ".worldMesh[0]", NameWrap + ".driverPoints[0]")
		cmds.connectAttr(sourceTransform + ".inflType", NameWrap + ".inflType[0]")

	return wrapList
def WrapsCreateOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return

	cmds.select(clear = True)
	wraps = WrapsCreate(selectedList)
	cmds.select(selectedList, replace = True)

	return selectedList, wraps

def WrapsDelete(wrapList, *args):
	for item in wrapList:
		cmds.disconnectAttr(item + ".input[0].inputGeometry", item + ".basePoints[0]")
		cmds.delete(item)

def BlendshapesWrapMigrate(*args): # TODO
	result = WrapsCreateOnSelected()
	if (result == None):
		cmds.warning("No objects detected")
		return

	selectedList = result[0]
	wraps = result[1]

	# TODO get original blendshape node
	#blendshape = selectedList[-1]
	# TODO get blenshaoe weights names
	#weights = cmds.listAttr(blendshape + ".weight", multi = True)

	# TODO set blendshape to 1
	# TODO duplicate mesh
	# TODO set blendshape to 0
	# TODO repeat
	# for item in selectedList:
		# print(len(weights))
		# for i in range(len(weights)):
		# 	weights[i]
		# 	pass
	
	# TODO connect new blendshapes to targets
	
	# TODO delete temporary wraps
	# WrapsDelete(wraps)
	pass

