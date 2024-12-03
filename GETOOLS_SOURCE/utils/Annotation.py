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

from ..utils import Parent
from ..utils import Text


_prefix = "ann_"


def Annotate(target, text, point=(0, 0, 0), displayArrow=True, useNameAsText=False, freeze=True):
	textFinal = target if useNameAsText else text
	annotation = cmds.annotate(target, text = textFinal, point = point)
	cmds.setAttr(annotation + ".displayArrow", displayArrow)
	if (freeze):
		cmds.setAttr(annotation + ".overrideEnabled", 1)
		cmds.setAttr(annotation + ".overrideDisplayType", 2)
	return annotation

def AnnotateSelected(*args): # TODO add constraint logic and group all annotations together
	selected = cmds.ls(selection = True)
	for item in selected:
		# Create annotation and get transform
		annotation = Annotate(item, item, (0, 0, 0), displayArrow = False, useNameAsText = True)
		transform = cmds.listRelatives(annotation, allParents = True)[0]

		# Rename
		nameFinal = _prefix + item
		nameFinal = Text.ConvertSymbols(nameFinal)
		transform = cmds.rename(transform, nameFinal)

		# Parent
		Parent.FirstToSecond(transform, item, maintainOffset = False)

