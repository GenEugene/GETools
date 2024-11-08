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

from ..utils import Selector
from ..values import Enums


def FilterAttributesAnimatable(attributes, skipLockedKeys=True, skipNonKeyableKeys=True, skipHiddenKeys=True, skipMutedKeys=False, skipConstrainedKeys=True):
	if (attributes == None):
		cmds.warning("No attributes provided")
		return None
	
	attributesFiltered = []
	
	for attribute in attributes:
		# Check and skip muted keys
		if (skipMutedKeys):
			keyed = cmds.keyframe(attribute, query = True)
			if (keyed):
				muted = cmds.mute(attribute, query = True)
				if (muted):
					continue
		
		# Check attribute if locked, if keyable, if settable
		locked = cmds.getAttr(attribute, lock = True)
		keyable = cmds.getAttr(attribute, keyable = True)
		settable = cmds.getAttr(attribute, settable = True)
		
		# Check attribute if constrained
		connections = cmds.listConnections(attribute)
		constrained = False
		if (connections):
			for connection in connections:
				connectionType = cmds.nodeType(connection)
				if (connectionType in Enums.Constraints.list):
					constrained = True
		
		# General check and filling final list
		if (skipLockedKeys and locked or
	  		skipNonKeyableKeys and not keyable or
			skipHiddenKeys and not settable or
			skipConstrainedKeys and constrained):
			continue
		attributesFiltered.append(attribute)

	if (len(attributesFiltered) == 0):
		cmds.warning("No attributes left after filtering")
		return None

	return attributesFiltered

def FilterAttributesWithoutAnimation(attributes):
	attributesWithoutAnimation = []

	for attribute in attributes:
		connection = cmds.listConnections(attribute, source = True, destination = False, type = "animCurve")
		if (connection == None):
			attributesWithoutAnimation.append(attribute)
	
	if (len(attributesWithoutAnimation) == 0):
		return None
	
	return attributesWithoutAnimation

def GetAttributesAnimatableOnSelected(useShapes=False): # TODO fix shapes detection, check on curves, cameras, meshes
	# Check selected objects
	selectedList = Selector.MultipleObjects(minimalCount = 1, transformsOnly = False)
	if (selectedList == None):
		return None
	
	# Add shapes to the end of the selected objects list
	if (useShapes):
		shapesList = []
		for selected in selectedList:
			relatives = cmds.listRelatives(selected)
			for relative in relatives:
				shapesList.append(relative)
		selectedList.extend(shapesList)

	finalAttributesList = []

	# Iterate for each selected object
	for selected in selectedList:	
		# Get keyable attributes
		attributes = cmds.listAttr(selected, keyable = True)
		if (attributes == None):
			return None
		
		# Add object name before attribute name
		attributesFull = []
		for i in range(len(attributes)):
			attributesFull.append(selected + "." + attributes[i])

		# Check filtered attributes and add to final list
		attributesFullFiltered = FilterAttributesAnimatable(attributes = attributesFull)
		if (attributesFullFiltered != None):
			for attribute in attributesFullFiltered:
				finalAttributesList.append(attribute)
	
	return finalAttributesList

def GetAttributesSelectedFromChannelBox(*args):
	attributes = cmds.channelBox("mainChannelBox", query = True, selectedMainAttributes = True) # selectedShapeAttributes = True
	return attributes

