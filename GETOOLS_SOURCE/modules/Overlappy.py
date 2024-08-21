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
import maya.mel as mel
from math import pow, sqrt
from functools import partial

from .. import Settings
from ..utils import Animation
from ..utils import Baker
from ..utils import Colors
from ..utils import Constraints
from ..utils import Layers
from ..utils import MayaSettings
from ..utils import Selector
from ..utils import Text
from ..utils import Timeline
from ..utils import UI
from ..values import Enums
from ..values import Icons


class OverlappyAnnotations:
	# Setup
	setup = "Create particle rig for first selected object. Use this step for setup settings. \nSetup runs every time for each selected object."
	setupDelete = "Delete particle rig if exists"

	# Baking
	translation = "Bake simulation for translation attributes"
	translationWithOffset = "Bake simulation for translation attributes with offset"
	rotation = "Bake simulation for rotation attributes"
	comboTranslateRotate = "Bake translation and rotation in order"
	comboRotateTranslate = "Bake rotation and translation in order"
	scale = "Bake simulation for scale attributes"

	# Layers
	layerDeleteBase = "All animation layers will be deleted"
	layerDeleteTemp = "Only Temp layer and child layers will be deleted"
	layerDeleteSafe = "Only Safe layer and child layers will be deleted"
	layerMoveTemp = "Move Temp layer sublayers to Safe layer"
	layerMoveSafe = "Move Safe layer sublayers to Temp layer"

	# Options
	checkboxHierarchy = "Bake simulation for all child hierarhy of selected objects"
	checkboxLayer = "Bake animation into override layers. \nIf turned off animation will be baked directly to selected objects"
	checkboxLoop = "Use for cycles. \nImportant to have cycle constant animation curves"
	checkboxClean = "Remove particle setup after baking end"

	# Particle
	particleRadius = "Particle Radius"
	particleConserve = "Particle Conserve"
	particleDrag = "Particle Drag"
	particleDamp = "Particle Damp"
	particleGoalSmooth = "Particle Goal Smooth"
	particleGoalWeight = "Particle Goal Weight"
	particleTimeScale = "Nucleus Time Scale"

	# Offset
	offsetMirrorX = "Mirror particle offset value to opposite"
	offsetMirrorY = offsetMirrorX
	offsetMirrorZ = offsetMirrorX
	offsetX = "Move particle from original object. Important to use offset for Rotation baking"
	offsetY = offsetX
	offsetZ = offsetX

class OverlappySettings:
	# NAMING
	prefix = "ovlp"
	prefixLayer = "_" + prefix

	nameGroup = prefix + "Group"
	nameLocGoalTarget = (prefix + "LocGoal", prefix + "LocTarget")
	nameLocAim = (prefix + "LocAimBase", prefix + "LocAimHidden", prefix + "LocAim", prefix + "LocAimUp")
	nameNucleus = prefix + "Nucleus"
	nameParticle = prefix + "Particle"
	nameLoft = (prefix + "LoftStart", prefix + "LoftEnd", prefix + "LoftShape")
	nameLayers = (prefixLayer + "TEMP_", prefixLayer + "SAFE_", "pos_", "rot_")
	
	# LOFT
	loftFactor = 0.9
	loftMinDistance = 5
	
	# SIMULATION SETTINGS # TODO: move to preset
	checkboxesOptions = (False, True, False, True)
	particleRadius = 5
	particleConserve = 1
	particleDrag = 0.01
	particleDamp = 0
	goalSmooth = 3
	goalWeight = 0.5
	nucleusTimeScale = 1
	loopOffset = 2 # TODO set count of pre cycles by ui
	
	# SLIDERS (field min/max, slider min/max)
	rangePRadius = (0, float("inf"), 0, 10)
	rangePConserve = (0, 1, 0, 1)
	rangePDrag = (0, 10, 0, 1)
	rangePDamp = (0, 10, 0, 1)
	rangeGSmooth = (0, 100, 0, 10)
	rangeGWeight = (0, 1, 0, 1)
	rangeNTimeScale = (0.001, 100, 0.001, 4)
	rangeOffsetX = (float("-inf"), float("inf"), 0, 100)
	rangeOffsetY = (float("-inf"), float("inf"), 0, 100)
	rangeOffsetZ = (float("-inf"), float("inf"), 0, 100)
	
