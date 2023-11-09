### DEPRECATED ###
# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from utils import Icons
from utils import Shelf

def ToolsRun():
	from modules import Tools as EugeneMyTools
	EugeneMyTools.Tools().RUN()

def CenterOfMassRun():
	from modules import CenterOfMass as EugeneCenterOfMass
	EugeneCenterOfMass.CenterOfMass().RUN()

def OverlappyRun():
	# from modules import CenterOfMass as EugeneCenterOfMass
	# EugeneCenterOfMass.CenterOfMass().RUN()
	cmds.warning("Overlappy not supported yet...")


def ToolsAddToShelf(*args):
	Shelf.AddToCurrentShelf(
		function = """
from modules import Tools as EugeneTools # TODO add existing method and not string duplicate
EugeneTools.Tools().RUN()
		""",
		imagePath = Icons.tools,
		annotation = "Bunch of different tools for locator creation, constraining and baking")

def CenterOfMassAddToShelf(*args):
	Shelf.AddToCurrentShelf(
		function = """
from modules import CenterOfMass as EugeneCenterOfMass # TODO add existing method and not string duplicate
EugeneCenterOfMass.CenterOfMass().RUN()
		""",
		imagePath = Icons.centerOfMass,
		annotation = "Center Of Mass tools")

def OverlappyAddToShelf(*args): # TODO
	cmds.warning("Overlappy not supported yet...")
