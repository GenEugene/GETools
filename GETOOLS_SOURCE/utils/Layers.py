# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

# from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import Text


LayerBase = "BaseAnimation"
LayerPrefix = "_layer_"


def LayerCreate(layerName, parent = LayerBase, *args):
	# if(cmds.objExists(layerName)):
	# 	cmds.warning("Layer \"{0}\" already exists".format(layerName))
	# 	return None
	# else:
	# 	return cmds.animLayer(layerName, override = True, parent = parent)

	layer = cmds.animLayer(layerName, override = True, parent = parent)
	print("Layer \"{0}\" created".format(layer))
	return layer

def LayerCreateForSelected(selected, parent = LayerBase, prefix = LayerPrefix, *args):
	layers = []
	for item in selected:
		layerName = prefix + Text.ConvertSymbols(item) + "_1"
		layers.append(LayerCreate(layerName, parent))
	print("{0} Layers created: {1}".format(len(layers), layers))
	return layers

def LayerDelete(layerName, *args):
	if(cmds.objExists(layerName)):
		cmds.delete(layerName)
		print("Layer \"{0}\" deleted".format(layerName))
	else:
		cmds.warning("Layer \"{0}\" doesn't exist".format(layerName))


# def LayerMoveToSafeOrTemp(self, safeLayer = True, *args): # TODO rework
# 	_id = [0, 1]
# 	if (not safeLayer): _id = [1, 0]
# 	_layer1 = OverlappySettings.nameLayers[_id[0]]
# 	_layer2 = OverlappySettings.nameLayers[_id[1]]

# 	# Check source layer
# 	if(not cmds.objExists(_layer1)):
# 		cmds.warning("Layer \"{0}\" doesn't exist".format(_layer1))
# 		return
	
# 	# Get selected layers
# 	_selectedLayers = []
# 	for animLayer in cmds.ls(type = "animLayer"):
# 		if cmds.animLayer(animLayer, query = True, selected = True):
# 			_selectedLayers.append(animLayer)
	
# 	# Check selected count
# 	_children = cmds.animLayer(self.layers[_id[0]], query = True, children = True)
# 	_filteredLayers = []
# 	if (len(_selectedLayers) == 0):
# 		if (_children == None):
# 			cmds.warning("Layer \"{0}\" is empty".format(_layer1))
# 			return
# 		else:
# 			for layer in _children:
# 				_filteredLayers.append(layer)
# 	else:
# 		if (_children == None):
# 			cmds.warning("Layer \"{0}\" is empty".format(_layer1))
# 			return
# 		else:
# 			for layer1 in _children:
# 				for layer2 in _selectedLayers:
# 					if (layer1 == layer2):
# 						_filteredLayers.append(layer1)
# 		if (len(_filteredLayers) == 0):
# 			cmds.warning("Nothing to move")
# 			return
	
# 	# Create safe layer
# 	if(not cmds.objExists(_layer2)):
# 		self.layers[_id[1]] = cmds.animLayer(_layer2, override = True)
	
# 	# Move children or selected layers
# 	for layer in _filteredLayers:
# 		cmds.animLayer(layer, edit = True, parent = self.layers[_id[1]])
	
# 	# Delete TEMP layer if no children
# 	if (len(_filteredLayers) == len(_children)):
# 		self._LayerDelete(_layer1)

# def LayerCreate_TEST(self, *args): # TODO rework
# 	# Check selected
# 	_selected = cmds.ls(selection = True)
# 	if (len(_selected) == 0):
# 		cmds.warning("You must select at least 1 object")
# 		return
	
# 	# Create main layer
# 	if(not cmds.objExists(OverlappySettings.nameLayers[0])):
# 		self.layers[0] = cmds.animLayer(OverlappySettings.nameLayers[0], override = True)
	
# 	# Create layers on selected
# 	for item in _selected:
# 		_name = OverlappySettings.nameLayers[2] + Text.ConvertSymbols(item) + "_1"
# 		cmds.animLayer(_name, override = True, parent = self.layers[0])

