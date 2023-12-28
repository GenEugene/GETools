# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import os
import sys

import GETOOLS_SOURCE.utils.Shelf as Shelf

class Presets:
	pathGeneral =\
	"import GETOOLS_SOURCE.modules.GeneralWindow as gtwindow"
	pathScene =\
	"import GETOOLS_SOURCE.utils.Scene as scene"
	pathBaker =\
	"import GETOOLS_SOURCE.utils.Baker as baker"
	pathSelector =\
	"import GETOOLS_SOURCE.utils.Selector as selector"
	pathLocators =\
	"import GETOOLS_SOURCE.utils.Locators as locators"
	pathTimeline =\
	"import GETOOLS_SOURCE.utils.Timeline as timeline"
	pathAnimation =\
	"import GETOOLS_SOURCE.utils.Animation as animation"
	pathSkinning =\
	"import GETOOLS_SOURCE.utils.Skinning as skinning"
	pathMotionTrail =\
	"import GETOOLS_SOURCE.utils.MotionTrail as mtrail"


	# GENERAL
	runGeneralWindow ='''\
{0}
gtwindow.GeneralWindow().RUN_DOCKED()\
'''.format(pathGeneral)


	# FILE
	runSceneReload ='''\
{0}
scene.Reload()\
'''.format(pathLocators)

	runExitMaya ='''\
{0}
scene.ExitMaya()\
'''.format(pathLocators)


	# UTILS
	runSelectTransformHierarchy ='''\
{0}
selector.SelectTransformHierarchy()\
'''.format(pathLocators)


	# LOCATORS
	runLocatorsSizeScale ='''\
{0}
locators.SelectedLocatorsSizeScale\
'''.format(pathLocators)

	runLocatorsSizeSet ='''\
{0}
locators.SelectedLocatorsSizeSet\
'''.format(pathLocators)

	runLocatorCreate ='''\
{0}
locators.Create()\
'''.format(pathLocators)

	runLocatorsMatch ='''\
{0}
locators.CreateOnSelected(constraint = False)\
'''.format(pathLocators)

	runLocatorsParent ='''\
{0}
locators.CreateOnSelected(constraint = True)\
'''.format(pathLocators)

	runLocatorsPin ='''\
{0}
locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = True)\
'''.format(pathLocators)

	runLocatorsPinWithoutReverse ='''\
{0}
locators.CreateOnSelected(constraint = True, bake = True)\
'''.format(pathLocators)

	runLocatorsPinPos ='''\
{0}
locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = False)\
'''.format(pathLocators)

	runLocatorsPinRot ='''\
{0}
locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = False, constrainRotate = True)\
'''.format(pathLocators)

	runLocatorsRelative ='''\
{0}
locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True, skipLastReverse = False)\
'''.format(pathLocators)

	runLocatorsRelativeSkipLast ='''\
{0}
locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True)\
'''.format(pathLocators)

	runLocatorsRelativeWithoutReverse ='''\
{0}
locators.CreateAndBakeAsChildrenFromLastSelected()\
'''.format(pathLocators)

	runLocatorsAim ='''\
{0}
locators.CreateOnSelectedAim\
'''.format(pathLocators)


	# BAKING
	runBakeClassic ='''\
{0}
baker.BakeSelected\
'''.format(pathBaker)


	# ANIMATION
	runAnimOffset ='''\
{0}
animation.OffsetObjects\
'''.format(pathAnimation)
	runSetTimeline ='''\
{0}
timeline.SetTime\
'''.format(pathTimeline)


	# RIGGING
	runCopySkin ='''\
{0}
skinning.CopySkinWeightsFromLastMesh()\
'''.format(pathSkinning)


	# EXPERIMENTAL
	runMotionTrailCreate ='''\
{0}
mtrail.Create()\
'''.format(pathLocators)
	runMotionTrailSelect ='''\
{0}
mtrail.Select()\
'''.format(pathLocators)
	runMotionTrailDelete ='''\
{0}
mtrail.Delete()\
'''.format(pathLocators)


# LOGIC
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

# LOCATORS
def ToShelf_LocatorsSizeScale50(path, *args):
	MoveToShelf(path, Presets.runLocatorsSizeScale + "(0.5)", "LocatorsSizeScale50", "L50%")
def ToShelf_LocatorsSizeScale90(path, *args):
	MoveToShelf(path, Presets.runLocatorsSizeScale + "(0.9)", "LocatorsSizeScale90", "L90%")
def ToShelf_LocatorsSizeScale110(path, *args):
	MoveToShelf(path, Presets.runLocatorsSizeScale + "(1.1)", "LocatorsSizeScale110", "L110%")
def ToShelf_LocatorsSizeScale200(path, *args):
	MoveToShelf(path, Presets.runLocatorsSizeScale + "(2.0)", "LocatorsSizeScale200", "L200%")

def ToShelf_LocatorCreate(path, *args):
	MoveToShelf(path, Presets.runLocatorCreate, "LocatorCreate", "Loc")
def ToShelf_LocatorsMatch(path, *args):
	MoveToShelf(path, Presets.runLocatorsMatch, "LocatorsMatch", "LocMatch")
def ToShelf_LocatorsParent(path, *args):
	MoveToShelf(path, Presets.runLocatorsParent, "LocatorsParent", "LocParent")

def ToShelf_LocatorsPin(path, *args):
	MoveToShelf(path, Presets.runLocatorsPin, "LocatorsPin", "Pin")
def ToShelf_LocatorsPinWithoutReverse(path, *args):
	MoveToShelf(path, Presets.runLocatorsPinWithoutReverse, "LocatorsPinWithoutReverse", "Pin-")
def ToShelf_LocatorsPinPos(path, *args):
	MoveToShelf(path, Presets.runLocatorsPinPos, "LocatorsPinPos", "P-Pos")
def ToShelf_LocatorsPinRot(path, *args):
	MoveToShelf(path, Presets.runLocatorsPinRot, "LocatorsPinRot", "P-Rot")

def ToShelf_LocatorsRelative(path, *args):
	MoveToShelf(path, Presets.runLocatorsRelative, "Relative", "Rel")
def ToShelf_LocatorsRelativeSkipLast(path, *args):
	MoveToShelf(path, Presets.runLocatorsRelativeSkipLast, "RelativeSkipLast", "Rel-1")
def ToShelf_LocatorsRelativeWithoutReverse(path, *args):
	MoveToShelf(path, Presets.runLocatorsRelativeWithoutReverse, "RelativeWithoutReverse", "Rel-")

def ToShelf_LocatorsAim(path, name, rotateOnly, aimVector, *args):
	parameters = "(rotateOnly = {0}, aimVector = {1}, reverse = True)".format(rotateOnly, aimVector)
	MoveToShelf(path, Presets.runLocatorsAim + parameters, "LocatorsAim{0}".format(name), "Aim {0}".format(name))

# BAKING
def ToShelf_BakeClassic(path, *args):
	MoveToShelf(path, Presets.runBakeClassic + "(classic = True, preserveOutsideKeys = True)", "BakeClassic", "Bake")
def ToShelf_BakeClassicCutOut(path, *args):
	MoveToShelf(path, Presets.runBakeClassic + "(classic = True, preserveOutsideKeys = False)", "BakeClassicCutOut", "BakeCut")

# ANIMATION
def ToShelf_AnimOffset(path, direction, time, *args):
	MoveToShelf(path, Presets.runAnimOffset + "({0}, {1})".format(direction, time), "AnimOffset_{0}_{1}".format(direction, time), "AO{0}_{1}".format(direction, time))

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

