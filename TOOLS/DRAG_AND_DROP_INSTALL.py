# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.
# Drag and Drop for Maya 2023 (other versions not tested)

import os
import sys
import maya.cmds as cmds


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

import experimental.GeneralWindow as gtwindow
gtwindow.GeneralWindow().RUN()

import scripts.old_GETools as oldget
oldget.GETOOLS_class().Start()

import scripts.Tools as tls
tls.Tools().RUN()

import scripts.CenterOfMass as com
com.CenterOfMass().RUN()

""".format(path = scriptPath)


# Drag and Drop function with button creation on current shelf
def onMayaDroppedPythonFile(*args, **kwargs):
	currentShelf = cmds.shelfTabLayout("ShelfLayout", query = True, selectTab = True)
	cmds.shelfButton(
		command = buttonCommand,
		label = buttonLabel,
		annotation = "GenEugene Animation Tools",
		sourceType = 'Python',
		image = scriptPath + "\icons\GET.png",
		image1 = scriptPath + "\icons\GET.png",
		parent = currentShelf
	)