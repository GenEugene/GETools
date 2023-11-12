# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

# import sys, os
# import maya.mel as mel
import maya.cmds as cmds
from math import pow, sqrt
from functools import partial
from utils import UI
from utils import Text
from utils import Colors
from utils import Selector
from utils import Timeline
from modules import GeneralWindow

class OverlappyAnnotations:
	goal_smooth_ann = "You can increase the maximum limit to 10.0 by entering the value manually"
	time_scale_ann = "You can increase the maximum limit to 10.0 by entering the value manually"
	goal_weight_ann = ""
	
	T_reset_ann = 'Reset all translation values'
	R_reset_ann = 'Reset all rotation values'
	CH1_reset_ann = 'Reset options'
	resetAll_ann = 'Reset all values and options in script window'
	
	aim_reverse_ann = \
	'Reorientation aim for rotation simulation. May be useful\
	\nwhen rotation bake animation with incorrect flipped rotations.'
	
	cycle_checkbox_ann = \
	'USE 60+ FPS\
	\n\nStrong recomended to use animation minimum\
	\nwith 1 phase before and after animation cycle.\
	\n\nSimple way to do it just use pre and post infinity\
	\nwith "Cycle" option in graph editor.\
	\n\nAfter baking loop animation on layer will be set cycle infinity'
	
	hierarchyMode_checkbox_ann = \
	'To use it, just select the root objects only.\n\
	\nThe script will find all hierarchies of transforms inside the selected,\
	\nand the simulation will process each chain separately'
	
	delete_ann = 'Delete main layer "OVERLAPPY" with all layers inside'
	
	hierarchy_ann = \
	'Select transforms hierarchy (without shapes)\
	\nIf you use this button, turn off Hierarchy checkbox'
	
	move_ann = \
	'Move all keyed layers from "OVERLAPPY" layer to "SAVED_Overlaps".\
	\n\nDELETE button cant delete saved layers.'
	
	loopFactor_ann = 'WARNING !!! More time will be spent to simulation loops\
	\n\nNeed to increase value, if the first and the last frames dont match well enough'

class OverlappySettings:
	# NAMING
	prefix = "ovlp"
	prefixLayer = "_" + prefix

	nameGroup = prefix + "Group"
	nameLocGoalTarget = (prefix + "LocGoal", prefix + "LocTarget")
	nameLocAim = (prefix + "LocAimBase", prefix + "LocAimHidden", prefix + "LocAim", prefix + "LocAimUp")
	nameParticle = prefix + "Particle"
	nameLoft = (prefix + "LoftStart", prefix + "LoftEnd", prefix + "LoftShape")
	nameLayers = (prefixLayer + "TEMP_", prefixLayer + "SAFE_", prefixLayer + "_", prefixLayer + "Pos_", prefixLayer + "Rot_")
	
	# LOFT
	loftFactor = 0.9
	loftMinDistance = 5
	
	# SIMULATION SETTINGS # TODO: move to preset
	checkboxesOptions = [False, True, False, True]
	particleRadius = 20
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
	
	# CONSTANTS
	attributesT = ("tx", "ty", "tz")
	attributesR = ("rx", "ry", "rz")
	attributesS = ("sx", "sy", "sz")
	constraintsNames = ("parentConstraint", "pointConstraint", "orientConstraint", "scaleConstraint", "aimConstraint")

