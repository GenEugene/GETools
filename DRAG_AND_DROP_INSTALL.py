# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.
# Drag and Drop for Maya 2023

import os

from GETOOLS_SOURCE.utils import Icons
from GETOOLS_SOURCE.utils import Shelf
from GETOOLS_SOURCE.utils import Install


# Get script directory path
scriptPath = os.path.dirname(__file__)
scriptPath = scriptPath.replace("\\", "/")
Install.AddPathToEnvironment(scriptPath)


# Button settings
buttonLabel = "GETools"
functionAddPathToEnvironment = Install.GetFunctionString(scriptPath)
buttonCommand = \
"""\
#########################################
### Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.
### GETools
### https://github.com/GenEugene/GETools
#########################################

import os
import sys
import maya.cmds as cmds

{func}

import GETOOLS_SOURCE.modules.GeneralWindow as gtwindow
gtwindow.GeneralWindow().RUN_DOCKED(\"{path}\")\
""".format(func = functionAddPathToEnvironment, path = scriptPath)


# Drag and Drop function with button creation on current shelf
def onMayaDroppedPythonFile(*args, **kwargs):
	Shelf.AddToCurrentShelf(
		command = buttonCommand,
		label = buttonLabel,
		annotation = "GenEugene Animation Tools",
		imagePath = scriptPath + Icons.get,
		)

