import maya.cmds as cmds

def LayerCreate(self, obj, *args):
	
	# Create main layer
	if(not cmds.objExists(OVLP.nameLayers[0])):
		self.layers[0] = cmds.animLayer(OVLP.nameLayers[0], override = True)
	
	# Create layers on selected
	_name = OVLP.nameLayers[2] + self.ConvertText(obj) + "_1"
	return cmds.animLayer(_name, override = True, parent = self.layers[0])

def LayerDelete(self, name, *args):
	if(cmds.objExists(name)):
		cmds.delete(name)
		print("Layer '{0}' deleted".format(name))
	else:
		cmds.warning("Layer '{0}' doesn't exist".format(name))

def LayerMoveToSafeOrBase(self, safeLayer=True, *args):
	_id = [0, 1]
	if (not safeLayer): _id = [1, 0]
	_layer1 = OVLP.nameLayers[_id[0]]
	_layer2 = OVLP.nameLayers[_id[1]]

	# Check source layer
	if(not c.objExists(_layer1)):
		c.warning("Layer '{0}' doesn't exist".format(_layer1))
		return
	# Get selected layers
	_selectedLayers = []
	for animLayer in c.ls(type = "animLayer"):
		if c.animLayer(animLayer, query = True, selected = True):
			_selectedLayers.append(animLayer)
	# Check selected count
	_children = c.animLayer(self.layers[_id[0]], query = True, children = True)
	_filteredLayers = []
	if (len(_selectedLayers) == 0):
		if (_children == None):
			c.warning("Layer '{0}' is empty".format(_layer1))
			return
		else:
			for layer in _children:
				_filteredLayers.append(layer)
	else:
		if (_children == None):
			c.warning("Layer '{0}' is empty".format(_layer1))
			return
		else:
			for layer1 in _children:
				for layer2 in _selectedLayers:
					if (layer1 == layer2):
						_filteredLayers.append(layer1)
		if (len(_filteredLayers) == 0):
			c.warning("Nothing to move")
			return
	# Create safe layer
	if(not c.objExists(_layer2)):
		self.layers[_id[1]] = c.animLayer(_layer2, override = True)
	# Move children or selected layers
	for layer in _filteredLayers:
		c.animLayer(layer, edit = True, parent = self.layers[_id[1]])
	# Delete base layer if no children
	if (len(_filteredLayers) == len(_children)):
		self._LayerDelete(_layer1)