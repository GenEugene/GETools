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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import os
import sys
import inspect

from ..utils import Shelf
from ..values import CodeSamples
from ..values import Enums


# LOGIC
def ReadFunctionAsString(func):
	source = inspect.getsource(func)

	# Remove first line and indents in code body
	lines = source.split('\n')
	lines = lines[1:-1]
	lines = [line.lstrip() for line in lines]
	linesCount = len(lines)
	result = ""
	
	for i in range(linesCount):
		result = result + lines[i]
		if (i < linesCount - 1):
			result = result + "\n"

	return result
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
	result = ""
	result += "import os" + "\n"
	result += "import sys" + "\n\n"
	result += GetFunctionString(path) + "\n\n"
	result += tool
	return result
def MoveToShelf(path, tool, label, labelImage, *args):
	command = GetFunctionStringForTool(path, tool)
	Shelf.AddToCurrentShelf(
		command = command,
		label = label,
		labelImage = labelImage,
		imageHighlightPath = labelImage
		)

# FILE
def ToShelf_ReloadScene(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SceneReload), "SceneReload", "Reload")
def ToShelf_ExitMaya(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.ExitMaya), "ExitMaya", "Exit")

# UTILS
def ToShelf_SelectHierarchy(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SelectHierarchy), "SelectHierarchy", "SelHi")
def ToShelf_CreateResetButton(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.CreateResetButton), "CreateResetButton", "Reset")

# TOGGLES
# def ToShelf_ToggleAllObjects(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.), "ToggleAllObjects", "tglAllObjects") # TODO
def ToShelf_ToggleCameras(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleCameras), "ToggleCameras", "tglCameras")
def ToShelf_ToggleControlVertices(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleControlVertices), "ToggleControlVertices", "tglControlVertices")
def ToShelf_ToggleDeformers(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleDeformers), "ToggleDeformers", "tglDeformers")
def ToShelf_ToggleDimensions(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleDimensions), "ToggleDimensions", "tglDimensions")
def ToShelf_ToggleDynamicConstraints(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleDynamicConstraints), "ToggleDynamicConstraints", "tglDynamicConstraints")
def ToShelf_ToggleDynamics(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleDynamics), "ToggleDynamics", "tglDynamics")
def ToShelf_ToggleFluids(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleFluids), "ToggleFluids", "tglFluids")
def ToShelf_ToggleFollicles(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleFollicles), "ToggleFollicles", "tglFollicles")
def ToShelf_ToggleGrid(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleGrid), "ToggleGrid", "tglGrid")
def ToShelf_ToggleHairSystems(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleHairSystems), "ToggleHairSystems", "tglHairSystems")
def ToShelf_ToggleHandles(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleHandles), "ToggleHandles", "tglHandles")
def ToShelf_ToggleHulls(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleHulls), "ToggleHulls", "tglHulls")
def ToShelf_ToggleIkHandles(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleIkHandles), "ToggleIkHandles", "tglIkHandles")
def ToShelf_ToggleJoints(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleJoints), "ToggleJoints", "tglJoints")
def ToShelf_ToggleLights(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleLights), "ToggleLights", "tglLights")
def ToShelf_ToggleLocators(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleLocators), "ToggleLocators", "tglLocators")
def ToShelf_ToggleManipulators(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleManipulators), "ToggleManipulators", "tglManipulators")
def ToShelf_ToggleNCloths(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleNCloths), "ToggleNCloths", "tglNCloths")
def ToShelf_ToggleNParticles(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleNParticles), "ToggleNParticles", "tglNParticles")
def ToShelf_ToggleNRigids(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleNRigids), "ToggleNRigids", "tglNRigids")
def ToShelf_ToggleNurbsCurves(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleNurbsCurves), "ToggleNurbsCurves", "tglNurbsCurves")
def ToShelf_ToggleNurbsSurfaces(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleNurbsSurfaces), "ToggleNurbsSurfaces", "tglNurbsSurfaces")
def ToShelf_TogglePivots(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.TogglePivots), "TogglePivots", "tglPivots")
def ToShelf_TogglePlanes(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.TogglePlanes), "TogglePlanes", "tglPlanes")
def ToShelf_TogglePolymeshes(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.TogglePolymeshes), "TogglePolymeshes", "tglPolymeshes")
def ToShelf_ToggleShadows(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleShadows), "ToggleShadows", "tglShadows")
def ToShelf_ToggleStrokes(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleStrokes), "ToggleStrokes", "tglStrokes")
def ToShelf_ToggleSubdivSurfaces(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleSubdivSurfaces), "ToggleSubdivSurfaces", "tglSubdivSurfaces")
def ToShelf_ToggleTextures(path, *args): MoveToShelf(path, ReadFunctionAsString(CodeSamples.ToggleTextures), "ToggleTextures", "tglTextures")

