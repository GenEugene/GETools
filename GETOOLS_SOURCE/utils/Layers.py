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

from ..utils import Text

LayerBase = "BaseAnimation"
LayerPrefix = "_layer_"

def Create(layerName, parent=LayerBase, *args):
	# if(cmds.objExists(layerName)):
	# 	cmds.warning("Layer \"{0}\" already exists".format(layerName))
	# 	return None
	# else:
	# 	return cmds.animLayer(layerName, override = True, parent = parent)

	layer = cmds.animLayer(layerName, override = True, parent = parent)
	print("Layer \"{0}\" created".format(layer))
	return layer

def CreateForSelected(selected, parent=LayerBase, prefix=LayerPrefix, *args):
	layers = []
	for item in selected:
		layerName = prefix + Text.ConvertSymbols(item) + "_1"
		layers.append(Create(layerName, parent))
	print("{0} Layers created: {1}".format(len(layers), layers))
	return layers

def Delete(layerName, *args):
	if(cmds.objExists(layerName)):
		cmds.delete(layerName)
		print("Layer \"{0}\" deleted".format(layerName))
	else:
		cmds.warning("Layer \"{0}\" doesn't exist".format(layerName))

def MoveChildrenToParent(children, parent): # TODO rework *args
	# Check child layer
	# if(not cmds.objExists(layerChild)):
	# 	cmds.warning("Layer \"{0}\" doesn't exist".format(layerChild))
	# 	return
	# # Check parent layer
	# if(not cmds.objExists(layerParent)):
	# 	cmds.warning("Layer \"{0}\" doesn't exist".format(layerParent))
	# 	return
	
	# Move children or selected layers
	for layer in children:
		cmds.animLayer(layer, edit = True, parent = parent)
	
	# Delete TEMP layer if no children
	# if (len(filteredLayers) == len(_children)):
	# 	self._LayerDelete(_layer1)
	pass

def GetSelected(): # *args
	animLayers = cmds.ls(type = "animLayer")
	if (animLayers == None):
		return None
	
	selectedLayers = []
	for animLayer in animLayers:
		if cmds.animLayer(animLayer, query = True, selected = True):
			selectedLayers.append(animLayer)
	
	print("*****")
	print(selectedLayers)
	return selectedLayers

