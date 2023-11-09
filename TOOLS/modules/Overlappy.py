# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

# import maya.mel as mel
# import sys, os
import maya.cmds as cmds
from math import pow, sqrt
from functools import partial
from utils import UI
from utils import Colors
from utils import Text
from utils import Selector
from modules import GeneralWindow

class Overlappy:
	version = "v2.0.1"
	title = "OVERLAPPY" + " " + version

	# NAMING
	nameGroup = "_OverlappyGroup_"
	nameLocGoalTarget = ("_locGoal_", "_locTarget_")
	nameLocAim = ("_locAimBase_", "_locAimHidden_", "_locAim_", "_locAimUp_")
	nameParticle = "_particle_"
	nameLoft = ("_loftStart_", "_loftEnd_", "_loftShape_")
	nameLayers = ("_OVLP_BASE_", "_OVLP_SAFE_", "OVLP_", "OVLPpos_", "OVLProt_")
	nameBakedWorldLocator = "BakedWorldLocator_"
	
	# WINDOW
	sliderWidth = (60, 60, 10)
	markerWidth = 6
	
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
	rangePRadius = (0, float("inf"), 0, 50)
	rangePConserve = (0, 1, 0, 1)
	rangePDrag = (0, 10, 0, 1)
	rangePDamp = (0, 10, 0, 1)
	rangeGSmooth = (0, 100, 0, 10)
	rangeGWeight = (0, 1, 0, 1)
	rangeNTimeScale = (0.001, 100, 0.001, 4)
	rangeOffsetX = (float("-inf"), float("inf"), 0, 300)
	rangeOffsetY = (float("-inf"), float("inf"), 0, 300)
	rangeOffsetZ = (float("-inf"), float("inf"), 0, 300)
	
	# CONSTANTS
	attributesT = ("tx", "ty", "tz")
	attributesR = ("rx", "ry", "rz")
	attributesS = ("sx", "sy", "sz")
	constraintsNames = ("parentConstraint", "pointConstraint", "orientConstraint", "scaleConstraint", "aimConstraint")

	### MAIN
	def __init__(self):
		# VALUES
		self.time = [0, 0, 0, 0, 0] # current, minS, min, max, maxE
		self.startPositionGoalParticle = [None, (0, 0, 0)]
		
		# OBJECTS
		self.selected = ""
		self.locGoalTarget = ["", ""]
		self.locAim = ["", "", "", ""]
		self.particle = ""
		self.nucleus = ""
		self.loft = ["", "", ""]
		self.layers = ["", ""]
		
		# LAYOUTS
		self.windowMain = None
		# self.layoutMain = None
		# self.layoutButtons = None
		# self.layoutBaking = None
		# self.layoutOptions = None
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
	def UILayout(self, layoutMain): # TODO
		settings = GeneralWindow.GeneralWindow()
		windowWidthMargin = settings.windowWidthMargin


		# BUTTONS
		cmds.frameLayout(label = "BUTTONS", parent = layoutMain, collapsable = True, backgroundColor = Colors.blackWhite10)
		#
		count = 4
		cmds.gridLayout(numberOfColumns = count, cellWidth = windowWidthMargin / count)
		cmds.button(label = "RESET ALL", command = self._ResetAllValues, backgroundColor = Colors.yellow10)
		cmds.button(label = "SELECT", command = self.SelectTransformHierarchy, backgroundColor = Colors.lightBlue10)
		cmds.popupMenu()
		cmds.menuItem(dividerLabel = "Created objects", divider = True)
		cmds.menuItem(label = "Objects", command = self._SelectObjects)
		cmds.menuItem(label = "Particle", command = self._SelectParticle)
		cmds.menuItem(label = "Nucleus", command = self._SelectNucleus)
		cmds.menuItem(label = "Target", command = self._SelectTarget)
		cmds.menuItem(label = "Aim", command = self._SelectAim)
		cmds.button(label = "LAYERS", command = partial(self._LayerMoveToSafeOrBase, True), backgroundColor = Colors.blue10) # _LayerCreate_TEST - old func for tests
		cmds.popupMenu()
		cmds.menuItem(dividerLabel = "Move", divider = True)
		cmds.menuItem(label = "Move to Base layer", command = partial(self._LayerMoveToSafeOrBase, False))
		cmds.menuItem(dividerLabel = "Delete", divider = True)
		cmds.menuItem(label = "Delete '{0}'".format(Overlappy.nameLayers[0]), command = partial(self._LayerDelete, Overlappy.nameLayers[0]))
		cmds.menuItem(label = "Delete '{0}'".format(Overlappy.nameLayers[1]), command = partial(self._LayerDelete, Overlappy.nameLayers[1]))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Delete 'BaseAnimation'", command = partial(self._LayerDelete, "BaseAnimation"))
		cmds.button(label = "SETUP", command = self._SetupInit, backgroundColor = Colors.green10)
		cmds.popupMenu()
		cmds.menuItem(label = "Scan setup into scene", command = self._SetupScan)
		cmds.menuItem(dividerLabel = "Delete", divider = True)
		cmds.menuItem(label = "Delete setup", command = self._SetupDelete)
		

		# BAKING
		cmds.button(label = "TRANSLATION", command = partial(self._BakeVariants, 1), backgroundColor = Colors.orange10)
		cmds.popupMenu()
		cmds.menuItem(label = "use offset", command = partial(self._BakeVariants, 2))
		cmds.button(label = "ROTATION", command = partial(self._BakeVariants, 3), backgroundColor = Colors.orange10)
		cmds.button(label = "COMBO", command = partial(self._BakeVariants, 4), backgroundColor = Colors.orange10)
		cmds.popupMenu()
		cmds.menuItem(label = "translate + rotate", command = self._BakeVariantComboTR)
		cmds.menuItem(label = "rotate + translate", command = self._BakeVariantComboRT)
		cmds.button(label = "TO LOCATOR", command = self._BakeWorldLocator, backgroundColor = Colors.orange10)


		# OPTIONS
		_optionsResetAll = self._ResetOptions
		self.checkboxHierarchy = UI.Checkbox(label = "HIERARCHY", value = Overlappy.checkboxesOptions[0], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxLayer = UI.Checkbox(label = "LAYER", value = Overlappy.checkboxesOptions[1], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxLoop = UI.Checkbox(label = "LOOP", value = Overlappy.checkboxesOptions[2], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxClean = UI.Checkbox(label = "CLEAN", value = Overlappy.checkboxesOptions[3], menuReset = True, ccResetAll = _optionsResetAll)


		# # SIMULATION SETTINGS
		# self.layoutSimulation = cmds.frameLayout(label = "SIMULATION", parent = layoutMain, collapsable = True, backgroundColor = Colors.blackWhite10)
		# cmds.columnLayout(parent = self.layoutSimulation)
		# _simStartName = Overlappy.nameParticle
		# _simParent = self.layoutSimulation
		# _simCCDefault = self._ValuesSetSimulation
		# _simCCReset = partial(self._ResetSimulation, True)
		# _simCCGetValues = self._GetSimulation
		# self.sliderPRadius = UI.Slider(label = "Radius", attribute = "Shape.radius", startName = _simStartName, nameAdd = True, value = Overlappy.particleRadius, minMax = Overlappy.rangePRadius, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		# self.sliderPConserve = UI.Slider(label = "Conserve", attribute = "Shape.conserve", startName = _simStartName, nameAdd = True, value = Overlappy.particleConserve, minMax = Overlappy.rangePConserve, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		# self.sliderPDrag = UI.Slider(label = "Drag", attribute = "Shape.drag", startName = _simStartName, nameAdd = True, value = Overlappy.particleDrag, minMax = Overlappy.rangePDrag, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		# self.sliderPDamp = UI.Slider(label = "Damp", attribute = "Shape.damp", startName = _simStartName, nameAdd = True, value = Overlappy.particleDamp, minMax = Overlappy.rangePDamp, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		# self.sliderGSmooth = UI.Slider(label = "G.Smooth", attribute = "Shape.goalSmoothness", startName = _simStartName, nameAdd = True, value = Overlappy.goalSmooth, minMax = Overlappy.rangeGSmooth, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		# self.sliderGWeight = UI.Slider(label = "G.Weight", attribute = "Shape.goalWeight[0]", startName = _simStartName, nameAdd = True, value = Overlappy.goalWeight, minMax = Overlappy.rangeGWeight, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		# self.sliderNTimeScale = UI.Slider(label = "Time Scale", attribute = ".timeScale", startName = self.nucleus, nameAdd = False, value = Overlappy.nucleusTimeScale, minMax = Overlappy.rangeNTimeScale, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		

		# # OFFSET SETTINGS
		# self.layoutOffset = cmds.frameLayout(label = "OFFSET", parent = layoutMain, collapsable = True, backgroundColor = Colors.blackWhite10)
		# cmds.gridLayout(numberOfColumns = 4, cellWidthHeight = (Overlappy.windowWidth / 4, Overlappy.lineHeight))
		# cmds.separator()
		# self.checkboxMirrorX = UI.Checkbox(label = "MIRROR X", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		# self.checkboxMirrorY = UI.Checkbox(label = "MIRROR Y", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		# self.checkboxMirrorZ = UI.Checkbox(label = "MIRROR Z", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		# cmds.columnLayout(parent = self.layoutOffset)
		# _offStartName = Overlappy.nameLocGoalTarget[0]
		# _offParent = self.layoutOffset
		# _offCCDefault = self._OffsetsUpdate
		# _offCCReset = self._ResetOffsets
		# _offCCGetValues = self._GetOffsets
		# self.sliderOffsetX = UI.Slider(label = "   Local X", attribute = "_parentConstraint1.target[0].targetOffsetTranslateX", startName = _offStartName, minMax = Overlappy.rangeOffsetX, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
		# self.sliderOffsetY = UI.Slider(label = "   Local Y", attribute = "_parentConstraint1.target[0].targetOffsetTranslateY", startName = _offStartName, minMax = Overlappy.rangeOffsetY, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
		# self.sliderOffsetZ = UI.Slider(label = "   Local Z", attribute = "_parentConstraint1.target[0].targetOffsetTranslateZ", startName = _offStartName, minMax = Overlappy.rangeOffsetZ, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
	
	def TimeRangeScan(self, *args): ### DEPRECATED # TODO to external class
		self.time[0] = cmds.currentTime(query = True)
		self.time[1] = cmds.playbackOptions(query = True, animationStartTime = True)
		self.time[2] = cmds.playbackOptions(query = True, min = True)
		self.time[3] = cmds.playbackOptions(query = True, max = True)
		self.time[4] = cmds.playbackOptions(query = True, animationEndTime = True)
	def TimeRangeSetCurrent(self, value, *args):
		cmds.currentTime(value)
	def TimeRangeSetCurrentCached(self, *args):
		cmds.currentTime(self.time[0])
	def TimeRangeSetMin(self, value, *args):
		cmds.playbackOptions(edit = True, min = value)
	def TimeRangeReset(self, *args):
		cmds.playbackOptions(edit = True, animationStartTime = self.time[1], min = self.time[2], max = self.time[3], animationEndTime = self.time[4])
		cmds.currentTime(self.time[2])

	def SelectTransformHierarchy(self, *args):
		selected = Selector.MultipleObjects(minimalCount = 1)
		if (selected == None):
			return
		Selector.SelectTransformHierarchy()

	@staticmethod
	def BakeSelected(doNotCut=True): # TODO from GETools class (need to merge in future)
		_startTime = cmds.playbackOptions(query = True, min = True)
		_endTime = cmds.playbackOptions(query = True, max = True)
		cmds.bakeResults(t = (_startTime, _endTime), preserveOutsideKeys = doNotCut, simulation = True)

	### LOGIC
	def _SetupInit(self, *args):
		self._SetupDelete(False)
		# Get selected objects
		self.selected = cmds.ls(selection = True)
		if (len(self.selected) == 0):
			cmds.warning("You must select at least 1 object")
			self.selected = ""
			return
		self.selected = self.selected[0]
		# Get min/max anim range time and reset time slider
		self.TimeRangeScan()
		self.TimeRangeSetCurrent(self.time[2])
		# Create group
		cmds.select(clear = True)
		if (cmds.objExists(Overlappy.nameGroup)):
			cmds.delete(Overlappy.nameGroup)
		cmds.group(empty = True, name = Overlappy.nameGroup)
		# Run setup logic
		self._SetupCreate(self.selected)
		self._OffsetsUpdate(cacheReset = True)
		cmds.select(self.selected, replace = True)
	def _SetupCreate(self, objCurrent, *args):
		# Names
		_objConverted = Text.ConvertSymbols(objCurrent)
		nameLocGoal = Overlappy.nameLocGoalTarget[0] + _objConverted
		nameLocParticle = Overlappy.nameLocGoalTarget[1] + _objConverted
		nameParticle = Overlappy.nameParticle + _objConverted
		nameLocAimBase = Overlappy.nameLocAim[0] + _objConverted
		nameLocAimHidden = Overlappy.nameLocAim[1] + _objConverted
		nameLocAim = Overlappy.nameLocAim[2] + _objConverted
		nameLocAimUp = Overlappy.nameLocAim[3] + _objConverted
		nameLoftStart = Overlappy.nameLoft[0] + _objConverted
		nameLoftEnd = Overlappy.nameLoft[1] + _objConverted
		nameLoftShape = Overlappy.nameLoft[2] + _objConverted

		# Create locator for goal
		self.locGoalTarget[0] = cmds.spaceLocator(name = nameLocGoal)[0]
		cmds.parent(self.locGoalTarget[0], Overlappy.nameGroup)
		cmds.matchTransform(self.locGoalTarget[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.locGoalTarget[0], maintainOffset = True)
		cmds.setAttr(self.locGoalTarget[0] + ".visibility", 0)
		self.startPositionGoalParticle[0] = cmds.xform(self.locGoalTarget[0], query = True, translation = True)

		# Create particle, goal and get selected object position
		_position = cmds.xform(objCurrent, query = True, worldSpace = True, rotatePivot = True)
		self.particle = cmds.nParticle(name = nameParticle, position = _position, conserve = 1)[0]
		cmds.goal(useTransformAsGoal = True, goal = self.locGoalTarget[0])
		cmds.parent(self.particle, Overlappy.nameGroup)
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
		cmds.parent(self.nucleus, Overlappy.nameGroup)
		self.sliderNTimeScale.startName = self.nucleus
		cmds.setAttr(self.nucleus + ".gravity", 0)
		cmds.setAttr(self.nucleus + ".timeScale", self.sliderNTimeScale.Get())
		cmds.setAttr(self.nucleus + ".startFrame", self.time[2])
		cmds.setAttr(self.nucleus + ".visibility", 0)

		# Create and connect locator to particle
		self.locGoalTarget[1] = cmds.spaceLocator(name = nameLocParticle)[0]
		cmds.parent(self.locGoalTarget[1], Overlappy.nameGroup)
		cmds.matchTransform(self.locGoalTarget[1], objCurrent, position = True, rotation = True)
		cmds.connectAttr(self.particle + ".center", self.locGoalTarget[1] + ".translate", force = True)
		cmds.setAttr(self.locGoalTarget[1] + ".visibility", 0)

		# Create base aim locator
		self.locAim[0] = cmds.spaceLocator(name = nameLocAimBase)[0]
		cmds.parent(self.locAim[0], Overlappy.nameGroup)
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
		_scale2 = self.sliderPRadius.Get() * Overlappy.loftFactor
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
		cmds.parent(self.loft[2], Overlappy.nameGroup)
		cmds.setAttr(self.loft[2] + ".overrideEnabled", 1)
		cmds.setAttr(self.loft[2] + ".overrideDisplayType", 2)
		cmds.setAttr(self.loft[2] + ".overrideShading", 0)
		if (self._LoftGetDistance() < Overlappy.loftMinDistance):
			cmds.setAttr(self.loft[2] + ".visibility", 0)
	def _SetupScan(self, *args):
		# Check overlappy group
		if (not cmds.objExists(Overlappy.nameGroup)):
			cmds.warning("Overlappy object doesn't exists")
			return
		# Get children of group
		_children = cmds.listRelatives(Overlappy.nameGroup)
		if (len(_children) == 0):
			cmds.warning("Overlappy object has no children objects")
			return
		# Try to get suffix name
		_tempList = [Overlappy.nameLocGoalTarget[0], Overlappy.nameLocGoalTarget[1], Overlappy.nameParticle, Overlappy.nameLocAim[0], Overlappy.nameLoft[2]]
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
			self.selected = _converted
		
		def CheckAndSet(name):
			if (cmds.objExists(name + _objectName)):
				return name + _objectName
			else: return
		# Objects
		self.locGoalTarget[0] = CheckAndSet(Overlappy.nameLocGoalTarget[0])
		self.locGoalTarget[1] = CheckAndSet(Overlappy.nameLocGoalTarget[1])
		self.locAim[0] = CheckAndSet(Overlappy.nameLocAim[0])
		self.locAim[1] = CheckAndSet(Overlappy.nameLocAim[1])
		self.locAim[2] = CheckAndSet(Overlappy.nameLocAim[2])
		self.particle = CheckAndSet(Overlappy.nameParticle)
		self.loft[0] = CheckAndSet(Overlappy.nameLoft[0])
		self.loft[1] = CheckAndSet(Overlappy.nameLoft[1])
		self.loft[2] = CheckAndSet(Overlappy.nameLoft[2])
		# Time and offset
		self.TimeRangeScan()
		self.TimeRangeSetCurrent(self.time[2])
		self.startPositionGoalParticle[0] = cmds.xform(self.locAim[0], query = True, translation = True)
		self.TimeRangeSetCurrentCached()
		# Nucleus
		_nucleus = cmds.ls(type = "nucleus")
		if (len(_nucleus) > 0):
			self.nucleus = _nucleus[0]
			self.sliderNTimeScale.startName = self.nucleus
		# Get sliders
		self.sliderPRadius.Scan()
		self._GetSimulation()
		self._GetOffsets()
	def _SetupDelete(self, deselect=True, *args):
		self.selected = ""
		self.locGoalTarget = ["", ""]
		self.locAim = ["", "", "", ""]
		self.particle = ""
		self.nucleus = ""
		self.loft = ["", "", ""]
		# Delete group
		if (cmds.objExists(Overlappy.nameGroup)):
			cmds.delete(Overlappy.nameGroup)
		# Delete nucleus node
		_nucleus = cmds.ls(type = "nucleus")
		if (len(_nucleus) > 0):
			cmds.delete(_nucleus)
		if (deselect):
			cmds.select(clear = True)
	def _OffsetsUpdate(self, cacheReset=False, *args):
		if (type(cacheReset) is float): cacheReset = False
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
		else: return

		self._ValuesSetOffset()

		_checkSelected = self.selected == "" or not cmds.objExists(self.selected)
		_checkGoal = not cmds.objExists(self.locGoalTarget[0])
		_checkAim = not cmds.objExists(self.locAim[2])
		_checkStartPos = self.startPositionGoalParticle[0] == None
		if (_checkSelected or _checkGoal or _checkAim or _checkStartPos): return

		cmds.currentTime(self.time[2])
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
		_particleAttributes[0] = Overlappy.nameParticle + Text.ConvertSymbols(self.selected) + ".translateX"
		_particleAttributes[1] = Overlappy.nameParticle + Text.ConvertSymbols(self.selected) + ".translateY"
		_particleAttributes[2] = Overlappy.nameParticle + Text.ConvertSymbols(self.selected) + ".translateZ"
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
	def _Select(self, name="", *args):
		if (name != ""):
			if (cmds.objExists(name)):
				cmds.select(name, replace = True)
			else: cmds.warning("'{0}' object doesn't exists".format(name))
		else: cmds.warning("Can't select 'None'")
	def _SelectObjects(self, *args):
		if (self.selected == ""):
			self._Select()
		else:
			self._Select(self.selected)
	def _SelectParticle(self, *args):
		self._Select(self.particle)
	def _SelectNucleus(self, *args):
		self._Select(self.nucleus)
	def _SelectTarget(self, *args):
		self._Select(self.locGoalTarget[1])
	def _SelectAim(self, *args):
		self._Select(self.locAim[2])

	### VALUES
	def _ValuesSetSimulation(self, *args):
		self.sliderPRadius.Set()
		self.sliderPConserve.Set()
		self.sliderPDrag.Set()
		self.sliderPDamp.Set()
		self.sliderGSmooth.Set()
		self.sliderGWeight.Set()
		self.sliderNTimeScale.Set()
		self._LoftUpdate()
	def _ValuesSetOffset(self, *args):
		self.sliderOffsetX.Set()
		self.sliderOffsetY.Set()
		self.sliderOffsetZ.Set()
		self._LoftUpdate()
	def _LoftUpdate(self, *args):
		if (self.loft[1] == ""): return
		if (not cmds.objExists(self.loft[1])): return
		_scale = self.sliderPRadius.Get() * Overlappy.loftFactor
		cmds.setAttr(self.loft[1] + ".scaleX", _scale)
		cmds.setAttr(self.loft[1] + ".scaleY", _scale)
		cmds.setAttr(self.loft[1] + ".scaleZ", _scale)
		if (self._LoftGetDistance() < Overlappy.loftMinDistance): cmds.setAttr(self.loft[2] + ".visibility", 0)
		else: cmds.setAttr(self.loft[2] + ".visibility", 1)
	def _LoftGetDistance(self, *args):
		_vector = [0, 0, 0]
		_vector[0] = self.sliderOffsetX.Get()
		_vector[1] = self.sliderOffsetY.Get()
		_vector[2] = self.sliderOffsetZ.Get()
		return sqrt(pow(_vector[0], 2) + pow(_vector[1], 2) + pow(_vector[2], 2)) # Distance formula : V((x2 - x1)2 + (y2 - y1)2 + (z2 - z1)2)

	def _GetSimulation(self, *args):
		self.sliderPConserve.Scan()
		self.sliderPDrag.Scan()
		self.sliderPDamp.Scan()
		self.sliderGSmooth.Scan()
		self.sliderGWeight.Scan()
		self.sliderNTimeScale.Scan()
	def _GetOffsets(self, *args):
		self.sliderOffsetX.Scan()
		self.sliderOffsetY.Scan()
		self.sliderOffsetZ.Scan()
	def _ResetAllValues(self, *args):
		self.checkboxHierarchy.Reset()
		self.checkboxLayer.Reset()
		self.checkboxLoop.Reset()
		self.checkboxClean.Reset()
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
		self._ValuesSetSimulation()
	def _ResetOffsets(self, *args):
		self.checkboxMirrorX.Reset()
		self.checkboxMirrorY.Reset()
		self.checkboxMirrorZ.Reset()
		self.sliderOffsetX.Reset()
		self.sliderOffsetY.Reset()
		self.sliderOffsetZ.Reset()
		self._ValuesSetOffset()
	
	### BAKE
	def _BakeLogic(self, parent, zeroOffsets=False, translation=True, deleteSetupLock=False, *args):
		# Filter attributes
		_item = self.selected
		if (translation): _attributesType = Overlappy.attributesT
		else: _attributesType = Overlappy.attributesR
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
					if(_type in Overlappy.constraintsNames):
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
		_startTime = self.time[2]
		if (self.checkboxLoop.Get()):
			_startTime = self.time[2] - self.time[3] * self.loopOffset
			self.TimeRangeSetMin(_startTime)
			self.TimeRangeSetCurrent(_startTime)
		cmds.setAttr(self.nucleus + ".startFrame", _startTime) # TODO bug when select ovlp objects
		
		# Start logic
		_name = "_rebake_" + Text.ConvertSymbols(_item)
		_clone = cmds.duplicate(_item, name = _name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		for attr in Overlappy.attributesT:
			cmds.setAttr(_clone[0] + "." + attr, lock = False)
		for attr in Overlappy.attributesR:
			cmds.setAttr(_clone[0] + "." + attr, lock = False)
		cmds.parentConstraint(parent, _clone, maintainOffset = True) # skipTranslate
		cmds.select(_clone, replace = True)
		
		# Bake
		Overlappy.BakeSelected()
		_children = cmds.listRelatives(_clone, type = "constraint")
		for child in _children: cmds.delete(child)
		
		# Copy keys, check layer and paste keys
		cmds.copyKey(_clone, time = (self.time[2], self.time[3]), attribute = _attributesFiltered)
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
			_startTime = self.time[2]
			cmds.setAttr(self.nucleus + ".startFrame", _startTime)
			self.TimeRangeReset()
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
			if (self.selected == ""): return None
			return 0, None
		else:
			if (self.checkboxHierarchy.Get()):
				self.SelectTransformHierarchy()
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
	def _BakeWorldLocator(self, *args):
		_selected = cmds.ls(selection = True) # Get selected objects
		if (len(_selected) == 0):
			cmds.warning("You must select at least 1 object")
			return
		else:
			if (self.checkboxHierarchy.Get()):
				self.SelectTransformHierarchy()
				_selected = cmds.ls(selection = True)
		_locators = []
		for item in _selected: # Create locator
			_name = Overlappy.nameBakedWorldLocator + "1"
			_locator = cmds.spaceLocator(name = _name)[0]
			cmds.matchTransform(_locator, item, position = True, rotation = True)
			cmds.parentConstraint(item, _locator, maintainOffset = True)
			cmds.scaleConstraint(item, _locator, maintainOffset = True)
			_scale = 50
			cmds.setAttr(_locator + "Shape.localScaleX", _scale)
			cmds.setAttr(_locator + "Shape.localScaleY", _scale)
			cmds.setAttr(_locator + "Shape.localScaleZ", _scale)
			_locators.append(_locator)
		cmds.select(_locators, replace = True) # Bake and cleanup
		Overlappy.BakeSelected()
		for loc in _locators:
			_children = cmds.listRelatives(loc, type = "constraint")
			for child in _children:
				cmds.delete(child)

	### LAYERS
	def _LayerCreate(self, obj, *args):
		# Create main layer
		if(not cmds.objExists(Overlappy.nameLayers[0])):
			self.layers[0] = cmds.animLayer(Overlappy.nameLayers[0], override = True)
		# Create layers on selected
		_name = Overlappy.nameLayers[2] + Text.ConvertSymbols(obj) + "_1"
		return cmds.animLayer(_name, override = True, parent = self.layers[0])
	def _LayerMoveToSafeOrBase(self, safeLayer=True, *args):
		_id = [0, 1]
		if (not safeLayer): _id = [1, 0]
		_layer1 = Overlappy.nameLayers[_id[0]]
		_layer2 = Overlappy.nameLayers[_id[1]]

		# Check source layer
		if(not cmds.objExists(_layer1)):
			cmds.warning("Layer '{0}' doesn't exist".format(_layer1))
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
				cmds.warning("Layer '{0}' is empty".format(_layer1))
				return
			else:
				for layer in _children:
					_filteredLayers.append(layer)
		else:
			if (_children == None):
				cmds.warning("Layer '{0}' is empty".format(_layer1))
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
		# Delete base layer if no children
		if (len(_filteredLayers) == len(_children)):
			self._LayerDelete(_layer1)
	def _LayerDelete(self, name, *args):
		if(cmds.objExists(name)):
			cmds.delete(name)
			print("Layer '{0}' deleted".format(name))
		else:
			cmds.warning("Layer '{0}' doesn't exist".format(name))
	def _LayerCreate_TEST(self, *args):
		# Check selected
		_selected = cmds.ls(selection = True)
		if (len(_selected) == 0):
			cmds.warning("You must select at least 1 object")
			return
		# Create main layer
		if(not cmds.objExists(Overlappy.nameLayers[0])):
			self.layers[0] = cmds.animLayer(Overlappy.nameLayers[0], override = True)
		# Create layers on selected
		for item in _selected:
			_name = Overlappy.nameLayers[2] + Text.ConvertSymbols(item) + "_1"
			cmds.animLayer(_name, override = True, parent = self.layers[0])

