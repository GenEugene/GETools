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

import maya.cmds as cmds
from functools import partial

from .. import Settings
from ..utils import Blendshapes
from ..utils import Colors
from ..utils import Constraints
from ..utils import Curves
from ..utils import Deformers
from ..utils import Other
from ..utils import Skinning
from ..utils import UI


class RiggingAnnotations:
	### Constraints
	_textAllSelectedConstrainToLast = "All selected objects will be constrained to last selected object"
	constraintReverse = "Reverse the direction of operation from last to first selected"
	constraintMaintain = "Use maintain offset"
	constraintOffset = "[IN DEVELOPMENT]\nAdd extra locators structure with ability to make offset animation"
	constraintParent = "Parent constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintPoint = "Point constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintOrient = "Orient constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintScale = "Scale constrain.\n{allToLast}".format(allToLast = _textAllSelectedConstrainToLast)
	constraintAim = "[IN DEVELOPMENT]\nAim constrain.".format(allToLast = _textAllSelectedConstrainToLast) # TODO
	constraintDisconnectSelected = "Disconnect targets objects from last selected object. They will be deleted from constraint attributes."
	constraintDelete = "Delete all constraints on selected objects"

	### Utils
	_rotateOrder = "rotate order attribute in channel box for all selected objects"
	rotateOrderShow = "Show {0}".format(_rotateOrder)
	rotateOrderHide = "Hide {0}".format(_rotateOrder)
	_scaleCompensate = "segment scale compensate attribute for all selected joints"
	scaleCompensateOn = "Activate {0}".format(_scaleCompensate)
	scaleCompensateOff = "Deactivate {0}".format(_scaleCompensate)
	_jointDrawStyle = "selected joints draw style"
	jointDrawStyleBone = "Bone {0}".format(_jointDrawStyle)
	jointDrawStyleHidden = "Hidden {0}".format(_jointDrawStyle)
	copySkinWeights = "Copy skin weights from last selected object to all other selected objects"

	### Deformers
	wrapsCreate = "Create a wrap deformer on selected objects.\nThe last object used as a source deformation object."
	blendshapeCopyFromTarget = "Reconstruct blendshapes on selected objects from the last selected object.\nThe last object must have a blendshape node."
	blendshapeExtract = "Extract blendshapes as duplicated meshes.\nPaint weights before extraction if needed."
	blendshapeZeroWeights = "Zero all blendshape weights on selected objects"

	### Curves
	curveCreateFromSelectedObjects = "Create a curve from selected objects.\nEach curve point will be created in the pivot."
	curveCreateFromTrajectory = "***DRAFT***\nCreate a curve from objects trajectories."

