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

class Presets:
	pathGeneral = "import GETOOLS_SOURCE.modules.GeneralWindow as gtwindow"
	pathAnimation = "import GETOOLS_SOURCE.utils.Animation as animation"
	pathBaker = "import GETOOLS_SOURCE.utils.Baker as baker"
	pathBlendshapes = "import GETOOLS_SOURCE.utils.Blendshapes as blendshapes"
	pathConstraints = "import GETOOLS_SOURCE.utils.Constraints as constraints"
	pathDeformers = "import GETOOLS_SOURCE.utils.Deformers as deformers"
	pathInstall = "import GETOOLS_SOURCE.utils.Install as install"
	pathLocators = "import GETOOLS_SOURCE.utils.Locators as locators"
	pathMotionTrail = "import GETOOLS_SOURCE.utils.MotionTrail as mtrail"
	pathOther = "import GETOOLS_SOURCE.utils.Other as other"
	pathScene = "import GETOOLS_SOURCE.utils.Scene as scene"
	pathSelector = "import GETOOLS_SOURCE.utils.Selector as selector"
	pathSkinning = "import GETOOLS_SOURCE.utils.Skinning as skinning"
	pathTimeline = "import GETOOLS_SOURCE.utils.Timeline as timeline"
	pathToggles = "import GETOOLS_SOURCE.utils.Toggles as toggles"

	# GENERAL
	runGeneralWindow = pathGeneral + "\n" + "gtwindow.GeneralWindow().RUN_DOCKED()"

	# FILE
	runSceneReload = pathScene + "\n" + "scene.Reload()"
	runExitMaya = pathScene + "\n" + "scene.ExitMaya()"

	# UTILS
	runSelectHierarchy = pathSelector + "\n" + "selector.SelectHierarchy()"
	runCreateResetButton = pathInstall + "\n" + "install.CreateResetButton()"

	# TOGGLES
	# runToggleAllObjects = pathToggles + "\n" + "toggles.ToggleAllObjects()"
	runToggleCameras = pathToggles + "\n" + "toggles.ToggleCameras()"
	runToggleControlVertices = pathToggles + "\n" + "toggles.ToggleControlVertices()"
	runToggleDeformers = pathToggles + "\n" + "toggles.ToggleDeformers()"
	runToggleDimensions = pathToggles + "\n" + "toggles.ToggleDimensions()"
	runToggleDynamicConstraints = pathToggles + "\n" + "toggles.ToggleDynamicConstraints()"
	runToggleDynamics = pathToggles + "\n" + "toggles.ToggleDynamics()"
	runToggleFluids = pathToggles + "\n" + "toggles.ToggleFluids()"
	runToggleFollicles = pathToggles + "\n" + "toggles.ToggleFollicles()"
	runToggleGrid = pathToggles + "\n" + "toggles.ToggleGrid()"
	runToggleHairSystems = pathToggles + "\n" + "toggles.ToggleHairSystems()"
	runToggleHandles = pathToggles + "\n" + "toggles.ToggleHandles()"
	runToggleHulls = pathToggles + "\n" + "toggles.ToggleHulls()"
	runToggleIkHandles = pathToggles + "\n" + "toggles.ToggleIkHandles()"
	runToggleJoints = pathToggles + "\n" + "toggles.ToggleJoints()"
	runToggleLights = pathToggles + "\n" + "toggles.ToggleLights()"
	runToggleLocators = pathToggles + "\n" + "toggles.ToggleLocators()"
	runToggleManipulators = pathToggles + "\n" + "toggles.ToggleManipulators()"
	runToggleNCloths = pathToggles + "\n" + "toggles.ToggleNCloths()"
	runToggleNParticles = pathToggles + "\n" + "toggles.ToggleNParticles()"
	runToggleNRigids = pathToggles + "\n" + "toggles.ToggleNRigids()"
	runToggleNurbsCurves = pathToggles + "\n" + "toggles.ToggleNurbsCurves()"
	runToggleNurbsSurfaces = pathToggles + "\n" + "toggles.ToggleNurbsSurfaces()"
	runTogglePivots = pathToggles + "\n" + "toggles.TogglePivots()"
	runTogglePlanes = pathToggles + "\n" + "toggles.TogglePlanes()"
	runTogglePolymeshes = pathToggles + "\n" + "toggles.TogglePolymeshes()"
	runToggleShadows = pathToggles + "\n" + "toggles.ToggleShadows()"
	runToggleStrokes = pathToggles + "\n" + "toggles.ToggleStrokes()"
	runToggleSubdivSurfaces = pathToggles + "\n" + "toggles.ToggleSubdivSurfaces()"
	runToggleTextures = pathToggles + "\n" + "toggles.ToggleTextures()"

	# LOCATORS
	runLocatorsSizeScale = pathLocators + "\n" + "locators.SelectedLocatorsSizeScale"
	runLocatorsSizeSet = pathLocators + "\n" + "locators.SelectedLocatorsSizeSet"
	runLocatorCreate = pathLocators + "\n" + "locators.Create()"
	runLocatorsMatch = pathLocators + "\n" + "locators.CreateOnSelected(constraint = False)"
	runLocatorsParent = pathLocators + "\n" + "locators.CreateOnSelected(constraint = True)"
	runLocatorsPin = pathLocators + "\n" + "locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = True)"
	runLocatorsPinWithoutReverse = pathLocators + "\n" + "locators.CreateOnSelected(constraint = True, bake = True)"
	runLocatorsPinPos = pathLocators + "\n" + "locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = False)"
	runLocatorsPinRot = pathLocators + "\n" + "locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = False, constrainRotate = True)"
	runLocatorsRelative = pathLocators + "\n" + "locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True, skipLastReverse = False)"
	runLocatorsRelativeSkipLast = pathLocators + "\n" + "locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True)"
	runLocatorsRelativeWithoutReverse = pathLocators + "\n" + "locators.CreateAndBakeAsChildrenFromLastSelected()"
	runLocatorsAim = pathLocators + "\n" + "locators.CreateOnSelectedAim"

	# BAKING
	runBakeClassic = pathBaker + "\n" + "baker.BakeSelected"
	runBakeCustom = pathBaker + "\n" + "baker.BakeSelected"
	runBakeByLast = pathBaker + "\n" + "baker.BakeSelectedByLastObject"
	runBakeByWorld = pathBaker + "\n" + "baker.BakeSelectedByWorld"

	# ANIMATION
	runAnimOffset = pathAnimation + "\n" + "animation.OffsetObjects"
	runDeleteKeys = pathAnimation + "\n" + "animation.DeleteKeys(True)"
	runDeleteNonkeyable = pathAnimation + "\n" + "animation.DeleteKeysNonkeyable()"
	runDeleteStatic = pathAnimation + "\n" + "animation.DeleteStaticCurves()"
	runEulerFilter = pathAnimation + "\n" + "animation.FilterCurve()"
	runSetInfinity = pathAnimation + "\n" + "animation.SetInfinity"
	runSetTimeline = pathTimeline + "\n" + "timeline.SetTime"

	# RIGGING
	runConstraint = pathConstraints + "\n" + "constraints.ConstrainSelectedToLastObject"
	runDeleteConstraints = pathConstraints + "\n" + "constraints.DeleteConstraintsOnSelected()"
	runDisconnectTargets = pathConstraints + "\n" + "constraints.DisconnectTargetsFromConstraintOnSelected()"
	runRotateOrder = pathOther + "\n" + "other.RotateOrderVisibility"
	runSegmentScaleCompensateCompensate = pathOther + "\n" + "other.SegmentScaleCompensate"
	runJointDrawStyle = pathOther + "\n" + "other.JointDrawStyle"
	runCopySkin = pathSkinning + "\n" + "skinning.CopySkinWeightsFromLastMesh()"
	runWrapsCreate = pathDeformers + "\n" + "deformers.WrapsCreateOnSelected()"

	# runWrapsConvert = pathDeformers + "\n" + "ndeformers.WrapsConvertFromSelected()" # TODO
	runBlendshapesReconstruct = pathDeformers + "\n" + "deformers.BlendshapesReconstruction()"
	runBlendshapesZeroWeights = pathBlendshapes + "\n" + "blendshapes.ZeroBlendshapeWeightsOnSelected()"

	# EXPERIMENTAL
	runMotionTrailCreate = pathMotionTrail + "\n" + "mtrail.Create()"
	runMotionTrailSelect = pathMotionTrail + "\n" + "mtrail.Select()"
	runMotionTrailDelete = pathMotionTrail + "\n" + "mtrail.Delete()"


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