# LOCATORS
def ToShelf_LocatorsSizeScale50(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsSizeScale) + "(0.5)", "LocatorsSizeScale50", "L50%")
def ToShelf_LocatorsSizeScale90(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsSizeScale) + "(0.9)", "LocatorsSizeScale90", "L90%")
def ToShelf_LocatorsSizeScale110(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsSizeScale) + "(1.1)", "LocatorsSizeScale110", "L110%")
def ToShelf_LocatorsSizeScale200(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsSizeScale) + "(2.0)", "LocatorsSizeScale200", "L200%")

def ToShelf_LocatorCreate(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorCreate), "LocatorCreate", "Loc")
def ToShelf_LocatorsMatch(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsMatch), "LocatorsMatch", "LocMatch")
def ToShelf_LocatorsParent(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsParent), "LocatorsParent", "LocParent")

def ToShelf_LocatorsPin(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsPin), "LocatorsPin", "Pin")
def ToShelf_LocatorsPinWithoutReverse(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsPinWithoutReverse), "LocatorsPinWithoutReverse", "Pin-")
def ToShelf_LocatorsPinPos(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsPinPos), "LocatorsPinPos", "P-Pos")
def ToShelf_LocatorsPinRot(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsPinRot), "LocatorsPinRot", "P-Rot")

def ToShelf_LocatorsRelative(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsRelative), "Relative", "Rel")
def ToShelf_LocatorsRelativeSkipLast(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsRelativeSkipLast), "RelativeSkipLast", "Rel-1")
def ToShelf_LocatorsRelativeWithoutReverse(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsRelativeWithoutReverse), "RelativeWithoutReverse", "Rel-")

def ToShelf_LocatorsAim(path, name, rotateOnly, aimVector, *args):
	parameters = "(rotateOnly = {0}, aimVector = {1}, reverse = True)".format(rotateOnly, aimVector)
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.LocatorsAim) + parameters, "LocatorsAim{0}".format(name), "Aim {0}".format(name))

# BAKING
def ToShelf_BakeClassic(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BakeClassic) + "(classic = True, preserveOutsideKeys = True)", "BakeClassic", "Bake")
def ToShelf_BakeClassicCutOut(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BakeClassic) + "(classic = True, preserveOutsideKeys = False)", "BakeClassicCutOut", "BakeCut")
def ToShelf_BakeCustom(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BakeCustom) + "(classic = False, preserveOutsideKeys = True, selectedRange = True, channelBox = True)", "BakeCustom", "BakeC")
def ToShelf_BakeCustomCutOut(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BakeCustom) + "(classic = False, preserveOutsideKeys = False, selectedRange = True, channelBox = True)", "BakeCustomCutOut", "BakeCCut")

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
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BakeByLast) + parameters, "BakeByLast{0}".format(suffix), "BL{0}".format(suffix))
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
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BakeByWorld) + parameters, "BakeByWorld{0}".format(suffix), "BW{0}".format(suffix))

# ANIMATION
def ToShelf_AnimOffsetSelected(path, direction, time, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.AnimOffsetSelected) + "({0}, {1})".format(direction, time), "AnimOffset_{0}_{1}".format(direction, time), "AO{0}_{1}".format(direction, time))

