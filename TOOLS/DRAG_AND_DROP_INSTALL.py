# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.
# Drag and Drop for Maya 2023 (other versions not tested)

import os
import sys
import maya.cmds as cmds
from utils import Shelf
from utils import Icons


# Get script directory path
scriptPath = os.path.dirname(__file__)
scriptPath = scriptPath.replace("\\", "/")
if not os.path.exists(scriptPath):
	raise IOError(r'The source path {0} does not exist!'.format(scriptPath))
if scriptPath not in sys.path:
	sys.path.insert(0, scriptPath)


# Button settings
buttonLabel = "GETools"
buttonCommand = """
#########################################
### Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.
### GETools
### https://github.com/GenEugene/GETools
#########################################

import os
import sys
import maya.cmds as cmds

if not os.path.exists("{path}"):
	raise IOError(r"The source path {path} does not exist!")

if "{path}" not in sys.path:
	sys.path.insert(0, "{path}")

import modules.GeneralWindow as gtwindow
gtwindow.GeneralWindow().RUN()

# import modules.old_GETools as oldget
# oldget.GETOOLS_class().Start()

# import modules.Tools as tls
# tls.Tools().RUN()

# import modules.CenterOfMass as com
# com.CenterOfMass().RUN()

""".format(path = scriptPath)


# Drag and Drop function with button creation on current shelf
def onMayaDroppedPythonFile(*args, **kwargs):
	Shelf.AddToCurrentShelf(
		command = buttonCommand,
		label = buttonLabel,
		annotation = "GenEugene Animation Tools",
		imagePath = scriptPath + Icons.get,
	)