# TOGGLES
# def ToShelf_ToggleAllObjects(path, *args): MoveToShelf(path, Presets.runToggleAllObjects, "ToggleAllObjects", "tglAllObjects")
def ToShelf_ToggleCameras(path, *args): MoveToShelf(path, Presets.runToggleCameras, "ToggleCameras", "tglCameras")
def ToShelf_ToggleControlVertices(path, *args): MoveToShelf(path, Presets.runToggleControlVertices, "ToggleControlVertices", "tglControlVertices")
def ToShelf_ToggleDeformers(path, *args): MoveToShelf(path, Presets.runToggleDeformers, "ToggleDeformers", "tglDeformers")
def ToShelf_ToggleDimensions(path, *args): MoveToShelf(path, Presets.runToggleDimensions, "ToggleDimensions", "tglDimensions")
def ToShelf_ToggleDynamicConstraints(path, *args): MoveToShelf(path, Presets.runToggleDynamicConstraints, "ToggleDynamicConstraints", "tglDynamicConstraints")
def ToShelf_ToggleDynamics(path, *args): MoveToShelf(path, Presets.runToggleDynamics, "ToggleDynamics", "tglDynamics")
def ToShelf_ToggleFluids(path, *args): MoveToShelf(path, Presets.runToggleFluids, "ToggleFluids", "tglFluids")
def ToShelf_ToggleFollicles(path, *args): MoveToShelf(path, Presets.runToggleFollicles, "ToggleFollicles", "tglFollicles")
def ToShelf_ToggleGrid(path, *args): MoveToShelf(path, Presets.runToggleGrid, "ToggleGrid", "tglGrid")
def ToShelf_ToggleHairSystems(path, *args): MoveToShelf(path, Presets.runToggleHairSystems, "ToggleHairSystems", "tglHairSystems")
def ToShelf_ToggleHandles(path, *args): MoveToShelf(path, Presets.runToggleHandles, "ToggleHandles", "tglHandles")
def ToShelf_ToggleHulls(path, *args): MoveToShelf(path, Presets.runToggleHulls, "ToggleHulls", "tglHulls")
def ToShelf_ToggleIkHandles(path, *args): MoveToShelf(path, Presets.runToggleIkHandles, "ToggleIkHandles", "tglIkHandles")
def ToShelf_ToggleJoints(path, *args): MoveToShelf(path, Presets.runToggleJoints, "ToggleJoints", "tglJoints")
def ToShelf_ToggleLights(path, *args): MoveToShelf(path, Presets.runToggleLights, "ToggleLights", "tglLights")
def ToShelf_ToggleLocators(path, *args): MoveToShelf(path, Presets.runToggleLocators, "ToggleLocators", "tglLocators")
def ToShelf_ToggleManipulators(path, *args): MoveToShelf(path, Presets.runToggleManipulators, "ToggleManipulators", "tglManipulators")
def ToShelf_ToggleNCloths(path, *args): MoveToShelf(path, Presets.runToggleNCloths, "ToggleNCloths", "tglNCloths")
def ToShelf_ToggleNParticles(path, *args): MoveToShelf(path, Presets.runToggleNParticles, "ToggleNParticles", "tglNParticles")
def ToShelf_ToggleNRigids(path, *args): MoveToShelf(path, Presets.runToggleNRigids, "ToggleNRigids", "tglNRigids")
def ToShelf_ToggleNurbsCurves(path, *args): MoveToShelf(path, Presets.runToggleNurbsCurves, "ToggleNurbsCurves", "tglNurbsCurves")
def ToShelf_ToggleNurbsSurfaces(path, *args): MoveToShelf(path, Presets.runToggleNurbsSurfaces, "ToggleNurbsSurfaces", "tglNurbsSurfaces")
def ToShelf_TogglePivots(path, *args): MoveToShelf(path, Presets.runTogglePivots, "TogglePivots", "tglPivots")
def ToShelf_TogglePlanes(path, *args): MoveToShelf(path, Presets.runTogglePlanes, "TogglePlanes", "tglPlanes")
def ToShelf_TogglePolymeshes(path, *args): MoveToShelf(path, Presets.runTogglePolymeshes, "TogglePolymeshes", "tglPolymeshes")
def ToShelf_ToggleShadows(path, *args): MoveToShelf(path, Presets.runToggleShadows, "ToggleShadows", "tglShadows")
def ToShelf_ToggleStrokes(path, *args): MoveToShelf(path, Presets.runToggleStrokes, "ToggleStrokes", "tglStrokes")
def ToShelf_ToggleSubdivSurfaces(path, *args): MoveToShelf(path, Presets.runToggleSubdivSurfaces, "ToggleSubdivSurfaces", "tglSubdivSurfaces")
def ToShelf_ToggleTextures(path, *args): MoveToShelf(path, Presets.runToggleTextures, "ToggleTextures", "tglTextures")


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
# def ToShelf_WrapsConvert(path, *args): # TODO
# 	MoveToShelf(path, Presets.runWrapsConvert, "WrapsConvert", "WrapsConvert")
def ToShelf_BlendshapesReconstruct(path, *args):
	MoveToShelf(path, Presets.runBlendshapesReconstruct, "BSReconstruct", "BSReconstruct")
def ToShelf_BlendshapesZeroWeights(path, *args):
	MoveToShelf(path, Presets.runBlendshapesZeroWeights, "BSZeroWeights", "BSZeroWeights")


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

