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


	def RunSceneReload():
		import GETOOLS_SOURCE.utils.Scene as scene
		scene.Reload()
	

	runSceneReload = \
'''\
import GETOOLS_SOURCE.utils.Scene as scene
scene.Reload()\
'''
	
	runExitMaya = \
'''\
import GETOOLS_SOURCE.utils.Scene as scene
scene.ExitMaya()\
'''
	
	runSelectTransformHierarchy = \
'''\
import GETOOLS_SOURCE.utils.Selector as selector
selector.SelectTransformHierarchy()\
'''

	runBakeClassic = \
'''\
import GETOOLS_SOURCE.utils.Baker as baker
baker.BakeSelected\
'''

	runAnimOffset = \
'''\
import GETOOLS_SOURCE.utils.Animation as animation
animation.OffsetObjects\
'''
	
	runSetTimeline = \
'''\
import GETOOLS_SOURCE.utils.Timeline as timeline
timeline.SetTime\
'''
	
	runCopySkin = \
'''\
import GETOOLS_SOURCE.utils.Skinning as skinning
skinning.CopySkinWeightsFromLastMesh()\
'''
	
	runMotionTrailCreate = \
'''\
import GETOOLS_SOURCE.utils.MotionTrail as mtrail
mtrail.Create()\
'''
	
	runMotionTrailSelect = \
'''\
import GETOOLS_SOURCE.utils.MotionTrail as mtrail
mtrail.Select()\
'''
	
	runMotionTrailDelete = \
'''\
import GETOOLS_SOURCE.utils.MotionTrail as mtrail
mtrail.Delete()\
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


# FILE
def ToShelf_ReloadScene(path, *args):
	MoveToShelf(path, Presets.runSceneReload, "SceneReload", "Reload")
def ToShelf_ExitMaya(path, *args):
	MoveToShelf(path, Presets.runExitMaya, "ExitMaya", "Exit")

# UTILS
def ToShelf_SelectHierarchy(path, *args):
	MoveToShelf(path, Presets.runSelectTransformHierarchy, "SelectHierarchy", "SelHi")

# BAKING
def ToShelf_BakeClassic(path, *args):
	MoveToShelf(path, Presets.runBakeClassic + "(classic = True, preserveOutsideKeys = True)", "BakeClassic", "Bake")
def ToShelf_BakeClassicCutOut(path, *args):
	MoveToShelf(path, Presets.runBakeClassic + "(classic = True, preserveOutsideKeys = False)", "BakeClassicCutOut", "BakeCut")

# ANIMATION
def ToShelf_AnimOffsetMinus3(path, *args):
	MoveToShelf(path, Presets.runAnimOffset + "(-1, 3)", "AnimOffsetMinus3", "AOm3")
def ToShelf_AnimOffsetMinus2(path, *args):
	MoveToShelf(path, Presets.runAnimOffset + "(-1, 2)", "AnimOffsetMinus2", "AOm2")
def ToShelf_AnimOffsetMinus1(path, *args):
	MoveToShelf(path, Presets.runAnimOffset + "(-1, 1)", "AnimOffsetMinus1", "AOm1")
def ToShelf_AnimOffsetPlus1(path, *args):
	MoveToShelf(path, Presets.runAnimOffset + "(1, 1)", "AnimOffsetPlus1", "AOp1")
def ToShelf_AnimOffsetPlus2(path, *args):
	MoveToShelf(path, Presets.runAnimOffset + "(1, 2)", "AnimOffsetPlus2", "AOp2")
def ToShelf_AnimOffsetPlus3(path, *args):
	MoveToShelf(path, Presets.runAnimOffset + "(1, 3)", "AnimOffsetPlus3", "AOp3")

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

# RIGGING
def ToShelf_CopySkin(path, *args):
	MoveToShelf(path, Presets.runCopySkin, "CopySkin", "CopySkin")

# MOTION TRAIL
def ToShelf_MotionTrailCreate(path, *args):
	MoveToShelf(path, Presets.runMotionTrailCreate, "MotionTrailCreate", "MTCreate")
def ToShelf_MotionTrailSelect(path, *args):
	MoveToShelf(path, Presets.runMotionTrailSelect, "MotionTrailSelect", "MTSelect")
def ToShelf_MotionTrailDelete(path, *args):
	MoveToShelf(path, Presets.runMotionTrailDelete, "MotionTrailDelete", "MTDelete")