class Overlappy:
	version = "v2.0.1"
	title = "[UNSTABLE] " + "OVERLAPPY" + " " + version

	def __init__(self):
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
		
		# LAYOUTS
		self.windowMain = None
		self.layoutSetup = None
		self.layoutBaking = None
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
		settings = GeneralWindow.GeneralWindowSettings
		windowWidthMargin = settings.windowWidthMargin
		lineHeight = settings.lineHeight
		sliderWidth = settings.sliderWidth
		sliderWidthMarker = settings.sliderWidthMarker

		self.UILayoutMenuBar(layoutMain, windowWidthMargin)
		self.UILayoutSetup(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutBaking(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutLayers(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutOptions(layoutMain, windowWidthMargin, lineHeight)
		self.UILayoutParticleAttributes(layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker)
		self.UILayoutParticleOffset(layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker)

	def UILayoutMenuBar(self, layoutMain, windowWidthMargin): # TODO
		cmds.columnLayout("layoutMenuBar", parent = layoutMain, adjustableColumn = True, width = windowWidthMargin)
		cmds.menuBarLayout()

		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Reset Settings", command = self._ResetAllValues)

		cmds.menu(label = "Select")
		cmds.menuItem(label = "Object", command = self._SelectObject)
		cmds.menuItem(label = "Particle", command = self._SelectParticle)
		cmds.menuItem(label = "Nucleus", command = self._SelectNucleus)
		cmds.menuItem(label = "Target locator", command = self._SelectTarget)
		cmds.menuItem(label = "Aim locator", command = self._SelectAim)
	def UILayoutSetup(self, layoutMain, windowWidthMargin, lineHeight): # TODO
		self.layoutSetup = cmds.frameLayout("layoutSetup", label = "SETUP", parent = layoutMain, collapsable = True)
		count = 2
		cmds.gridLayout(parent = self.layoutSetup, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)

		cmds.button(label = "SETUP", command = self._SetupInit, backgroundColor = Colors.green10)
		# cmds.button(label = "Scan setup into scene", command = self._SetupScan, backgroundColor = Colors.green10)
		cmds.button(label = "Delete setup", command = self._SetupDelete, backgroundColor = Colors.green10)
	def UILayoutBaking(self, layoutMain, windowWidthMargin, lineHeight): # TODO
		self.layoutBaking = cmds.frameLayout("layoutBaking", label = "BAKING", parent = layoutMain, collapsable = True)
		
		count = 3
		cmds.gridLayout(parent = self.layoutBaking, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)

		cmds.button(label = "TRANSLATION", command = partial(self._BakeVariants, 1), backgroundColor = Colors.orange10)
		cmds.popupMenu()
		cmds.menuItem(label = "use offset", command = partial(self._BakeVariants, 2))
		
		cmds.button(label = "ROTATION", command = partial(self._BakeVariants, 3), backgroundColor = Colors.orange10)
		
		cmds.button(label = "COMBO", command = partial(self._BakeVariants, 4), backgroundColor = Colors.orange10)
		cmds.popupMenu()
		cmds.menuItem(label = "translate + rotate", command = self._BakeVariantComboTR)
		cmds.menuItem(label = "rotate + translate", command = self._BakeVariantComboRT)
	def UILayoutLayers(self, layoutMain, windowWidthMargin, lineHeight):
		self.layoutLayers = cmds.frameLayout("layoutLayers", label = "LAYERS", parent = layoutMain, collapsable = True)
		
		count = 2
		cmds.gridLayout(parent = self.layoutLayers, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		cmds.button(label = "Delete Temp layer", command = partial(self._LayerDelete, OverlappySettings.nameLayers[0]), backgroundColor = Colors.red10)
		cmds.button(label = "Move to Safe layer", command = partial(self._LayerMoveToSafeOrTemp, True), backgroundColor = Colors.blue10)

		count = 1
		cmds.gridLayout(parent = self.layoutLayers, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		cmds.button(label = "Delete BaseAnimation layer", command = partial(self._LayerDelete, "BaseAnimation"), backgroundColor = Colors.red50)
		
		count = 2
		cmds.gridLayout(parent = self.layoutLayers, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		cmds.button(label = "Delete Safe layer", command = partial(self._LayerDelete, OverlappySettings.nameLayers[1]), backgroundColor = Colors.red10)
		cmds.button(label = "Move to Temp layer", command = partial(self._LayerMoveToSafeOrTemp, False), backgroundColor = Colors.blue10)
	def UILayoutOptions(self, layoutMain, windowWidthMargin, lineHeight):
		self.layoutOptions = cmds.frameLayout("layoutOptions", label = "OPTIONS", parent = layoutMain, collapsable = True)
		
		count = 4
		cmds.gridLayout(parent = self.layoutOptions, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		
		# _optionsResetAll = self._ResetOptions # , commandResetAll = _optionsResetAll
		
		self.checkboxHierarchy = UI.Checkbox(label = "Hierarchy", value = OverlappySettings.checkboxesOptions[0], menuReset = True)
		self.checkboxLayer = UI.Checkbox(label = "Layer", value = OverlappySettings.checkboxesOptions[1], menuReset = True)
		self.checkboxLoop = UI.Checkbox(label = "Loop", value = OverlappySettings.checkboxesOptions[2], menuReset = True)
		self.checkboxClean = UI.Checkbox(label = "Clean", value = OverlappySettings.checkboxesOptions[3], menuReset = True)
	def UILayoutParticleAttributes(self, layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker):
		self.layoutSimulation = cmds.frameLayout("layoutParticleSliders", label = "PARTICLE ATTRIBUTES", parent = layoutMain, collapsable = True)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click") # TODO add reset all function

		commandDefault = self._UpdateParticleAttributes

		layoutSliders1 = cmds.gridLayout(parent = self.layoutSimulation, numberOfColumns = 1, cellWidth = windowWidthMargin, cellHeight = lineHeight)
		self.sliderPRadius = UI.Slider(
			parent = layoutSliders1,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "Radius",
			value = OverlappySettings.particleRadius,
			minMax = OverlappySettings.rangePRadius,
			menuReset = True,
		)

		# cmds.separator(parent = self.layoutSimulation, style = "in", height = 1)
		cmds.separator(parent = self.layoutSimulation, style = "in")
		
		layoutSliders2 = cmds.gridLayout(parent = self.layoutSimulation, numberOfColumns = 1, cellWidth = windowWidthMargin, cellHeight = lineHeight)
		self.sliderPConserve = UI.Slider(
			parent = layoutSliders2,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "Conserve",
			value = OverlappySettings.particleConserve,
			minMax = OverlappySettings.rangePConserve,
			menuReset = True,
		)
		
		self.sliderPDrag = UI.Slider(
			parent = layoutSliders2,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "Drag",
			value = OverlappySettings.particleDrag,
			minMax = OverlappySettings.rangePDrag,
			menuReset = True,
		)
		
		self.sliderPDamp = UI.Slider(
			parent = layoutSliders2,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "Damp",
			value = OverlappySettings.particleDamp,
			minMax = OverlappySettings.rangePDamp,
			menuReset = True,
		)
		
		self.sliderGSmooth = UI.Slider(
			parent = layoutSliders2,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "G.Smooth",
			value = OverlappySettings.goalSmooth,
			minMax = OverlappySettings.rangeGSmooth,
			menuReset = True,
		)
		
		self.sliderGWeight = UI.Slider(
			parent = layoutSliders2,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "G.Weight",
			value = OverlappySettings.goalWeight,
			minMax = OverlappySettings.rangeGWeight,
			menuReset = True,
		)
		
		self.sliderNTimeScale = UI.Slider(
			parent = layoutSliders2,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "Time Scale",
			value = OverlappySettings.nucleusTimeScale,
			minMax = OverlappySettings.rangeNTimeScale,
			menuReset = True,
		)
	def UILayoutParticleOffset(self, layoutMain, windowWidthMargin, lineHeight, sliderWidth, sliderWidthMarker):
		self.layoutOffset = cmds.frameLayout("layoutParticleOffset", label = "PARTICLE OFFSET - use for baking rotation", parent = layoutMain, collapsable = True)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click") # TODO add reset all function

		count = 3
		cmds.gridLayout(parent = self.layoutOffset, numberOfColumns = count, cellWidth = windowWidthMargin / count, cellHeight = lineHeight)
		# cmds.separator()
		# , commandResetAll = self._ResetOffsets
		self.checkboxMirrorX = UI.Checkbox(label = "Mirror X", command = partial(self._OffsetsUpdate, True))
		self.checkboxMirrorY = UI.Checkbox(label = "Mirror Y", command = partial(self._OffsetsUpdate, True))
		self.checkboxMirrorZ = UI.Checkbox(label = "Mirror Z", command = partial(self._OffsetsUpdate, True))
		

		layoutSliders = cmds.gridLayout(parent = self.layoutOffset, numberOfColumns = 1, cellWidth = windowWidthMargin, cellHeight = lineHeight)

		commandDefault = self._OffsetsUpdate

		self.sliderOffsetX = UI.Slider(
			parent = layoutSliders,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "   Local X",
			minMax = OverlappySettings.rangeOffsetX,
			menuReset = True,
		)

		self.sliderOffsetY = UI.Slider(
			parent = layoutSliders,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "   Local Y",
			minMax = OverlappySettings.rangeOffsetY,
			menuReset = True,
		)

		self.sliderOffsetZ = UI.Slider(
			parent = layoutSliders,
			widthWindow = windowWidthMargin,
			widthMarker = sliderWidthMarker,
			columnWidth3 = sliderWidth,
			command = commandDefault,
			label = "   Local Z",
			minMax = OverlappySettings.rangeOffsetZ,
			menuReset = True,
		)


	@staticmethod
	def BakeSelected(doNotCut = True): # TODO from GETools class (need to merge in future)
		_startTime = cmds.playbackOptions(query = True, min = True)
		_endTime = cmds.playbackOptions(query = True, max = True)
		cmds.bakeResults(t = (_startTime, _endTime), preserveOutsideKeys = doNotCut, simulation = True)

	### LOGIC
	def _SetupInit(self, *args): # TODO rework
		self._SetupDelete(False)
		
		# Get selected objects
		self.selectedObject = cmds.ls(selection = True)
		if (len(self.selectedObject) == 0):
			cmds.warning("You must select at least 1 object")
			self.selectedObject = ""
			return
		self.selectedObject = self.selectedObject[0]

		# Get min/max anim range time and reset time slider
		self.time.Scan()
		self.time.SetCurrent(self.time.values[2])

		# Create group
		cmds.select(clear = True)
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		cmds.group(empty = True, name = OverlappySettings.nameGroup)
		
		# Run setup logic
		self._SetupCreate(self.selectedObject)
		self._OffsetsUpdate(cacheReset = True)
		cmds.select(self.selectedObject, replace = True)
	def _SetupCreate(self, objCurrent, *args): # TODO rework
		# Names
		_objConverted = Text.ConvertSymbols(objCurrent)
		nameLocGoal = OverlappySettings.nameLocGoalTarget[0] + _objConverted
		nameLocParticle = OverlappySettings.nameLocGoalTarget[1] + _objConverted
		nameParticle = OverlappySettings.nameParticle + _objConverted
		nameLocAimBase = OverlappySettings.nameLocAim[0] + _objConverted
		nameLocAimHidden = OverlappySettings.nameLocAim[1] + _objConverted
		nameLocAim = OverlappySettings.nameLocAim[2] + _objConverted
		nameLocAimUp = OverlappySettings.nameLocAim[3] + _objConverted
		nameLoftStart = OverlappySettings.nameLoft[0] + _objConverted
		nameLoftEnd = OverlappySettings.nameLoft[1] + _objConverted
		nameLoftShape = OverlappySettings.nameLoft[2] + _objConverted

		# Create locator for goal
		self.locGoalTarget[0] = cmds.spaceLocator(name = nameLocGoal)[0]
		cmds.parent(self.locGoalTarget[0], OverlappySettings.nameGroup)
		cmds.matchTransform(self.locGoalTarget[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.locGoalTarget[0], maintainOffset = True)
		cmds.setAttr(self.locGoalTarget[0] + ".visibility", 0)
		self.startPositionGoalParticle[0] = cmds.xform(self.locGoalTarget[0], query = True, translation = True)

		# Create particle, goal and get selected object position
		_position = cmds.xform(objCurrent, query = True, worldSpace = True, rotatePivot = True)
		self.particle = cmds.nParticle(name = nameParticle, position = _position, conserve = 1)[0]
		cmds.goal(useTransformAsGoal = True, goal = self.locGoalTarget[0])
		cmds.parent(self.particle, OverlappySettings.nameGroup)
		# self.startPositionGoalParticle[1] = cmds.xform(self.particle, query = True, translation = True)
		cmds.setAttr(self.particle + ".overrideEnabled", 1)
		cmds.setAttr(self.particle + ".overrideDisplayType", 2)

		# Set simulation attributes
		cmds.setAttr(self.particle + "Shape.radius", self.sliderPRadius.Get())
		cmds.setAttr(self.particle + "Shape.solverDisplay", 1)
		cmds.setAttr(self.particle + "Shape.conserve", self.sliderPConserve.Get())
		cmds.setAttr(self.particle + "Shape.drag", self.sliderPDrag.Get())
		cmds.setAttr(self.particle + "Shape.damp", self.sliderPDamp.Get())
		cmds.setAttr(self.particle + "Shape.goalSmoothness", self.sliderGSmooth.Get())
		cmds.setAttr(self.particle + "Shape.goalWeight[0]", self.sliderGWeight.Get())

		# Nucleus detection
		self.nucleus = cmds.ls(type = "nucleus")[0]
		cmds.parent(self.nucleus, OverlappySettings.nameGroup)
		# self.sliderNTimeScale.startName = self.nucleus
		cmds.setAttr(self.nucleus + ".gravity", 0)
		cmds.setAttr(self.nucleus + ".timeScale", self.sliderNTimeScale.Get())
		cmds.setAttr(self.nucleus + ".startFrame", self.time.values[2])
		cmds.setAttr(self.nucleus + ".visibility", 0)

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
		self.loft[0] = cmds.circle(name = nameLoftStart, degree = 1, sections = 4, normal = [0, 1, 0])[0]
		self.loft[1] = cmds.duplicate(self.loft[0], name = nameLoftEnd)[0]
		_scale1 = 0.001
		_scale2 = self.sliderPRadius.Get() * OverlappySettings.loftFactor
		cmds.setAttr(self.loft[0] + ".scaleX", _scale1)
		cmds.setAttr(self.loft[0] + ".scaleY", _scale1)
		cmds.setAttr(self.loft[0] + ".scaleZ", _scale1)
		cmds.setAttr(self.loft[1] + ".scaleX", _scale2)
		cmds.setAttr(self.loft[1] + ".scaleY", _scale2)
		cmds.setAttr(self.loft[1] + ".scaleZ", _scale2)
		cmds.setAttr(self.loft[0] + ".visibility", 0)
		cmds.setAttr(self.loft[1] + ".visibility", 0)
		#
		cmds.matchTransform(self.loft[0], self.locAim[2], position = True, rotation = True)
		cmds.parent(self.loft[0], self.locAim[2])
		cmds.matchTransform(self.loft[1], self.locGoalTarget[1], position = True)
		cmds.parent(self.loft[1], self.locGoalTarget[1])
		cmds.aimConstraint(self.loft[0], self.loft[1], weight = 1, aimVector = (0, 1, 0), upVector = (0, 1, 0), worldUpType = "vector", worldUpVector = (0, 0, 1))
		#
		self.loft[2] = cmds.loft(self.loft[0], self.loft[1], name = nameLoftShape, reverseSurfaceNormals = 0, uniform = 1, polygon = 0)[0]
		cmds.parent(self.loft[2], OverlappySettings.nameGroup)
		cmds.setAttr(self.loft[2] + ".overrideEnabled", 1)
		cmds.setAttr(self.loft[2] + ".overrideDisplayType", 2)
		cmds.setAttr(self.loft[2] + ".overrideShading", 0)
		if (self._LoftGetDistance() < OverlappySettings.loftMinDistance):
			cmds.setAttr(self.loft[2] + ".visibility", 0)
	def _SetupScan(self, *args): # TODO rework
		# Check overlappy group
		if (not cmds.objExists(OverlappySettings.nameGroup)):
			cmds.warning("Overlappy object doesn't exists")
			return
		
		# Get children of group
		_children = cmds.listRelatives(OverlappySettings.nameGroup)
		if (len(_children) == 0):
			cmds.warning("Overlappy object has no children objects")
			return
		
		# Try to get suffix name
		_tempList = [OverlappySettings.nameLocGoalTarget[0], OverlappySettings.nameLocGoalTarget[1], OverlappySettings.nameParticle, OverlappySettings.nameLocAim[0], OverlappySettings.nameLoft[2]]
		_objectName = ""
		for child in _children:
			for item in _tempList:
				_splitNames = child.split(item)
				if (len(_splitNames) < 2): continue
				_lastName = _splitNames[-1]
				if (_objectName == ""):
					_objectName = _lastName
				else:
					if (_objectName == _lastName): continue
					else: cmds.warning("Suffix '{0}' don't equals to '{1}'".format(_objectName, _lastName))
		_converted = Text.ConvertSymbols(_objectName, False)
		if (cmds.objExists(_converted)):
			self.selectedObject = _converted
		
		def CheckAndSet(name):
			if (cmds.objExists(name + _objectName)):
				return name + _objectName
			else: return
		
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
		self.TimeRangeScan()
		self.TimeRangeSetCurrent(self.timeRange[2])
		self.startPositionGoalParticle[0] = cmds.xform(self.locAim[0], query = True, translation = True)
		self.TimeRangeSetCurrentCached()
		
		# Nucleus
		_nucleus = cmds.ls(type = "nucleus")
		if (len(_nucleus) > 0):
			self.nucleus = _nucleus[0]
			# self.sliderNTimeScale.startName = self.nucleus
		
		# Get sliders
		# self.sliderPRadius.Scan()
		# self._GetSimulation()
		# self._GetOffsets()
		pass
	def _SetupDelete(self, deselect = True, *args): # TODO rework
		self.selectedObject = ""
		self.locGoalTarget = ["", ""]
		self.locAim = ["", "", "", ""]
		self.particle = ""
		self.nucleus = ""
		self.loft = ["", "", ""]
		
		# Delete group
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		
		# Delete nucleus node
		_nucleus = cmds.ls(type = "nucleus")
		if (len(_nucleus) > 0):
			cmds.delete(_nucleus)
		if (deselect):
			cmds.select(clear = True)
	def _OffsetsUpdate(self, cacheReset = False, *args): # TODO rework
		if (type(cacheReset) is float):
			cacheReset = False
		if (cacheReset):
			self.sliderOffsetX.ResetCached()
			self.sliderOffsetY.ResetCached()
			self.sliderOffsetZ.ResetCached()
		
		# Check and set cached value
		_checkX = self.sliderOffsetX.GetCached() != self.sliderOffsetX.Get()
		_checkY = self.sliderOffsetY.GetCached() != self.sliderOffsetY.Get()
		_checkZ = self.sliderOffsetZ.GetCached() != self.sliderOffsetZ.Get()
		if (_checkX or _checkY or _checkZ):
			self.sliderOffsetX.SetCached()
			self.sliderOffsetY.SetCached()
			self.sliderOffsetZ.SetCached()
		else:
			return

		self._ValuesSetParticleOffset()

		_checkSelected = self.selectedObject == "" or not cmds.objExists(self.selectedObject)
		_checkGoal = not cmds.objExists(self.locGoalTarget[0])
		_checkAim = not cmds.objExists(self.locAim[2])
		_checkStartPos = self.startPositionGoalParticle[0] == None
		
		if (_checkSelected or _checkGoal or _checkAim or _checkStartPos):
			return

		cmds.currentTime(self.time.values[2])

		# Mirrors
		_mirror = [1, 1, 1]
		if (self.checkboxMirrorX.Get()): _mirror[0] = -1
		if (self.checkboxMirrorY.Get()): _mirror[1] = -1
		if (self.checkboxMirrorZ.Get()): _mirror[2] = -1
		
		# Get values from sliders
		_values = [0, 0, 0]
		_values[0] = self.sliderOffsetX.Get() * _mirror[0]
		_values[1] = self.sliderOffsetY.Get() * _mirror[1]
		_values[2] = self.sliderOffsetZ.Get() * _mirror[2]
		
		# Set locGoal constraint offset
		_goalAttributes = [0, 0, 0]
		_goalAttributes[0] = self.locGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateX"
		_goalAttributes[1] = self.locGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateY"
		_goalAttributes[2] = self.locGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateZ"
		cmds.setAttr(_goalAttributes[0], _values[0])
		cmds.setAttr(_goalAttributes[1], _values[1])
		cmds.setAttr(_goalAttributes[2], _values[2])
		
		# Get offset
		_goalPosition = cmds.xform(self.locGoalTarget[0], query = True, translation = True)
		_goalOffset = [0, 0, 0]
		_goalOffset[0] = self.startPositionGoalParticle[0][0] - _goalPosition[0]
		_goalOffset[1] = self.startPositionGoalParticle[0][1] - _goalPosition[1]
		_goalOffset[2] = self.startPositionGoalParticle[0][2] - _goalPosition[2]
		
		# Set particle attributes
		_particleAttributes = [0, 0, 0]
		_particleAttributes[0] = OverlappySettings.nameParticle + Text.ConvertSymbols(self.selectedObject) + ".translateX"
		_particleAttributes[1] = OverlappySettings.nameParticle + Text.ConvertSymbols(self.selectedObject) + ".translateY"
		_particleAttributes[2] = OverlappySettings.nameParticle + Text.ConvertSymbols(self.selectedObject) + ".translateZ"
		cmds.setAttr(_particleAttributes[0], self.startPositionGoalParticle[1][0] - _goalOffset[0])
		cmds.setAttr(_particleAttributes[1], self.startPositionGoalParticle[1][1] - _goalOffset[1])
		cmds.setAttr(_particleAttributes[2], self.startPositionGoalParticle[1][2] - _goalOffset[2])
		
		# Reposition aim up locator and reconstrain aim
		_selected = cmds.ls(selection = True)
		cmds.delete(self.locAim[1] + "_aimConstraint1")
		cmds.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		cmds.delete(self.locAim[1] + "_aimConstraint1")
		cmds.parent(self.locAim[3], self.locAim[1])
		cmds.setAttr(self.locAim[3] + ".tx", 0)
		cmds.setAttr(self.locAim[3] + ".ty", 100)
		cmds.setAttr(self.locAim[3] + ".tz", 0)
		cmds.parent(self.locAim[3], self.locAim[0])
		cmds.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.locAim[3])
		cmds.select(_selected, replace = True)
		
		# Reconstrain aim locator to hidden aim
		cmds.setAttr(self.locAim[2] + ".rotateX", 0)
		cmds.setAttr(self.locAim[2] + ".rotateY", 0)
		cmds.setAttr(self.locAim[2] + ".rotateZ", 0)
		cmds.orientConstraint(self.locAim[1], self.locAim[2], maintainOffset = True)

	### SELECT
	def _Select(self, name = "", *args):
		if (name != ""):
			if (cmds.objExists(name)):
				cmds.select(name, replace = True)
			else:
				cmds.warning("\"{0}\" object doesn't exists".format(name))
		else:
			cmds.warning("Can't select 'None'")
	def _SelectObject(self, *args):
		if (self.selectedObject == ""):
			self._Select()
		else:
			self._Select(self.selectedObject)
	def _SelectParticle(self, *args):
		self._Select(self.particle)
	def _SelectNucleus(self, *args):
		self._Select(self.nucleus)
	def _SelectTarget(self, *args):
		self._Select(self.locGoalTarget[1])
	def _SelectAim(self, *args):
		self._Select(self.locAim[2])

	### VALUES
	def _SetParticleAttribute(self, sliderValue, startName, attributeName, addSelectedName, *args):
		_selectedName = self.selectedObject
		if (_selectedName == ""):
			return
		
		# Add selected name or not
		_selectedName = Text.ConvertSymbols(_selectedName)
		if (addSelectedName):
			resultName = startName + _selectedName + attributeName
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
		_scale = self.sliderPRadius.Get() * OverlappySettings.loftFactor
		cmds.setAttr(self.loft[1] + ".scaleX", _scale)
		cmds.setAttr(self.loft[1] + ".scaleY", _scale)
		cmds.setAttr(self.loft[1] + ".scaleZ", _scale)
		if (self._LoftGetDistance() < OverlappySettings.loftMinDistance):
			cmds.setAttr(self.loft[2] + ".visibility", 0)
		else:
			cmds.setAttr(self.loft[2] + ".visibility", 1)
	def _LoftGetDistance(self, *args):
		_vector = [0, 0, 0]
		_vector[0] = self.sliderOffsetX.Get()
		_vector[1] = self.sliderOffsetY.Get()
		_vector[2] = self.sliderOffsetZ.Get()
		return sqrt(pow(_vector[0], 2) + pow(_vector[1], 2) + pow(_vector[2], 2)) # Distance formula : V((x2 - x1)2 + (y2 - y1)2 + (z2 - z1)2)

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
	def _ResetSimulation(self, full = False, *args):
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
	def _BakeLogic(self, parent, zeroOffsets = False, translation = True, deleteSetupLock = False, *args):
		# Filter attributes
		_item = self.selectedObject
		if (translation): _attributesType = OverlappySettings.attributesT
		else: _attributesType = OverlappySettings.attributesR
		_attrs = ["", "", ""]
		for i in range(len(_attrs)):
			_attrs[i] = "{0}.{1}".format(_item, _attributesType[i])
		_attributesFiltered = []
		for i in range(len(_attrs)):
			_keyed = cmds.keyframe(_attrs[i], query = True)
			if(_keyed):
				_muted = cmds.mute(_attrs[i], query = True)
				if(_muted):
					continue
			_locked = cmds.getAttr(_attrs[i], lock = True)
			_keyable = cmds.getAttr(_attrs[i], keyable = True)
			_settable = cmds.getAttr(_attrs[i], settable = True)
			_constrained = False
			_connections = cmds.listConnections(_attrs[i])
			if(_connections):
				for item in _connections:
					_type = cmds.nodeType(item)
					if(_type in OverlappySettings.constraintsNames):
						_constrained = True
			if(not _locked and _keyable and _settable and not _constrained):
				_attributesFiltered.append(_attributesType[i])
		if(len(_attributesFiltered) == 0):
			cmds.warning("No attributes")
			self._SetupDelete()
			return
		
		# Keyframe target attributes
		cmds.setKeyframe(_item, attribute = _attributesFiltered)

		# Zero offsets
		if (zeroOffsets):
			_value1 = self.sliderOffsetX.Get()
			_value2 = self.sliderOffsetY.Get()
			_value3 = self.sliderOffsetZ.Get()
			self.sliderOffsetX.Reset()
			self.sliderOffsetY.Reset()
			self.sliderOffsetZ.Reset()
		
		# Set time range
		self.TimeRangeScan()
		_startTime = self.timeRange[2]
		if (self.checkboxLoop.Get()):
			_startTime = self.timeRange[2] - self.timeRange[3] * self.loopOffset
			self.TimeRangeSetMin(_startTime)
			self.TimeRangeSetCurrent(_startTime)
		cmds.setAttr(self.nucleus + ".startFrame", _startTime) # TODO bug when select ovlp objects
		
		# Start logic
		_name = "_rebake_" + Text.ConvertSymbols(_item)
		_clone = cmds.duplicate(_item, name = _name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		for attr in OverlappySettings.attributesT:
			cmds.setAttr(_clone[0] + "." + attr, lock = False)
		for attr in OverlappySettings.attributesR:
			cmds.setAttr(_clone[0] + "." + attr, lock = False)
		cmds.parentConstraint(parent, _clone, maintainOffset = True) # skipTranslate
		cmds.select(_clone, replace = True)
		
		# Bake
		OverlappySettings.BakeSelected()
		_children = cmds.listRelatives(_clone, type = "constraint")
		for child in _children: cmds.delete(child)
		
		# Copy keys, check layer and paste keys
		cmds.copyKey(_clone, time = (self.timeRange[2], self.timeRange[3]), attribute = _attributesFiltered)
		if (self.checkboxLayer.Get()):
			_animLayer = self._LayerCreate(_item)
			_attrsLayer = []
			for item in _attributesFiltered:
				_attrsLayer.append("{0}.{1}".format(_item, item))
			cmds.animLayer(_animLayer, edit = True, attribute = _attrsLayer)
			cmds.pasteKey(_item, option = "replace", attribute = _attributesFiltered, animLayer = _animLayer)
		else:
			cmds.pasteKey(_item, option = "replaceCompletely", attribute = _attributesFiltered)
		cmds.delete(_clone)
		
		# Set time range
		if (self.checkboxLoop.Get()):
			_startTime = self.timeRange[2]
			cmds.setAttr(self.nucleus + ".startFrame", _startTime)
			self.TimeRangeReset()
			# Timeline.
			cmds.setInfinity(_item, preInfinite = "cycle", postInfinite = "cycle")
		else:
			cmds.setInfinity(_item, preInfinite = "constant", postInfinite = "constant")
		
		# Delete setup
		if (self.checkboxClean.Get()):
			if (not deleteSetupLock):
				self._SetupDelete()
		
		# Restore offsets sliders
		if (zeroOffsets):
			self.sliderOffsetX.Set(_value1)
			self.sliderOffsetY.Set(_value2)
			self.sliderOffsetZ.Set(_value3)
			self._OffsetsUpdate(True)
	def _BakeCheck(self, *args):
		_selected = cmds.ls(selection = True) # type = "transform"
		if (len(_selected) == 0):
			if (self.selectedObject == ""): return None
			return 0, None
		else:
			if (self.checkboxHierarchy.Get()):
				Selector.SelectTransformHierarchy()
				_selected = cmds.ls(selection = True)
			return len(_selected), _selected
	def _BakeVariants(self, variant, *args):
		_selected = self._BakeCheck()
		if (_selected == None): return

		if (_selected[0] == 0):
			if (variant == 1):
				self._BakeLogic(self.locGoalTarget[1], True, True, False)
			elif (variant == 2):
				self._BakeLogic(self.locGoalTarget[1], False, True, False)
			elif (variant == 3):
				self._BakeLogic(self.locAim[2], False, False, False)
			elif (variant == 4):
				self._BakeLogic(self.locGoalTarget[1], True, True, True)
				self._BakeLogic(self.locAim[2], False, False, False)
		else:
			for ii in range(_selected[0]):
				cmds.select(_selected[1][ii], replace = True)
				self._SetupInit()
				if (variant == 1):
					self._BakeLogic(self.locGoalTarget[1], True, True, False)
				elif (variant == 2):
					self._BakeLogic(self.locGoalTarget[1], False, True, False)
				elif (variant == 3):
					self._BakeLogic(self.locAim[2], False, False, False)
				elif (variant == 4):
					self._BakeLogic(self.locGoalTarget[1], True, True, True)
					self._BakeLogic(self.locAim[2], False, False, False)
			cmds.select(_selected[1], replace = True)
	def _BakeVariantComboTR(self, *args):
		self._BakeVariants(1)
		self._BakeVariants(3)
	def _BakeVariantComboRT(self, *args):
		self._BakeVariants(3)
		self._BakeVariants(1)
	
	### LAYERS
	def _LayerCreate(self, obj, *args):
		# Create main layer
		if(not cmds.objExists(OverlappySettings.nameLayers[0])):
			self.layers[0] = cmds.animLayer(OverlappySettings.nameLayers[0], override = True)
		
		# Create layers on selected
		_name = OverlappySettings.nameLayers[2] + Text.ConvertSymbols(obj) + "_1"
		return cmds.animLayer(_name, override = True, parent = self.layers[0])
	def _LayerMoveToSafeOrTemp(self, safeLayer = True, *args):
		_id = [0, 1]
		if (not safeLayer): _id = [1, 0]
		_layer1 = OverlappySettings.nameLayers[_id[0]]
		_layer2 = OverlappySettings.nameLayers[_id[1]]

		# Check source layer
		if(not cmds.objExists(_layer1)):
			cmds.warning("Layer \"{0}\" doesn't exist".format(_layer1))
			return
		
		# Get selected layers
		_selectedLayers = []
		for animLayer in cmds.ls(type = "animLayer"):
			if cmds.animLayer(animLayer, query = True, selected = True):
				_selectedLayers.append(animLayer)
		
		# Check selected count
		_children = cmds.animLayer(self.layers[_id[0]], query = True, children = True)
		_filteredLayers = []
		if (len(_selectedLayers) == 0):
			if (_children == None):
				cmds.warning("Layer \"{0}\" is empty".format(_layer1))
				return
			else:
				for layer in _children:
					_filteredLayers.append(layer)
		else:
			if (_children == None):
				cmds.warning("Layer \"{0}\" is empty".format(_layer1))
				return
			else:
				for layer1 in _children:
					for layer2 in _selectedLayers:
						if (layer1 == layer2):
							_filteredLayers.append(layer1)
			if (len(_filteredLayers) == 0):
				cmds.warning("Nothing to move")
				return
		
		# Create safe layer
		if(not cmds.objExists(_layer2)):
			self.layers[_id[1]] = cmds.animLayer(_layer2, override = True)
		
		# Move children or selected layers
		for layer in _filteredLayers:
			cmds.animLayer(layer, edit = True, parent = self.layers[_id[1]])
		
		# Delete TEMP layer if no children
		if (len(_filteredLayers) == len(_children)):
			self._LayerDelete(_layer1)
	def _LayerDelete(self, name, *args):
		if(cmds.objExists(name)):
			cmds.delete(name)
			print("Layer \"{0}\" deleted".format(name))
		else:
			cmds.warning("Layer \"{0}\" doesn't exist".format(name))
	def _LayerCreate_TEST(self, *args):
		# Check selected
		_selected = cmds.ls(selection = True)
		if (len(_selected) == 0):
			cmds.warning("You must select at least 1 object")
			return
		
		# Create main layer
		if(not cmds.objExists(OverlappySettings.nameLayers[0])):
			self.layers[0] = cmds.animLayer(OverlappySettings.nameLayers[0], override = True)
		
		# Create layers on selected
		for item in _selected:
			_name = OverlappySettings.nameLayers[2] + Text.ConvertSymbols(item) + "_1"
			cmds.animLayer(_name, override = True, parent = self.layers[0])