class Overlappy:
	version = "v2.10"
	name = "OVERLAPPY"
	title = name + " " + version

	# HACK use only for code editor # TODO try to find better way to get access to other classes with cross import
	# from ..modules import GeneralWindow
	# def __init__(self, generalInstance: GeneralWindow.GeneralWindow):
	def __init__(self, generalInstance):
		self.generalInstance = generalInstance

		# VALUES
		self.time = Timeline.TimeRangeHandler()
		self.startPositionGoalParticle = [None, (0, 0, 0)]
		
		# OBJECTS
		self.selectedObject = ""
		self.locGoalTarget = ["", ""]
		self.locAim = ["", "", "", ""]
		self.particle = ""
		self.nucleus = ""
		self.loft = ["", "", ""]
		self.layers = ["", ""]
		self.nucleusNodesBefore = [""]
		self.nucleusNodesAfter = [""]
		
		# LAYOUTS
		self.windowMain = None
		self.layoutButtons = None
		self.layoutLayers = None
		self.layoutOptions = None
		self.layoutSimulation = None
		self.layoutOffset = None
		
		# CHECKBOXES
		self.checkboxHierarchy = None
		self.checkboxLayer = None
		self.checkboxLoop = None
		self.checkboxClean = None
		self.checkboxMirrorX = None
		self.checkboxMirrorY = None
		self.checkboxMirrorZ = None
		
		# SLIDERS
		self.sliderPRadius = None
		self.sliderPConserve = None
		self.sliderPDrag = None
		self.sliderPDamp = None
		self.sliderGSmooth = None
		self.sliderGWeight = None
		self.sliderNTimeScale = None
		self.sliderOffsetX = None
		self.sliderOffsetY = None
		self.sliderOffsetZ = None
	def UICreate(self, layoutMain):
		self.UILayoutMenuBar(layoutMain)
		self.UILayoutButtons(layoutMain)
		self.UILayoutLayers(layoutMain)
		self.UILayoutOptions(layoutMain)
		self.UILayoutParticleAttributes(layoutMain)
		self.UILayoutParticleOffset(layoutMain)
	def UILayoutMenuBar(self, layoutMain):
		cmds.columnLayout("layoutMenuBar", parent = layoutMain, adjustableColumn = True, width = Settings.windowWidthMargin)
		cmds.menuBarLayout()

		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Reset Settings", command = self._ResetAllValues, image = Icons.rotateClockwise)

		cmds.menu(label = "Select", tearOff = True)
		cmds.menuItem(label = "Object", command = self._SelectObject, image = Icons.cursor)
		cmds.menuItem(label = "Particle", command = self._SelectParticle, image = Icons.particle)
		cmds.menuItem(label = "Nucleus", command = self._SelectNucleus, image = Icons.nucleus)
		cmds.menuItem(label = "Target locator", command = self._SelectTarget, image = Icons.locator)
		cmds.menuItem(label = "Aim locator", command = self._SelectAim, image = Icons.locator)
	def UILayoutButtons(self, layoutMain):
		# SETUP
		self.layoutButtons = cmds.frameLayout("layoutButtons", label = Settings.frames2Prefix + "BUTTONS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutButtons, adjustableColumn = True)

		count = 2
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		#
		cmds.button(label = "SETUP", command = self._SetupInit, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setup)
		# cmds.button(label = "Scan setup into scene", command = self._SetupScan, backgroundColor = Colors.green10)
		cmds.button(label = "DELETE", command = self._SetupDelete, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setupDelete)

		# BAKING
		count = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		#
		cmds.button(label = "TRANSLATION", command = partial(self._BakeVariants, 1), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.translation)
		cmds.popupMenu()
		cmds.menuItem(label = "translate with offset", command = partial(self._BakeVariants, 2)) # TODO popup message if offsets are zero
		#
		cmds.button(label = "ROTATION", command = partial(self._BakeVariants, 3), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.rotation) # TODO popup message if offsets are zero
		#
		cmds.button(label = "COMBO", command = partial(self._BakeVariants, 4), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.comboTranslateRotate) # TODO popup message if offsets are zero
		cmds.popupMenu()
		cmds.menuItem(label = "rotate + translate", command = partial(self._BakeVariants, 5))
		#
		# cmds.button(label = "SCALE", command = partial(self._BakeVariants, 6), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.scale) # TODO implement scale simulation
		pass
	def UILayoutLayers(self, layoutMain):
		self.layoutLayers = cmds.frameLayout("layoutLayers", label = Settings.frames2Prefix + "LAYERS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutLayers, adjustableColumn = True)
		
		count = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Delete BaseAnimation layer", command = partial(Layers.Delete, "BaseAnimation"), backgroundColor = Colors.red50, annotation = OverlappyAnnotations.layerDeleteBase)

		count = 2
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Delete Temp layer", command = partial(Layers.Delete, OverlappySettings.nameLayers[0]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteTemp)
		cmds.button(label = "Move to Safe layer", command = partial(self._LayerMoveToSafeOrTemp, True), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveTemp)
		
		cmds.button(label = "Delete Safe layer", command = partial(Layers.Delete, OverlappySettings.nameLayers[1]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteSafe)
		cmds.button(label = "Move to Temp layer", command = partial(self._LayerMoveToSafeOrTemp, False), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveSafe)
	def UILayoutOptions(self, layoutMain):
		self.layoutOptions = cmds.frameLayout("layoutOptions", label = Settings.frames2Prefix + "OPTIONS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		
		count = 4
		cmds.gridLayout(parent = self.layoutOptions, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		
		# _optionsResetAll = self._ResetOptions # , commandResetAll = _optionsResetAll
		
		self.checkboxHierarchy = UI.Checkbox(label = "Hierarchy", value = OverlappySettings.checkboxesOptions[0], annotation = OverlappyAnnotations.checkboxHierarchy)
		self.checkboxLayer = UI.Checkbox(label = "Layer", value = OverlappySettings.checkboxesOptions[1], annotation = OverlappyAnnotations.checkboxLayer)
		self.checkboxLoop = UI.Checkbox(label = "Loop", value = OverlappySettings.checkboxesOptions[2], annotation = OverlappyAnnotations.checkboxLoop) # FIXME make cycle infinity before bake
		self.checkboxClean = UI.Checkbox(label = "Clean", value = OverlappySettings.checkboxesOptions[3], annotation = OverlappyAnnotations.checkboxClean)
	def UILayoutParticleAttributes(self, layoutMain):
		self.layoutSimulation = cmds.frameLayout("layoutParticleSliders", label = Settings.frames2Prefix + "PARTICLE ATTRIBUTES", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutSimulation, adjustableColumn = True)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click") # TODO add reset all function

		commandDefault = self._UpdateParticleAttributes

		layoutSliders1 = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)
		self.sliderPRadius = UI.Slider(
			parent = layoutSliders1,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "Radius",
			annotation = OverlappyAnnotations.particleRadius,
			value = OverlappySettings.particleRadius,
			minMax = OverlappySettings.rangePRadius,
			menuReset = True,
		)

		# cmds.separator(parent = self.layoutSimulation, style = "in", height = 1)
		cmds.separator(parent = layoutColumn, style = "in")
		
		layoutSliders2 = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)
		self.sliderPConserve = UI.Slider(
			parent = layoutSliders2,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "Conserve",
			annotation = OverlappyAnnotations.particleConserve,
			value = OverlappySettings.particleConserve,
			minMax = OverlappySettings.rangePConserve,
			menuReset = True,
		)
		
		self.sliderPDrag = UI.Slider(
			parent = layoutSliders2,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "Drag",
			annotation = OverlappyAnnotations.particleDrag,
			value = OverlappySettings.particleDrag,
			minMax = OverlappySettings.rangePDrag,
			menuReset = True,
		)
		
		self.sliderPDamp = UI.Slider(
			parent = layoutSliders2,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "Damp",
			annotation = OverlappyAnnotations.particleDamp,
			value = OverlappySettings.particleDamp,
			minMax = OverlappySettings.rangePDamp,
			menuReset = True,
		)
		
		self.sliderGSmooth = UI.Slider(
			parent = layoutSliders2,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "G.Smooth",
			annotation = OverlappyAnnotations.particleGoalSmooth,
			value = OverlappySettings.goalSmooth,
			minMax = OverlappySettings.rangeGSmooth,
			menuReset = True,
		)
		
		self.sliderGWeight = UI.Slider(
			parent = layoutSliders2,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "G.Weight",
			annotation = OverlappyAnnotations.particleGoalWeight,
			value = OverlappySettings.goalWeight,
			minMax = OverlappySettings.rangeGWeight,
			menuReset = True,
		)
		
		self.sliderNTimeScale = UI.Slider(
			parent = layoutSliders2,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "Time Scale",
			annotation = OverlappyAnnotations.particleTimeScale,
			value = OverlappySettings.nucleusTimeScale,
			minMax = OverlappySettings.rangeNTimeScale,
			menuReset = True,
		)
	def UILayoutParticleOffset(self, layoutMain):
		self.layoutOffset = cmds.frameLayout("layoutParticleOffset", label = Settings.frames2Prefix + "PARTICLE OFFSET", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutOffset, adjustableColumn = True)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click") # TODO add reset all function

		count = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		# cmds.separator()
		# , commandResetAll = self._ResetOffsets
		self.checkboxMirrorX = UI.Checkbox(label = "Mirror X", command = partial(self._OffsetsUpdate, True), annotation = OverlappyAnnotations.offsetMirrorX)
		self.checkboxMirrorY = UI.Checkbox(label = "Mirror Y", command = partial(self._OffsetsUpdate, True), annotation = OverlappyAnnotations.offsetMirrorY)
		self.checkboxMirrorZ = UI.Checkbox(label = "Mirror Z", command = partial(self._OffsetsUpdate, True), annotation = OverlappyAnnotations.offsetMirrorZ)
		

		layoutSliders = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)

		commandDefault = self._OffsetsUpdate

		self.sliderOffsetX = UI.Slider(
			parent = layoutSliders,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "   Move X",
			annotation = OverlappyAnnotations.offsetX,
			minMax = OverlappySettings.rangeOffsetX,
			menuReset = True,
		)

		self.sliderOffsetY = UI.Slider(
			parent = layoutSliders,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "   Move Y",
			annotation = OverlappyAnnotations.offsetY,
			minMax = OverlappySettings.rangeOffsetY,
			menuReset = True,
		)

		self.sliderOffsetZ = UI.Slider(
			parent = layoutSliders,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "   Move Z",
			annotation = OverlappyAnnotations.offsetZ,
			minMax = OverlappySettings.rangeOffsetZ,
			menuReset = True,
		)


	### LOGIC
	def _SetupInit(self, *args):
		# Get min/max anim range time and reset time slider
		self.time.Scan()
		self.time.SetCurrent(self.time.values[2])
		
		# Remove previous setup if exists
		self._SetupDelete(deselect = False)
		
		# Get selected objects
		self.selectedObject = Selector.MultipleObjects()
		if (self.selectedObject == None):
			self.selectedObject = ""
			return
		
		self.selectedObject = self.selectedObject[0]

		# Create group
		cmds.select(clear = True)
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		cmds.group(empty = True, name = OverlappySettings.nameGroup)
		
		# Run setup logic
		self._SetupCreate(self.selectedObject)
		self._OffsetsUpdate(cacheReset = True)
		cmds.select(self.selectedObject, replace = True)
	def _SetupCreate(self, objCurrent, *args): # TODO replace locators by locators class
		# Names
		objConverted = Text.ConvertSymbols(objCurrent)
		nameLocGoal = OverlappySettings.nameLocGoalTarget[0] + objConverted
		nameLocParticle = OverlappySettings.nameLocGoalTarget[1] + objConverted
		nameNucleus = OverlappySettings.nameNucleus + objConverted
		nameParticle = OverlappySettings.nameParticle + objConverted
		nameLocAimBase = OverlappySettings.nameLocAim[0] + objConverted
		nameLocAimHidden = OverlappySettings.nameLocAim[1] + objConverted
		nameLocAim = OverlappySettings.nameLocAim[2] + objConverted
		nameLocAimUp = OverlappySettings.nameLocAim[3] + objConverted
		nameLoftStart = OverlappySettings.nameLoft[0] + objConverted
		nameLoftEnd = OverlappySettings.nameLoft[1] + objConverted
		nameLoftShape = OverlappySettings.nameLoft[2] + objConverted

		# Create locator for goal
		self.locGoalTarget[0] = cmds.spaceLocator(name = nameLocGoal)[0]
		cmds.parent(self.locGoalTarget[0], OverlappySettings.nameGroup)
		cmds.matchTransform(self.locGoalTarget[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.locGoalTarget[0], maintainOffset = True)
		cmds.setAttr(self.locGoalTarget[0] + ".visibility", 0)
		self.startPositionGoalParticle[0] = cmds.xform(self.locGoalTarget[0], query = True, translation = True)

		# Nucleus node
		self.nucleusNodesBefore = cmds.ls(type = "nucleus")
		self.nucleus = cmds.createNode("nucleus", name = nameNucleus)
		cmds.connectAttr("time1.outTime", self.nucleus + ".currentTime")
		cmds.parent(self.nucleus, OverlappySettings.nameGroup)
		# self.sliderNTimeScale.startName = self.nucleus
		cmds.setAttr(self.nucleus + ".gravity", 0)
		cmds.setAttr(self.nucleus + ".timeScale", self.sliderNTimeScale.Get())
		cmds.setAttr(self.nucleus + ".startFrame", self.time.values[2])
		cmds.setAttr(self.nucleus + ".visibility", 0)

		# Create particle, goal and get selected object position
		position = cmds.xform(objCurrent, query = True, worldSpace = True, rotatePivot = True)
		self.particle = cmds.nParticle(name = nameParticle, position = position, conserve = 1)[0]
		cmds.goal(useTransformAsGoal = True, goal = self.locGoalTarget[0])
		cmds.parent(self.particle, OverlappySettings.nameGroup)
		# self.startPositionGoalParticle[1] = cmds.xform(self.particle, query = True, translation = True)
		cmds.setAttr(self.particle + ".overrideEnabled", 1)
		cmds.setAttr(self.particle + ".overrideDisplayType", 2)

		# Reconnect particle to temp nucleus and remove extra nodes
		mel.eval("assignNSolver {0}".format(nameNucleus))
		self.nucleusNodesAfter = cmds.ls(type = "nucleus")
		nodesForRemoving = [item for item in self.nucleusNodesAfter if item not in self.nucleusNodesBefore]
		for item in nodesForRemoving:
			if (item != self.nucleus):
				# cmds.warning("extra node deleted {0}".format(item))
				cmds.delete(item)

		# Set simulation attributes
		cmds.setAttr(self.particle + "Shape.radius", self.sliderPRadius.Get())
		cmds.setAttr(self.particle + "Shape.solverDisplay", 1)
		cmds.setAttr(self.particle + "Shape.conserve", self.sliderPConserve.Get())
		cmds.setAttr(self.particle + "Shape.drag", self.sliderPDrag.Get())
		cmds.setAttr(self.particle + "Shape.damp", self.sliderPDamp.Get())
		cmds.setAttr(self.particle + "Shape.goalSmoothness", self.sliderGSmooth.Get())
		cmds.setAttr(self.particle + "Shape.goalWeight[0]", self.sliderGWeight.Get())

		# Create and connect locator to particle
		self.locGoalTarget[1] = cmds.spaceLocator(name = nameLocParticle)[0]
		cmds.parent(self.locGoalTarget[1], OverlappySettings.nameGroup)
		cmds.matchTransform(self.locGoalTarget[1], objCurrent, position = True, rotation = True)
		cmds.connectAttr(self.particle + ".center", self.locGoalTarget[1] + ".translate", force = True)
		cmds.setAttr(self.locGoalTarget[1] + ".visibility", 0)

		# Create base aim locator
		self.locAim[0] = cmds.spaceLocator(name = nameLocAimBase)[0]
		cmds.parent(self.locAim[0], OverlappySettings.nameGroup)
		cmds.matchTransform(self.locAim[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.locAim[0], maintainOffset = True)
		cmds.setAttr(self.locAim[0] + ".visibility", 0)

		# Create hidden aim locator
		self.locAim[1] = cmds.spaceLocator(name = nameLocAimHidden)[0]
		cmds.matchTransform(self.locAim[1], self.locAim[0], position = True, rotation = True)
		cmds.parent(self.locAim[1], self.locAim[0])
		cmds.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		cmds.delete(self.locAim[1] + "_aimConstraint1")
		self.locAim[3] = cmds.duplicate(self.locAim[1], name = nameLocAimUp)[0]
		cmds.parent(self.locAim[3], self.locAim[1])
		cmds.setAttr(self.locAim[3] + ".ty", 100)
		cmds.parent(self.locAim[3], self.locAim[0])
		cmds.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.locAim[3]) # "scene" "object" "objectrotation" "vector" "none"
		
		# Create aim locator
		self.locAim[2] = cmds.spaceLocator(name = nameLocAim)[0]
		cmds.matchTransform(self.locAim[2], self.locAim[0], position = True, rotation = True)
		cmds.parent(self.locAim[2], self.locAim[0])

		# Create aim loft
		self.loft[0] = cmds.circle(name = nameLoftStart, degree = 1, sections = 4, normal = (0, 1, 0))[0]
		self.loft[1] = cmds.duplicate(self.loft[0], name = nameLoftEnd)[0]
		scale1 = 0.001
		scale2 = self.sliderPRadius.Get() * OverlappySettings.loftFactor
		cmds.setAttr(self.loft[0] + ".scaleX", scale1)
		cmds.setAttr(self.loft[0] + ".scaleY", scale1)
		cmds.setAttr(self.loft[0] + ".scaleZ", scale1)
		cmds.setAttr(self.loft[1] + ".scaleX", scale2)
		cmds.setAttr(self.loft[1] + ".scaleY", scale2)
		cmds.setAttr(self.loft[1] + ".scaleZ", scale2)
		cmds.setAttr(self.loft[0] + ".visibility", 0)
		cmds.setAttr(self.loft[1] + ".visibility", 0)
		#
		cmds.matchTransform(self.loft[0], self.locAim[2], position = True, rotation = True)
		cmds.parent(self.loft[0], self.locAim[2])
		cmds.matchTransform(self.loft[1], self.locGoalTarget[1], position = True)
		cmds.parent(self.loft[1], self.locGoalTarget[1])
		cmds.aimConstraint(self.loft[0], self.loft[1], weight = 1, aimVector = (0, 1, 0), upVector = (0, 1, 0), worldUpType = "vector", worldUpVector = (0, 0, 1))
		#
		self.loft[2] = cmds.loft(self.loft[0], self.loft[1], name = nameLoftShape, sectionSpans = 4, reverseSurfaceNormals = 0, uniform = 1, polygon = 0)[0]
		cmds.parent(self.loft[2], OverlappySettings.nameGroup)
		cmds.setAttr(self.loft[2] + ".overrideEnabled", 1)
		cmds.setAttr(self.loft[2] + ".overrideDisplayType", 2)
		cmds.setAttr(self.loft[2] + ".overrideShading", 0)
		
		if (self._LoftGetDistance() < OverlappySettings.loftMinDistance):
			cmds.setAttr(self.loft[2] + ".visibility", 0)
	def _SetupScan(self, *args): # TODO rework or delete
		# Check overlappy group
		if (not cmds.objExists(OverlappySettings.nameGroup)):
			cmds.warning("Overlappy object doesn't exists")
			return
		
		# Get children of group
		children = cmds.listRelatives(OverlappySettings.nameGroup)
		if (len(children) == 0):
			cmds.warning("Overlappy object has no children objects")
			return
		
		# Try to get suffix name
		tempList = (OverlappySettings.nameLocGoalTarget[0], OverlappySettings.nameLocGoalTarget[1], OverlappySettings.nameParticle, OverlappySettings.nameLocAim[0], OverlappySettings.nameLoft[2])
		objectName = ""
		for child in children:
			for item in tempList:
				splitNames = child.split(item)
				if (len(splitNames) < 2):
					continue
				lastName = splitNames[-1]
				if (objectName == ""):
					objectName = lastName
				else:
					if (objectName == lastName):
						continue
					else:
						cmds.warning("Suffix \"{0}\" don't equals to \"{1}\"".format(objectName, lastName))
		converted = Text.ConvertSymbols(objectName, False)
		if (cmds.objExists(converted)):
			self.selectedObject = converted
		
		def CheckAndSet(name):
			if (cmds.objExists(name + objectName)):
				return name + objectName
			else:
				return
		
		# Objects
		self.locGoalTarget[0] = CheckAndSet(OverlappySettings.nameLocGoalTarget[0])
		self.locGoalTarget[1] = CheckAndSet(OverlappySettings.nameLocGoalTarget[1])
		self.locAim[0] = CheckAndSet(OverlappySettings.nameLocAim[0])
		self.locAim[1] = CheckAndSet(OverlappySettings.nameLocAim[1])
		self.locAim[2] = CheckAndSet(OverlappySettings.nameLocAim[2])
		self.particle = CheckAndSet(OverlappySettings.nameParticle)
		self.loft[0] = CheckAndSet(OverlappySettings.nameLoft[0])
		self.loft[1] = CheckAndSet(OverlappySettings.nameLoft[1])
		self.loft[2] = CheckAndSet(OverlappySettings.nameLoft[2])
		
		# Time and offset
		self.time.Scan()
		self.time.SetCurrent(self.time.values[2])
		self.startPositionGoalParticle[0] = cmds.xform(self.locAim[0], query = True, translation = True)
		self.time.SetCurrentCached()
		
		# Nucleus
		# _nucleus = cmds.ls(type = "nucleus")
		# if (len(_nucleus) > 0):
		# 	self.nucleus = _nucleus[0]
			# self.sliderNTimeScale.startName = self.nucleus
		
		# Get sliders
		# self.sliderPRadius.Scan()
		# self._GetSimulation()
		# self._GetOffsets()
		pass
	def _SetupDelete(self, deselect=True, *args):
		self.selectedObject = ""
		self.locGoalTarget = ["", ""]
		self.locAim = ["", "", "", ""]
		self.particle = ""
		self.nucleus = ""
		self.loft = ["", "", ""]
		
		# Delete group
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		
		if (deselect):
			cmds.select(clear = True)
	def _OffsetsUpdate(self, cacheReset=False, *args): # TODO rework
		if (type(cacheReset) is float):
			cacheReset = False
		if (cacheReset):
			self.sliderOffsetX.ResetCached()
			self.sliderOffsetY.ResetCached()
			self.sliderOffsetZ.ResetCached()
		
		# Check and set cached value
		checkX = self.sliderOffsetX.GetCached() != self.sliderOffsetX.Get()
		checkY = self.sliderOffsetY.GetCached() != self.sliderOffsetY.Get()
		checkZ = self.sliderOffsetZ.GetCached() != self.sliderOffsetZ.Get()
		if (checkX or checkY or checkZ):
			self.sliderOffsetX.SetCached()
			self.sliderOffsetY.SetCached()
			self.sliderOffsetZ.SetCached()
		else:
			return

		self._ValuesSetParticleOffset()

		checkSelected = self.selectedObject == "" or not cmds.objExists(self.selectedObject)
		checkGoal = not cmds.objExists(self.locGoalTarget[0])
		checkAim = not cmds.objExists(self.locAim[2])
		checkStartPos = self.startPositionGoalParticle[0] == None
		
		if (checkSelected or checkGoal or checkAim or checkStartPos):
			return

		cmds.currentTime(self.time.values[2])

		# Mirrors
		mirror = [1, 1, 1]
		if (self.checkboxMirrorX.Get()):
			mirror[0] = -1
		if (self.checkboxMirrorY.Get()):
			mirror[1] = -1
		if (self.checkboxMirrorZ.Get()):
			mirror[2] = -1
		
		# Get values from sliders
		values = (
			self.sliderOffsetX.Get() * mirror[0],
			self.sliderOffsetY.Get() * mirror[1],
			self.sliderOffsetZ.Get() * mirror[2],
			)
		
		# Set locGoal constraint offset
		goalAttributes = (
			self.locGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateX",
			self.locGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateY",
			self.locGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateZ",
			)
		cmds.setAttr(goalAttributes[0], values[0])
		cmds.setAttr(goalAttributes[1], values[1])
		cmds.setAttr(goalAttributes[2], values[2])
		
		# Get offset
		goalPosition = cmds.xform(self.locGoalTarget[0], query = True, translation = True)
		goalOffset = (
			self.startPositionGoalParticle[0][0] - goalPosition[0],
			self.startPositionGoalParticle[0][1] - goalPosition[1],
			self.startPositionGoalParticle[0][2] - goalPosition[2],
			)
		
		# Set particle attributes
		particleAttributes = (
			OverlappySettings.nameParticle + Text.ConvertSymbols(self.selectedObject) + ".translateX",
			OverlappySettings.nameParticle + Text.ConvertSymbols(self.selectedObject) + ".translateY",
			OverlappySettings.nameParticle + Text.ConvertSymbols(self.selectedObject) + ".translateZ",
			)

		cmds.setAttr(particleAttributes[0], self.startPositionGoalParticle[1][0] - goalOffset[0])
		cmds.setAttr(particleAttributes[1], self.startPositionGoalParticle[1][1] - goalOffset[1])
		cmds.setAttr(particleAttributes[2], self.startPositionGoalParticle[1][2] - goalOffset[2])
		
		# Reposition aim up locator and reconstrain aim
		selected = cmds.ls(selection = True)
		cmds.delete(self.locAim[1] + "_aimConstraint1")
		cmds.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		cmds.delete(self.locAim[1] + "_aimConstraint1")
		cmds.parent(self.locAim[3], self.locAim[1])
		cmds.setAttr(self.locAim[3] + ".tx", 0)
		cmds.setAttr(self.locAim[3] + ".ty", 100)
		cmds.setAttr(self.locAim[3] + ".tz", 0)
		cmds.parent(self.locAim[3], self.locAim[0])
		cmds.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.locAim[3])
		cmds.select(selected, replace = True)
		
		# Reconstrain aim locator to hidden aim
		cmds.setAttr(self.locAim[2] + ".rotateX", 0)
		cmds.setAttr(self.locAim[2] + ".rotateY", 0)
		cmds.setAttr(self.locAim[2] + ".rotateZ", 0)
		cmds.orientConstraint(self.locAim[1], self.locAim[2], maintainOffset = True)


	### SELECT
	def _Select(self, name="", *args):
		if (name != ""):
			if (cmds.objExists(name)):
				cmds.select(name, replace = True)
			else:
				cmds.warning("\"{0}\" object doesn't exists".format(name))
		else:
			cmds.warning("Object name is not specified")
	def _SelectObject(self, *args): self._Select(self.selectedObject)
	def _SelectParticle(self, *args): self._Select(self.particle)
	def _SelectNucleus(self, *args): self._Select(self.nucleus)
	def _SelectTarget(self, *args): self._Select(self.locGoalTarget[1])
	def _SelectAim(self, *args): self._Select(self.locAim[2])
	

	### VALUES
	def _SetParticleAttribute(self, sliderValue, startName, attributeName, addSelectedName, *args):
		selectedName = self.selectedObject
		if (selectedName == ""):
			return
		
		# Add selected name or not
		selectedName = Text.ConvertSymbols(selectedName)
		if (addSelectedName):
			resultName = startName + selectedName + attributeName
		else:
			resultName = startName + attributeName
		
		cmds.setAttr(resultName, sliderValue)
	def _UpdateParticleAttributes(self, *args):
		self._SetParticleAttribute(self.sliderPRadius.Get(), OverlappySettings.nameParticle, "Shape.radius", True)
		self._SetParticleAttribute(self.sliderPConserve.Get(), OverlappySettings.nameParticle, "Shape.conserve", True)
		self._SetParticleAttribute(self.sliderPDrag.Get(), OverlappySettings.nameParticle, "Shape.drag", True)
		self._SetParticleAttribute(self.sliderPDamp.Get(), OverlappySettings.nameParticle, "Shape.damp", True)
		self._SetParticleAttribute(self.sliderGSmooth.Get(), OverlappySettings.nameParticle, "Shape.goalSmoothness", True)
		self._SetParticleAttribute(self.sliderGWeight.Get(), OverlappySettings.nameParticle, "Shape.goalWeight[0]", True)
		self._SetParticleAttribute(self.sliderNTimeScale.Get(), self.nucleus, ".timeScale", False)
		self._LoftUpdate()
	def _ValuesSetParticleOffset(self, *args):
		self._SetParticleAttribute(self.sliderOffsetX.Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateX", True)
		self._SetParticleAttribute(self.sliderOffsetY.Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateY", True)
		self._SetParticleAttribute(self.sliderOffsetZ.Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateZ", True)
		self._LoftUpdate()
	
	def _LoftUpdate(self, *args):
		if (self.loft[1] == ""):
			return
		
		if (not cmds.objExists(self.loft[1])):
			return
		
		scale = self.sliderPRadius.Get() * OverlappySettings.loftFactor
		cmds.setAttr(self.loft[1] + ".scaleX", scale)
		cmds.setAttr(self.loft[1] + ".scaleY", scale)
		cmds.setAttr(self.loft[1] + ".scaleZ", scale)
		
		if (self._LoftGetDistance() < OverlappySettings.loftMinDistance):
			cmds.setAttr(self.loft[2] + ".visibility", 0)
		else:
			cmds.setAttr(self.loft[2] + ".visibility", 1)
	def _LoftGetDistance(self, *args):
		vector = (
			self.sliderOffsetX.Get(),
			self.sliderOffsetY.Get(),
			self.sliderOffsetZ.Get(),
			)

		return sqrt(pow(vector[0], 2) + pow(vector[1], 2) + pow(vector[2], 2)) # Distance formula : V((x2 - x1)2 + (y2 - y1)2 + (z2 - z1)2)

	# def _GetSimulation(self, *args): # TODO rework scan logic
	# 	self.sliderPConserve.Scan()
	# 	self.sliderPDrag.Scan()
	# 	self.sliderPDamp.Scan()
	# 	self.sliderGSmooth.Scan()
	# 	self.sliderGWeight.Scan()
	# 	self.sliderNTimeScale.Scan()
	# def _GetOffsets(self, *args):
	# 	self.sliderOffsetX.Scan()
	# 	self.sliderOffsetY.Scan()
	# 	self.sliderOffsetZ.Scan()
	
	def _ResetAllValues(self, *args):
		self._ResetOptions()
		self._ResetSimulation(True)
		self._ResetOffsets()
	def _ResetOptions(self, *args):
		self.checkboxHierarchy.Reset()
		self.checkboxLayer.Reset()
		self.checkboxLoop.Reset()
		self.checkboxClean.Reset()
	def _ResetSimulation(self, full=False, *args):
		if (full):
			self.sliderPRadius.Reset()
		self.sliderPConserve.Reset()
		self.sliderPDrag.Reset()
		self.sliderPDamp.Reset()
		self.sliderGSmooth.Reset()
		self.sliderGWeight.Reset()
		self.sliderNTimeScale.Reset()
		self._UpdateParticleAttributes()
	def _ResetOffsets(self, *args):
		self.checkboxMirrorX.Reset()
		self.checkboxMirrorY.Reset()
		self.checkboxMirrorZ.Reset()
		self.sliderOffsetX.Reset()
		self.sliderOffsetY.Reset()
		self.sliderOffsetZ.Reset()
		self._ValuesSetParticleOffset()
	

	### BAKE
	def _BakeLogic(self, parent, zeroOffsets=False, translation=True, deleteSetupLock=False, *args):
		# Filter attributes
		if (translation):
			attributesType = Enums.Attributes.translateShort
		else:
			attributesType = Enums.Attributes.rotateShort
		attrs = ["", "", ""]
		
		selected = self.selectedObject
		for i in range(len(attrs)):
			attrs[i] = "{0}.{1}".format(selected, attributesType[i])
		attributesFiltered = []

		# TODO replace filtering by new attributes filtering method
		for i in range(len(attrs)):
			keyed = cmds.keyframe(attrs[i], query = True)
			if (keyed):
				muted = cmds.mute(attrs[i], query = True)
				if (muted):
					continue
			
			locked = cmds.getAttr(attrs[i], lock = True)
			keyable = cmds.getAttr(attrs[i], keyable = True)
			settable = cmds.getAttr(attrs[i], settable = True)
			constrained = False
			connections = cmds.listConnections(attrs[i])
			
			if (connections):
				for connection in connections:
					type = cmds.nodeType(connection)
					if (type in Enums.Constraints.list):
						constrained = True
			
			if (not locked and keyable and settable and not constrained):
				attributesFiltered.append(attributesType[i])
		
		if (len(attributesFiltered) == 0):
			cmds.warning("No attributes. Overlappy setup deleted")
			self._SetupDelete()
			return
		
		# Keyframe target attributes
		cmds.setKeyframe(selected, attribute = attributesFiltered)

		# Zero offsets
		if (zeroOffsets):
			value1 = self.sliderOffsetX.Get()
			value2 = self.sliderOffsetY.Get()
			value3 = self.sliderOffsetZ.Get()
			self.sliderOffsetX.Reset()
			self.sliderOffsetY.Reset()
			self.sliderOffsetZ.Reset()
		
		# Set time range
		self.time.Scan()
		startTime = self.time.values[2]
		if (self.checkboxLoop.Get()):
			startTime = self.time.values[2] - self.time.values[3] * OverlappySettings.loopOffset
			self.time.SetMin(startTime)
			self.time.SetCurrent(startTime)
		cmds.setAttr(self.nucleus + ".startFrame", startTime) # TODO bug when select ovlp objects
		
		# Start logic
		name = "_rebake_" + Text.ConvertSymbols(selected)
		clone = cmds.duplicate(selected, name = name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		
		for attribute in Enums.Attributes.translateShort:
			cmds.setAttr(clone[0] + "." + attribute, lock = False)
		for attribute in Enums.Attributes.rotateShort:
			cmds.setAttr(clone[0] + "." + attribute, lock = False)
		
		cmds.parentConstraint(parent, clone, maintainOffset = True) # skipTranslate
		cmds.select(clone, replace = True)
		
		# Bake
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		Constraints.DeleteConstraints(clone)
		
		# Copy keys, create layers and paste keys
		cmds.copyKey(clone, time = (self.time.values[2], self.time.values[3]), attribute = attributesFiltered)
		
		if (self.checkboxLayer.Get()):
			if (translation):
				name = OverlappySettings.nameLayers[2] + selected
			else:
				name = OverlappySettings.nameLayers[3] + selected
			animLayer = self._LayerCreate(name)
			
			attrsLayer = []
			for attributeFiltered in attributesFiltered:
				attrsLayer.append("{0}.{1}".format(selected, attributeFiltered))
			
			cmds.animLayer(animLayer, edit = True, attribute = attrsLayer)
			cmds.pasteKey(selected, option = "replace", attribute = attributesFiltered, animLayer = animLayer)
		else:
			cmds.pasteKey(selected, option = "replaceCompletely", attribute = attributesFiltered)
		cmds.delete(clone)
		
		# Set time range
		if (self.checkboxLoop.Get()):
			startTime = self.time.values[2]
			cmds.setAttr(self.nucleus + ".startFrame", startTime)
			self.time.Reset()
			Animation.SetInfinityCycle(selected)
		else:
			Animation.SetInfinityConstant(selected)
		
		# Delete setup
		if (self.checkboxClean.Get()):
			if (not deleteSetupLock):
				self._SetupDelete()
		
		# Restore offsets sliders
		if (zeroOffsets):
			self.sliderOffsetX.Set(value1)
			self.sliderOffsetY.Set(value2)
			self.sliderOffsetZ.Set(value3)
			self._OffsetsUpdate(True)
	def _BakeVariants(self, variant, *args):
		selected = Selector.MultipleObjects()
		if (selected == None):
			return
		
		# Check zero particle offset
		if variant in [3, 4, 5]:
			checkOffsetX = self.sliderOffsetX.Get() == 0
			checkOffsetY = self.sliderOffsetY.Get() == 0
			checkOffsetZ = self.sliderOffsetZ.Get() == 0
			if (checkOffsetX and checkOffsetY and checkOffsetZ):
				dialogResult = cmds.confirmDialog(
					title = "Zero particle offset detected",
					message = "For ROTATION BAKING, set the particle offset to non-zero values.\nIf all XYZ values are zero, the particle will stay in the same position as the original object, and no rotation will occur.\n",
					messageAlign = "left",
					icon = "warning",
					button = ["Continue anyway", "Cancel"],
					annotation = ["Bake with zero offset, no useful animation will be baked", "Cancel baking operation"],
					defaultButton = "Cancel",
					cancelButton = "Cancel",
					dismissString = "TODO: dismissString"
					)
				if (dialogResult == "Cancel"):
					cmds.warning("Overlappy Rotation Baking cancelled")
					return

		MayaSettings.CachedPlaybackDeactivate()

		if (self.checkboxHierarchy.Get()):
			selected = Selector.SelectHierarchyTransforms()
		
		def RunBakeLogicVariant():
			if (variant == 1):
				self._BakeLogic(self.locGoalTarget[1], zeroOffsets = True)
			elif (variant == 2):
				self._BakeLogic(self.locGoalTarget[1])
			elif (variant == 3):
				self._BakeLogic(self.locAim[2], translation = False)
			elif (variant == 4):
				self._BakeLogic(self.locGoalTarget[1], zeroOffsets = True, deleteSetupLock = True)
				self._BakeLogic(self.locAim[2], translation = False)
			elif (variant == 5):
				self._BakeLogic(self.locAim[2], translation = False, deleteSetupLock = True)
				self._BakeLogic(self.locGoalTarget[1], zeroOffsets = True)
		
		for i in range(len(selected)):
			cmds.select(selected[i], replace = True)
			self._SetupInit()
			RunBakeLogicVariant()
		
		cmds.select(selected, replace = True)


	### LAYERS
	def _LayerCreate(self, name, *args): # TODO additional naming for translation and rotation
		# Create main layer
		if (not cmds.objExists(OverlappySettings.nameLayers[0])):
			self.layers[0] = Layers.Create(layerName = OverlappySettings.nameLayers[0])
		
		# Create layers on selected
		layerName = Text.ConvertSymbols(name) + "_1"
		return Layers.Create(layerName = layerName, parent = self.layers[0])
	def _LayerMoveToSafeOrTemp(self, safeLayer=True, *args): # TODO rework
		id = [0, 1]
		
		if (not safeLayer):
			id = [1, 0]
		
		layer1 = OverlappySettings.nameLayers[id[0]]
		layer2 = OverlappySettings.nameLayers[id[1]]


		# Check source layer
		if (not cmds.objExists(layer1)):
			cmds.warning("Layer \"{0}\" doesn't exist".format(layer1))
			return
		

		# Get selected layers
		selectedLayers = []
		for animLayer in cmds.ls(type = "animLayer"):
			if cmds.animLayer(animLayer, query = True, selected = True):
				selectedLayers.append(animLayer)
		

		# Check selected count
		children = cmds.animLayer(self.layers[id[0]], query = True, children = True)
		filteredLayers = []
		
		if (len(selectedLayers) == 0):
			if (children == None):
				cmds.warning("Layer \"{0}\" is empty".format(layer1))
				return
			else:
				for layer in children:
					filteredLayers.append(layer)
		else:
			if (children == None):
				cmds.warning("Layer \"{0}\" is empty".format(layer1))
				return
			else:
				for layer1 in children:
					for layer2 in selectedLayers:
						if (layer1 == layer2):
							filteredLayers.append(layer1)
			if (len(filteredLayers) == 0):
				cmds.warning("Nothing to move")
				return
		

		# Create safe layer
		if (not cmds.objExists(layer2)):
			self.layers[id[1]] = cmds.animLayer(layer2, override = True)
		

		# Move children or selected layers
		for layer in filteredLayers:
			cmds.animLayer(layer, edit = True, parent = self.layers[id[1]])
		

		# Delete TEMP layer if no children
		if (len(filteredLayers) == len(children)):
			Layers.Delete(layer1)

