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

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene https://discord.gg/heMxJhTqCz
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds

from ..utils import Selector


def ParentShape(*args): # TODO improve logic
	# Check selected objects
	selected = Selector.MultipleObjects(minimalCount = 2, transformsOnly = False)
	if (selected == None):
		return
	cmds.parent(relative = True, shape = True)

def FirstToSecond(child, parent, maintainOffset=True):
	cmds.parent(child, parent)
	if (not maintainOffset):
		cmds.matchTransform(child, parent, position = True, rotation = True)
	
def SelectedToLastObject(): # TODO check if redundant
	# Check selected objects
	selected = Selector.MultipleObjects(2)
	if (selected == None):
		return
	ListToLastObjects(selected)

def ListToLastObjects(selected, maintainOffset=True, reverse=False):
	for i in range(len(selected)):
		if (i == len(selected) - 1):
			break
		
		if (reverse):
			index1 = -1
			index2 = i
		else:
			index1 = i
			index2 = -1
		
		FirstToSecond(selected[index1], selected[index2], maintainOffset)

