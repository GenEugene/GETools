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


def FilterAttributesAnimatable(attributes, checkMutedKeys=False):
	if (attributes == None):
		cmds.warning("No attributes provided")
		return None
	
	attributesFiltered = []
	
	for item in attributes:
		# Check muted keys
		if (checkMutedKeys):
			keyed = cmds.keyframe(item, query = True)
			if (keyed):
				muted = cmds.mute(item, query = True)
				if (muted):
					continue
		
		# Check attribute if locked, if keyable, if settable
		locked = cmds.getAttr(item, lock = True)
		keyable = cmds.getAttr(item, keyable = True)
		settable = cmds.getAttr(item, settable = True)
		
		# Check attribute if constrained
		connections = cmds.listConnections(item)
		constrained = False
		if (connections):
			for item in connections:
				type = cmds.nodeType(item)
				if (type in Enums.Constraints.list):
					constrained = True
		
		# General check and filling final list
		if (not locked and keyable and settable and not constrained):
			attributesFiltered.append(item)
	
	if (len(attributesFiltered) == 0):
		cmds.warning("No attributes left after filtering")
		return None

	return attributesFiltered

def GetAttributesAnimatableOnSelected(*args):
	# Check selected objects
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return None

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
		attributesFullFiltered = FilterAttributesAnimatable(attributesFull)
		if (attributesFullFiltered != None):
			for attribute in attributesFullFiltered:
				finalAttributesList.append(attribute)
	
	return finalAttributesList

def GetAttributesSelectedFromChannelBox(*args):
	attributes = cmds.channelBox("mainChannelBox", query = True, selectedMainAttributes = True) # selectedHistoryAttributes # selectedMainAttributes # selectedOutputAttributes # selectedShapeAttributes
	return attributes

