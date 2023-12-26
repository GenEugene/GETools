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
	
	runSetTimeline = \
'''\
import GETOOLS_SOURCE.utils.Timeline as timeline
timeline.SetTime\
'''

	runBakeClassic = \
'''\
import GETOOLS_SOURCE.utils.Baker as baker
baker.BakeSelected\
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

def MoveToShelf(path, tool, label, labelImage, *args):
	command = GetFunctionStringForTool(path, tool)
	Shelf.AddToCurrentShelf(
		command = command,
		label = label,
		labelImage = labelImage
		)


# UTILS
def ToShelf_SelectHierarchy(path, *args):
	MoveToShelf(path, Presets.runSelectTransformHierarchy, "SelectHierarchy", "SelHi")

# BAKING
def ToShelf_BakeClassic(path, *args):
	MoveToShelf(path, Presets.runBakeClassic + "(classic = True, preserveOutsideKeys = True)", "BakeClassic", "Bake")
def ToShelf_BakeClassicCutOut(path, *args):
	MoveToShelf(path, Presets.runBakeClassic + "(classic = True, preserveOutsideKeys = False)", "BakeClassicCutOut", "BakeCut")

# TIMELINE
def ToShelf_SetTimelineMinOut(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(3)", "SetTimelineMinOut", "<<")
def ToShelf_SetTimelineMinIn(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(1)", "SetTimelineMinIn", "<-")
def ToShelf_SetTimelineMaxIn(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(2)", "SetTimelineMaxIn", "->")
def ToShelf_SetTimelineMaxOut(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(4)", "SetTimelineMaxOut", ">>")
def ToShelf_SetTimelineExpandOut(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(5)", "SetTimelineExpandOut", "<->")
def ToShelf_SetTimelineExpandIn(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(6)", "SetTimelineExpandIn", ">-<")
def ToShelf_SetTimelineSet(path, *args):
	MoveToShelf(path, Presets.runSetTimeline + "(7)", "SetTimelineSet", "|<->|")
