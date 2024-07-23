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

import os

from GETOOLS_SOURCE import Settings
from GETOOLS_SOURCE.utils import Install
from GETOOLS_SOURCE.utils import Shelf
from GETOOLS_SOURCE.values import CodeSamples
from GETOOLS_SOURCE.values import Icons
from GETOOLS_SOURCE.values import License


# Get script directory path
scriptPath = os.path.dirname(__file__)
scriptPath = scriptPath.replace("\\", "/")
Install.AddPathToEnvironment(scriptPath)

imports = """\
import os
import sys
import maya.cmds as cmds
"""

environment = Install.GetFunctionString(scriptPath)
code = Install.ReadFunctionAsString(CodeSamples.GeneralWindow)

# Generate code line by line
buttonCommand = ""
buttonCommand += License.text + "\n"
buttonCommand += imports + "\n"
buttonCommand += environment + "\n\n"
buttonCommand += code + "(\"{0}\")".format(scriptPath)

# Drag and Drop function with button creation on current shelf
def onMayaDroppedPythonFile(*args, **kwargs):
	Shelf.AddToCurrentShelf(
		command = buttonCommand,
		label = Settings.buttonLabel,
		annotation = "GenEugene Animation Tools",
		image = scriptPath + Icons.get1[0],
		imageHighlight = scriptPath + Icons.get2[0],
		)