class Rigging:
	_version = "v1.3"
	_name = "RIGGING"
	_title = _name + " " + _version

	def __init__(self):
		self.checkboxConstraintReverse = None
		self.checkboxConstraintMaintain = None
		# self.checkboxConstraintOffset = None
	def UICreate(self, layoutMain):
		### CONSTRAINTS
		layoutConstraints = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "CONSTRAINTS", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumnConstraints = cmds.columnLayout(parent = layoutConstraints, adjustableColumn = True)
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutColumnConstraints, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.separator(style = "none")
		self.checkboxConstraintReverse = cmds.checkBox(label = "Reverse", value = False, annotation = RiggingAnnotations.constraintReverse)
		self.checkboxConstraintMaintain = cmds.checkBox(label = "Maintain", value = False, annotation = RiggingAnnotations.constraintMaintain)
		# self.checkboxConstraintOffset = UI.Checkbox(label = "**Offset", value = False, annotation = RiggingAnnotations.constraintOffset)
		cmds.separator(style = "none")
		#
		countOffsets = 4
		cmds.gridLayout(parent = layoutColumnConstraints, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Parent", command = self.ConstrainParent, backgroundColor = Colors.red10, annotation = RiggingAnnotations.constraintParent)
		cmds.button(label = "Point", command = self.ConstrainPoint, backgroundColor = Colors.red10, annotation = RiggingAnnotations.constraintPoint)
		cmds.button(label = "Orient", command = self.ConstrainOrient, backgroundColor = Colors.red10, annotation = RiggingAnnotations.constraintOrient)
		cmds.button(label = "Scale", command = self.ConstrainScale, backgroundColor = Colors.red10, annotation = RiggingAnnotations.constraintScale)
		# cmds.button(label = "**Aim", command = self.ConstrainAim, backgroundColor = Colors.red10, annotation = RiggingAnnotations.constraintAim, enable = False) # TODO
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutColumnConstraints, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Disconnect", command = Constraints.DisconnectTargetsFromConstraintOnSelected, backgroundColor = Colors.red50, annotation = RiggingAnnotations.constraintDisconnectSelected)
		cmds.button(label = "Delete Constraints", command = Constraints.DeleteConstraintsOnSelected, backgroundColor = Colors.red50, annotation = RiggingAnnotations.constraintDelete)


		### UTILS
		layoutUtils = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "UTILS", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumnUtils = cmds.columnLayout(parent = layoutUtils, adjustableColumn = True)
		#
		rowLayoutSize = (130, 50, 50)
		#
		cmds.rowLayout(parent = layoutColumnUtils, numberOfColumns = 3, columnWidth3 = rowLayoutSize, columnAlign = [(1, "right"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)])
		cmds.text(label = "Rotate Order")
		cmds.button(label = "SHOW", command = partial(Other.RotateOrderVisibility, True), backgroundColor = Colors.green10, annotation = RiggingAnnotations.rotateOrderShow)
		cmds.button(label = "HIDE", command = partial(Other.RotateOrderVisibility, False), backgroundColor = Colors.green10, annotation = RiggingAnnotations.rotateOrderHide)
		#
		cmds.rowLayout(parent = layoutColumnUtils, numberOfColumns = 3, columnWidth3 = rowLayoutSize, columnAlign = [(1, "right"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)])
		cmds.text(label = "Scale Compensate")
		cmds.button(label = "ON", command = partial(Other.SegmentScaleCompensate, True), backgroundColor = Colors.orange10, annotation = RiggingAnnotations.scaleCompensateOn)
		cmds.button(label = "OFF", command = partial(Other.SegmentScaleCompensate, False), backgroundColor = Colors.orange10, annotation = RiggingAnnotations.scaleCompensateOff)
		#
		cmds.rowLayout(parent = layoutColumnUtils, numberOfColumns = 3, columnWidth3 = rowLayoutSize, columnAlign = [(1, "right"), (2, "center"), (3, "center")], columnAttach = [(1, "both", 0), (2, "both", 0), (3, "both", 0)])
		cmds.text(label = "Joint Draw Style")
		cmds.button(label = "BONE", command = partial(Other.JointDrawStyle, 0), backgroundColor = Colors.yellow10, annotation = RiggingAnnotations.jointDrawStyleBone)
		cmds.button(label = "HIDDEN", command = partial(Other.JointDrawStyle, 2), backgroundColor = Colors.yellow10, annotation = RiggingAnnotations.jointDrawStyleHidden)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumnUtils, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Copy Skin Weights From Last Selected", command = Skinning.CopySkinWeightsFromLastMesh, backgroundColor = Colors.blue10, annotation = RiggingAnnotations.copySkinWeights)
		
		### BLENDSHAPES
		layoutBlendshapes = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "BLENDSHAPES", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumnBlendshapes = cmds.columnLayout(parent = layoutBlendshapes, adjustableColumn = True)
		#
		countOffsets = 3
		cmds.gridLayout(parent = layoutColumnBlendshapes, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Wraps", command = Deformers.WrapsCreateOnSelected, backgroundColor = Colors.yellow10, annotation = RiggingAnnotations.wrapsCreate)
		# cmds.button(label = "**Convert", command = Deformers.WrapConvertToBlendshapes) # TODO
		cmds.button(label = "Reconstruct", command = Deformers.BlendshapesReconstruction, backgroundColor = Colors.green50, annotation = RiggingAnnotations.blendshapeCopyFromTarget)
		cmds.button(label = "Extract Shapes", command = Blendshapes.ExtractShapesFromSelected, backgroundColor = Colors.green10, annotation = RiggingAnnotations.blendshapeExtract)
		#
		countOffsets = 1
		cmds.gridLayout(parent = layoutColumnBlendshapes, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Zero Weights", command = Blendshapes.ZeroBlendshapeWeightsOnSelected, backgroundColor = Colors.blackWhite100, annotation = RiggingAnnotations.blendshapeZeroWeights)
		
		### CURVES
		layoutCurves = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "CURVES", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumnCurves = cmds.columnLayout(parent = layoutCurves, adjustableColumn = True)
		#
		countOffsets = 2
		cmds.gridLayout(parent = layoutColumnCurves, numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "From Selected Objects", command = Curves.CreateCurveFromSelectedObjects, backgroundColor = Colors.blue10, annotation = RiggingAnnotations.curveCreateFromSelectedObjects)
		cmds.button(label = "From Trajectory", command = Curves.CreateCurveFromTrajectory, backgroundColor = Colors.orange10, annotation = RiggingAnnotations.curveCreateFromTrajectory)


	### CONSTRAINTS
	def GetCheckboxConstraintReverse(self):
		return cmds.checkBox(self.checkboxConstraintReverse, query = True, value = True)
	def GetCheckboxConstraintMaintain(self):
		return cmds.checkBox(self.checkboxConstraintMaintain, query = True, value = True)

	def ConstrainParent(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.GetCheckboxConstraintReverse(), maintainOffset = self.GetCheckboxConstraintMaintain(), parent = True, point = False, orient = False, scale = False, aim = False)
	def ConstrainPoint(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.GetCheckboxConstraintReverse(), maintainOffset = self.GetCheckboxConstraintMaintain(), parent = False, point = True, orient = False, scale = False, aim = False)
	def ConstrainOrient(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.GetCheckboxConstraintReverse(), maintainOffset = self.GetCheckboxConstraintMaintain(), parent = False, point = False, orient = True, scale = False, aim = False)
	def ConstrainScale(self, *args):
		Constraints.ConstrainSelectedToLastObject(reverse = self.GetCheckboxConstraintReverse(), maintainOffset = self.GetCheckboxConstraintMaintain(), parent = False, point = False, orient = False, scale = True, aim = False)
	def ConstrainAim(self, *args): # TODO
		Constraints.ConstrainSelectedToLastObject(reverse = self.GetCheckboxConstraintReverse(), maintainOffset = self.GetCheckboxConstraintMaintain(), parent = False, point = False, orient = False, scale = False, aim = True)

