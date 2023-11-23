# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Text


LayerBase = "BaseAnimation"
LayerPrefix = "_layer_"


def Create(layerName, parent = LayerBase, *args):
	# if(cmds.objExists(layerName)):
	# 	cmds.warning("Layer \"{0}\" already exists".format(layerName))
	# 	return None
	# else:
	# 	return cmds.animLayer(layerName, override = True, parent = parent)

	layer = cmds.animLayer(layerName, override = True, parent = parent)
	print("Layer \"{0}\" created".format(layer))
	return layer

def CreateForSelected(selected, parent = LayerBase, prefix = LayerPrefix, *args):
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

