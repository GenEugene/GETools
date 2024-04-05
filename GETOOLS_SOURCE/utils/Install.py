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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Logic in this module is not optimal enough, need manually change path names, methods and parameters.

import os
import sys

from ..utils import Shelf

from ..values import Enums

class Presets: # TODO simplify
	pathGeneral =\
	"import GETOOLS_SOURCE.modules.GeneralWindow as gtwindow"
	pathScene =\
	"import GETOOLS_SOURCE.utils.Scene as scene"
	pathInstall =\
	"import GETOOLS_SOURCE.utils.Install as install"
	pathBaker =\
	"import GETOOLS_SOURCE.utils.Baker as baker"
	pathSelector =\
	"import GETOOLS_SOURCE.utils.Selector as selector"
	pathOther =\
	"import GETOOLS_SOURCE.utils.Other as other"
	pathDeformers =\
	"import GETOOLS_SOURCE.utils.Deformers as deformers"
	pathConstraints =\
	"import GETOOLS_SOURCE.utils.Constraints as constraints"
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
'''.format(pathScene)

	runExitMaya ='''\
{0}
scene.ExitMaya()\
'''.format(pathScene)


	# UTILS
	runSelectHierarchy ='''\
{0}
selector.SelectHierarchy()\
'''.format(pathSelector)
	
	runCreateResetButton ='''\
{0}
install.CreateResetButton()\
'''.format(pathInstall)


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

	runBakeCustom ='''\
{0}
baker.BakeSelected\
'''.format(pathBaker)

	runBakeByLast ='''\
{0}
baker.BakeSelectedByLastObject\
'''.format(pathBaker)

	runBakeByWorld ='''\
{0}
baker.BakeSelectedByWorld\
'''.format(pathBaker)


	# ANIMATION
	runAnimOffset ='''\
{0}
animation.OffsetObjects\
'''.format(pathAnimation)

	runDeleteKeys ='''\
{0}
animation.DeleteKeys(True)\
'''.format(pathAnimation)

	runDeleteNonkeyable ='''\
{0}
animation.DeleteKeysNonkeyable()\
'''.format(pathAnimation)

	runDeleteStatic ='''\
{0}
animation.DeleteStaticCurves()\
'''.format(pathAnimation)

	runEulerFilter ='''\
{0}
animation.FilterCurve()\
'''.format(pathAnimation)

	runSetInfinity ='''\
{0}
animation.SetInfinity\
'''.format(pathAnimation)

	runSetTimeline ='''\
{0}
timeline.SetTime\
'''.format(pathTimeline)


	# RIGGING
	runConstraint ='''\
{0}
constraints.ConstrainSelectedToLastObject\
'''.format(pathConstraints)

	runDeleteConstraints ='''\
{0}
constraints.DeleteConstraintsOnSelected()\
'''.format(pathConstraints)

	runDisconnectTargets ='''\
{0}
constraints.DisconnectTargetsFromConstraintOnSelected()\
'''.format(pathConstraints)

	runRotateOrder ='''\
{0}
other.RotateOrderVisibility\
'''.format(pathOther)

	runSegmentScaleCompensateCompensate ='''\
{0}
other.SegmentScaleCompensate\
'''.format(pathOther)

	runJointDrawStyle ='''\
{0}
other.JointDrawStyle\
'''.format(pathOther)

	runCopySkin ='''\
{0}
skinning.CopySkinWeightsFromLastMesh()\
'''.format(pathSkinning)

	runWrapsCreate ='''\
{0}
deformers.WrapsCreateOnSelected()\
'''.format(pathDeformers)

	runBlendshapesProjecting ='''\
{0}
deformers.BlendshapesProjecting()\
'''.format(pathDeformers)


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
	return """\
if not os.path.exists("{path}"):
	raise IOError(r"The source path {path} does not exist!")

if "{path}" not in sys.path:
	sys.path.insert(0, "{path}")\
""".format(path = path)
def GetFunctionStringForTool(path, tool, *args):
	return """\
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
	MoveToShelf(path, Presets.runSelectHierarchy, "SelectHierarchy", "SelHi")
def ToShelf_CreateResetButton(path, *args):
	MoveToShelf(path, Presets.runCreateResetButton, "CreateResetButton", "Reset")

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
def ToShelf_BakeCustom(path, *args):
	MoveToShelf(path, Presets.runBakeCustom + "(classic = False, preserveOutsideKeys = True, selectedRange = True, channelBox = True)", "BakeCustom", "BakeC")
def ToShelf_BakeCustomCutOut(path, *args):
	MoveToShelf(path, Presets.runBakeCustom + "(classic = False, preserveOutsideKeys = False, selectedRange = True, channelBox = True)", "BakeCustomCutOut", "BakeCCut")

def ToShelf_BakeByLast(path, translate, rotate, *args):
	if (translate and rotate):
		suffix = ""
		parameters = "(selectedRange = True, channelBox = True)"
	elif (translate and not rotate):
		suffix = "POS"
		attributes = Enums.Attributes.translateShort
		parameters = "(selectedRange = True, channelBox = False, attributes = {0})".format(attributes)
	elif (not translate and rotate):
		suffix = "ROT"
		attributes = Enums.Attributes.rotateShort
		parameters = "(selectedRange = True, channelBox = False, attributes = {0})".format(attributes)
	MoveToShelf(path, Presets.runBakeByLast + parameters, "BakeByLast{0}".format(suffix), "BL{0}".format(suffix))
def ToShelf_BakeByWorld(path, translate, rotate, *args):
	if (translate and rotate):
		suffix = ""
		parameters = "(selectedRange = True, channelBox = True)"
	elif (translate and not rotate):
		suffix = "POS"
		attributes = Enums.Attributes.translateShort
		parameters = "(selectedRange = True, channelBox = False, attributes = {0})".format(attributes)
	elif (not translate and rotate):
		suffix = "ROT"
		attributes = Enums.Attributes.rotateShort
		parameters = "(selectedRange = True, channelBox = False, attributes = {0})".format(attributes)
	MoveToShelf(path, Presets.runBakeByWorld + parameters, "BakeByWorld{0}".format(suffix), "BW{0}".format(suffix))


# ANIMATION
def ToShelf_AnimOffset(path, direction, time, *args):
	MoveToShelf(path, Presets.runAnimOffset + "({0}, {1})".format(direction, time), "AnimOffset_{0}_{1}".format(direction, time), "AO{0}_{1}".format(direction, time))

def ToShelf_DeleteKeys(path, *args):
	MoveToShelf(path, Presets.runDeleteKeys, "DeleteKeys", "DKeys")
def ToShelf_DeleteNonkeyable(path, *args):
	MoveToShelf(path, Presets.runDeleteNonkeyable, "DeleteNonkeyable", "DNonkeyable")
def ToShelf_DeleteStatic(path, *args):
	MoveToShelf(path, Presets.runDeleteStatic, "DeleteStatic", "DStatic")

def ToShelf_EulerFilter(path, *args):
	MoveToShelf(path, Presets.runEulerFilter, "EulerFilter", "Euler")
def ToShelf_SetInfinity(path, mode, *args):
	MoveToShelf(path, Presets.runSetInfinity + "({0})".format(mode), "SetInfinity{0}".format(mode), "Inf{0}".format(mode))

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
def ToShelf_Constraint(path, maintainOffset, parent, point, orient, scale, *args):
	if (maintainOffset):
		suffixMaintain = "M"
	else:
		suffixMaintain = ""
	
	if (parent):
		suffix = "Parent"
	elif (not parent and point):
		suffix = "Point"
	elif (not parent and orient):
		suffix = "Orient"
	elif (not parent and not point and not orient and scale):
		suffix = "Scale"
	
	suffix = suffixMaintain + suffix

	MoveToShelf(path, Presets.runConstraint + "(maintainOffset = {0}, parent = {1}, point = {2}, orient = {3}, scale = {4})".format(maintainOffset, parent, point, orient, scale), "Constraint{0}".format(suffix), "C{0}".format(suffix))
def ToShelf_DeleteConstraints(path, *args):
	MoveToShelf(path, Presets.runDeleteConstraints, "DeleteConstraints", "DeleteConstraints")
def ToShelf_DisconnectTargets(path, *args):
	MoveToShelf(path, Presets.runDisconnectTargets, "DisconnectTargets", "Disconnect")

def ToShelf_RotateOrder(path, mode, *args):
	MoveToShelf(path, Presets.runRotateOrder + "({0})".format(mode), "RotateOrder{0}".format(mode), "RO{0}".format(mode))
def ToShelf_SegmentScaleCompensate(path, mode, *args):
	MoveToShelf(path, Presets.runSegmentScaleCompensateCompensate + "({0})".format(mode), "SegmentScaleCompensate{0}".format(mode), "SSC{0}".format(mode))
def ToShelf_JointDrawStyle(path, mode, *args):
	MoveToShelf(path, Presets.runJointDrawStyle + "({0})".format(mode), "JointDrawStyle{0}".format(mode), "J{0}".format(mode))

def ToShelf_CopySkin(path, *args):
	MoveToShelf(path, Presets.runCopySkin, "CopySkin", "CopySkin")

def ToShelf_WrapsCreate(path, *args):
	MoveToShelf(path, Presets.runWrapsCreate, "WrapsCreate", "WrapsCreate")
def ToShelf_BlendshapesProjecting(path, *args):
	MoveToShelf(path, Presets.runBlendshapesProjecting, "BSProjecting", "BSProjecting")


# MOTION TRAIL
def ToShelf_MotionTrailCreate(path, *args):
	MoveToShelf(path, Presets.runMotionTrailCreate, "MotionTrailCreate", "MTCreate")
def ToShelf_MotionTrailSelect(path, *args):
	MoveToShelf(path, Presets.runMotionTrailSelect, "MotionTrailSelect", "MTSelect")
def ToShelf_MotionTrailDelete(path, *args):
	MoveToShelf(path, Presets.runMotionTrailDelete, "MotionTrailDelete", "MTDelete")


# RESET BUTTON
def CreateResetButton(*args): # TODO get all published attributes
	# get namespace
	# get all published attributes
	# generate reset code
	# create button and fill command

	# nameNamespace = "rig_Staff_01:"
	# cmds.setAttr(nameNamespace + "ct_Root.translateX", 0)
	
	print("Reset button for objects")