def ToShelf_DeleteKeys(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.DeleteKeys), "DeleteKeys", "DKeys")
def ToShelf_DeleteNonkeyable(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.DeleteNonkeyable), "DeleteNonkeyable", "DNonkeyable")
def ToShelf_DeleteStatic(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.DeleteStatic), "DeleteStatic", "DStatic")

def ToShelf_EulerFilter(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.EulerFilter), "EulerFilter", "Euler")
def ToShelf_SetInfinity(path, mode, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetInfinity) + "({0})".format(mode), "SetInfinity{0}".format(mode), "Inf{0}".format(mode))

# TIMELINE
def ToShelf_SetTimelineMinOut(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(3)", "SetTimelineMinOut", "<<")
def ToShelf_SetTimelineMinIn(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(1)", "SetTimelineMinIn", "<-")
def ToShelf_SetTimelineMaxIn(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(2)", "SetTimelineMaxIn", "->")
def ToShelf_SetTimelineMaxOut(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(4)", "SetTimelineMaxOut", ">>")
def ToShelf_SetTimelineFocusOut(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(5)", "SetTimelineFocusOut", "<->")
def ToShelf_SetTimelineFocusIn(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(6)", "SetTimelineFocusIn", ">-<")
def ToShelf_SetTimelineSet(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SetTimeline) + "(7)", "SetTimelineSet", "|<->|")

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

	MoveToShelf(path, ReadFunctionAsString(CodeSamples.Constraint) + "(maintainOffset = {0}, parent = {1}, point = {2}, orient = {3}, scale = {4})".format(maintainOffset, parent, point, orient, scale), "Constraint{0}".format(suffix), "C{0}".format(suffix))
def ToShelf_DeleteConstraints(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.DeleteConstraints), "DeleteConstraints", "DeleteConstraints")
def ToShelf_DisconnectTargets(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.DisconnectTargets), "DisconnectTargets", "Disconnect")

def ToShelf_RotateOrder(path, mode, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.RotateOrder) + "({0})".format(mode), "RotateOrder{0}".format(mode), "RO{0}".format(mode))
def ToShelf_SegmentScaleCompensate(path, mode, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SegmentScaleCompensate) + "({0})".format(mode), "SegmentScaleCompensate{0}".format(mode), "SSC{0}".format(mode))
def ToShelf_JointDrawStyle(path, mode, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.JointDrawStyle) + "({0})".format(mode), "JointDrawStyle{0}".format(mode), "J{0}".format(mode))

def ToShelf_CopySkin(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.CopySkin), "CopySkin", "CopySkin")
def ToShelf_SelectSkinnedMeshesOrJoints(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.SelectSkinnedMeshesOrJoints), "SelectSkinned", "SelectSkinned")

def ToShelf_WrapsCreate(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.WrapsCreate), "WrapsCreate", "WrapsCreate")
def ToShelf_WrapsConvert(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.WrapsConvert), "WrapsConvert", "WrapsConvert") # TODO add corresponding logic
def ToShelf_BlendshapesReconstruct(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BlendshapesReconstruct), "BSReconstruct", "BSReconstruct")
def ToShelf_BlendshapesExtractShapes(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BlendshapesExtractShapes), "BSExtractShapes", "BSExtractShapes")
def ToShelf_BlendshapesZeroWeights(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.BlendshapesZeroWeights), "BSZeroWeights", "BSZeroWeights")

# MOTION TRAIL
def ToShelf_MotionTrailCreate(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.MotionTrailCreate), "MotionTrailCreate", "MTCreate")
def ToShelf_MotionTrailSelect(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.MotionTrailSelect), "MotionTrailSelect", "MTSelect")
def ToShelf_MotionTrailDelete(path, *args):
	MoveToShelf(path, ReadFunctionAsString(CodeSamples.MotionTrailDelete), "MotionTrailDelete", "MTDelete")

# RESET BUTTON
def CreateResetButton(*args): # TODO get all published attributes
	# get namespace
	# get all published attributes
	# generate reset code
	# create button and fill command

	# nameNamespace = "rig_Staff_01:"
	# cmds.setAttr(nameNamespace + "ct_Root.translateX", 0)
	
	print("Reset button for objects")

