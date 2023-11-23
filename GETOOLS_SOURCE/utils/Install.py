# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import os
import sys

import GETOOLS_SOURCE.utils.Shelf as Shelf

class Presets:
	runGeneralWindow = \
'''\
import GETOOLS_SOURCE.modules.GeneralWindow as gtwindow
gtwindow.GeneralWindow().RUN_DOCKED()\
'''
	runSelectTransformHierarchy = \
'''\
import GETOOLS_SOURCE.utils.Selector as selector
selector.SelectTransformHierarchy()\
'''

def AddPathToEnvironment(path, *args):
	if not os.path.exists(path):
		raise IOError(r'The source path {0} does not exist!'.format(path))

	if path not in sys.path:
		sys.path.insert(0, path)

def GetFunctionString(path, *args):
	return \
"""\
if not os.path.exists("{path}"):
	raise IOError(r"The source path {path} does not exist!")

if "{path}" not in sys.path:
	sys.path.insert(0, "{path}")\
""".format(path = path)

def GetFunctionStringForTool(path, tool, *args):
	return \
"""\
import os
import sys

{path}

{tool}\
""".format(path = GetFunctionString(path), tool = tool)


# SAVE TO SHELF
def ToShelf_SelectHierarchy(path, *args):
	tool = Presets.runSelectTransformHierarchy

	command = GetFunctionStringForTool(path, tool)

	Shelf.AddToCurrentShelf(
		command = command,
		label = "SelectHierarchy",
		labelImage = "SelHier",
		)

