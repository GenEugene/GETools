### DEPRECATED ###
# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

# Overlappy v2.0.0 for Maya 2022
# Author Eugene Gataulin (GenEugene) tek94@mail.ru tek942@gmail.com
# https://github.com/GenEugene/Overlappy

import maya.cmds as c
from math import pow, sqrt
from functools import partial
# import maya.mel as mel
# import sys, os

class OVLP:
	# NAMING
	textTitle = "OVERLAPPY v2.0.0"
	nameWindowMain = "__OverlappyWindow__"
	nameGroup = "_OverlappyGroup_"
	nameLocGoalTarget = ("_locGoal_", "_locTarget_")
	nameLocAim = ("_locAimBase_", "_locAimHidden_", "_locAim_", "_locAimUp_")
	nameParticle = "_particle_"
	nameLoft = ("_loftStart_", "_loftEnd_", "_loftShape_")
	nameLayers = ("_OVLP_BASE_", "_OVLP_SAFE_", "OVLP_", "OVLPpos_", "OVLProt_")
	nameBakedWorldLocator = "BakedWorldLocator_"
	replaceSymbols = ("_R1S_", "_R2S_") # for "|" and ":"
	# WINDOW
	windowWidth = 330
	windowHeight = 27
	lineHeight = 28
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
	loopOffset = 2 # TODO set count of pre cycles
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
	# COLORS
	cLRed = (1, .7, .7)
	cRed = (1, .5, .5)
	cLOrange = (1, .75, .45)
	cOrange = (1, .6, .3)
	cYellow = (1, 1, .5)
	cGreen = (.6, 1, .6)
	cLBlue = (.5, .9, 1)
	cBlue = (.3, .7, 1)
	cPurple = (.81, .4, 1)
	cWhite = (1, 1, 1)
	cGray = (.5, .5, .5)
	cDarkGray = (.3, .3, .3)
	cBlack = (.15, .15, .15)
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
		self.layoutMain = None
		self.layoutButtons = None
		# self.layoutBaking = None
		# self.layoutOptions = None
		self.layoutSimulation = None
		self.layoutOffset = None
		self.layoutDevTools = None
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
	def CreateUI(self):
		# WINDOW
		if c.window(OVLP.nameWindowMain, exists = True):
			c.deleteUI(OVLP.nameWindowMain)
		self.windowMain = c.window(OVLP.nameWindowMain, title = OVLP.textTitle, maximizeButton = 0, sizeable = 0, resizeToFitChildren = True, widthHeight = (OVLP.windowWidth, OVLP.windowHeight * 6))
		self.layoutMain = c.columnLayout(adjustableColumn = True, height = OVLP.windowHeight)

		# CLASSES
		class classCheckbox:
			def __init__(self, label="label", value=False, command="pass", menuReset=True, enabled=True, ccResetAll="pass"):
				self.value = value
				self.checkbox = c.checkBox(label = label, value = value, changeCommand = command, enable = enabled)
				c.popupMenu()
				if (menuReset):
					c.menuItem(label = "reset current", command = self.Reset)
					c.menuItem(label = "reset all", command = ccResetAll)
			def Get(self, *args):
				return c.checkBox(self.checkbox, query = True, value = True)
			def Set(self, value=None, *args):
				c.checkBox(self.checkbox, edit = True, value = value)
			def Reset(self, *args):
				c.checkBox(self.checkbox, edit = True, value = self.value)
		class classSlider:
			def __init__(self, label="label", attribute="", startName="", nameAdd=True, value=0, minMax=[0, 1, 0, 1], parent=self.layoutMain, command="pass", precision=3, menuReset=True, menuScan=True, ccResetAll="pass", ccScanAll="pass"):
				self.attribute = attribute
				self.startName = startName
				self.addSelectedName = nameAdd
				self.value = value
				self.command = command
				self.precision = precision
				self.markerColorDefault = OVLP.cGray
				self.markerColorChanged = OVLP.cBlue
				self.valueCached = 0;
				c.flowLayout(parent = parent)
				self.slider = c.floatSliderGrp(label = " " + label, value = self.value, changeCommand = self.command, dragCommand = self.command, fieldMinValue = minMax[0], fieldMaxValue = minMax[1], minValue = minMax[2], maxValue = minMax[3], field = True,
														precision = self.precision, width = OVLP.windowWidth - OVLP.markerWidth, columnAlign = (1, "left"), columnWidth3 = (OVLP.sliderWidth[0], OVLP.sliderWidth[1], OVLP.sliderWidth[2]), enableKeyboardFocus = True)
				c.popupMenu(parent = self.slider)
				if (menuReset):
					c.menuItem(label = "reset current", command = self.Reset)
					c.menuItem(label = "reset all", command = ccResetAll)
				if (menuScan):
					c.menuItem(divider = True)
					c.menuItem(label = "scan current", command = self.Scan)
					c.menuItem(label = "scan all", command = ccScanAll)
				self._marker = c.button(label = "", enable = 0, w = OVLP.markerWidth, backgroundColor = self.markerColorDefault)
			def Get(self, *args):
				return c.floatSliderGrp(self.slider, query = True, value = True)
			def Set(self, value=None, *args):
				if (value == None): _value = c.floatSliderGrp(self.slider, query = True, value = True)
				else:
					_value = value
					c.floatSliderGrp(self.slider, edit = True, value = _value)
					self.command()
				# Marker update
				if (_value != self.value):
					c.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
				else:
					c.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
				# Check selected
				_selectedName = _OVERLAPPY.selected
				if (_selectedName == ""):
					return
				# Add suffix or not
				_selectedName = _OVERLAPPY.ConvertText(_selectedName) # TODO _OVERLAPPY
				if (self.addSelectedName):
					_selectedName = self.startName + _selectedName
				else:
					_selectedName = self.startName
				# Set attribute
				try:
					c.setAttr(_selectedName + self.attribute, _value)
				except:
					# print("Can't set value")
					pass
			def Reset(self, *args):
				c.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
				c.floatSliderGrp(self.slider, edit = True, value = self.value)
				self.command()
			def Scan(self, *args):
				_firstName = _OVERLAPPY.selected
				if (_firstName == ""):
					return
				_firstName = _OVERLAPPY.ConvertText(_firstName)
				if (self.addSelectedName):
					_firstName = self.startName + _firstName
				else:
					_firstName = self.startName
				# Get attribute
				try:
					# print(firstName + self._attribute)
					_value = c.getAttr(_firstName + self.attribute)
					c.floatSliderGrp(self.slider, edit = True, value = _value)
				except:
					# print("Can't get value")
					return
				# Marker update
				if (round(_value, 3) != self.value):
					c.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
				else:
					c.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
			def GetCached(self, *args):
				return self.valueCached
			def SetCached(self, *args):
				self.valueCached = c.floatSliderGrp(self.slider, query = True, value = True)
			def ResetCached(self, *args):
				self.valueCached = 0

		# HEAD MENU
		c.menuBarLayout()
		#
		# c.menu(label = "Settings")
		# c.menuItem(label = "Save")
		# c.menuItem(label = "Save as")
		# c.menuItem(label = "Load")
		# c.menuItem(divider = True)
		# c.menuItem(label = "Reset")
		#
		c.menu(label = "Scene")
		c.menuItem(label = "Reload", command = self.SceneReload)
		c.menuItem(dividerLabel = "Be careful", divider = True)
		c.menuItem(label = "Quit", command = self.SceneQuit)
		#
		c.menu(label = "Script")
		c.menuItem(label = "Reload", command = self.Restart)
		c.menuItem(dividerLabel = "Layouts", divider = True)
		c.menuItem(label = "Collapse all", command = partial(self.LayoutsCollapseLogic, True))
		c.menuItem(label = "Expand all", command = partial(self.LayoutsCollapseLogic, False))
		c.menuItem(dividerLabel = "Other", divider = True)
		c.menuItem(label = "Dev Tools toggle", command = self.LayoutDevToolsToggle, checkBox = False)
		#
		c.menu(label = "Help")
		def LinkPatreon(self): c.showHelp("https://www.patreon.com/geneugene", absolute = True)
		def LinkGumroad(self): c.showHelp("https://app.gumroad.com/geneugene", absolute = True)
		def LinkGithub(self): c.showHelp("https://github.com/GenEugene/Overlappy", absolute = True)
		def LinkYoutube(self): c.showHelp("https://www.youtube.com/channel/UCCIzdVu6RMqUoOmxHoOEPAQ", absolute = True)
		def LinkReport(self): c.showHelp("https://github.com/GenEugene/Overlappy/discussions/categories/report-a-problem", absolute = True)
		c.menuItem(label = "About Overlappy", enable = False) # TODO add window with information
		c.menuItem(dividerLabel = "Links", divider = True)
		# c.menuItem(label = "Discord")
		c.menuItem(label = "Patreon", command = LinkPatreon)
		c.menuItem(label = "Gumroad", command = LinkGumroad)
		c.menuItem(label = "GitHub", command = LinkGithub)
		c.menuItem(label = "YouTube", command = LinkYoutube)
		c.menuItem(dividerLabel = "Support", divider = True)
		c.menuItem(label = "Report a Problem...", command = LinkReport)
		
		# BUTTONS
		self.layoutButtons = c.frameLayout(label = "BUTTONS", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		c.gridLayout(parent = self.layoutButtons, numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		c.button(label = "RESET ALL", command = self._ResetAllValues, backgroundColor = OVLP.cYellow)
		c.button(label = "SELECT", command = self.SelectTransformHierarchy, backgroundColor = OVLP.cLBlue)
		c.popupMenu()
		c.menuItem(dividerLabel = "Created objects", divider = True)
		c.menuItem(label = "Objects", command = self._SelectObjects)
		c.menuItem(label = "Particle", command = self._SelectParticle)
		c.menuItem(label = "Nucleus", command = self._SelectNucleus)
		c.menuItem(label = "Target", command = self._SelectTarget)
		c.menuItem(label = "Aim", command = self._SelectAim)
		c.button(label = "LAYERS", command = partial(self._LayerMoveToSafeOrBase, True), backgroundColor = OVLP.cBlue) # _LayerCreate_TEST - old func for tests
		c.popupMenu()
		c.menuItem(dividerLabel = "Move", divider = True)
		c.menuItem(label = "Move to Base layer", command = partial(self._LayerMoveToSafeOrBase, False))
		c.menuItem(dividerLabel = "Delete", divider = True)
		c.menuItem(label = "Delete '{0}'".format(OVLP.nameLayers[0]), command = partial(self._LayerDelete, OVLP.nameLayers[0]))
		c.menuItem(label = "Delete '{0}'".format(OVLP.nameLayers[1]), command = partial(self._LayerDelete, OVLP.nameLayers[1]))
		c.menuItem(divider = True)
		c.menuItem(label = "Delete 'BaseAnimation'", command = partial(self._LayerDelete, "BaseAnimation"))
		c.button(label = "SETUP", command = self._SetupInit, backgroundColor = OVLP.cGreen)
		c.popupMenu()
		c.menuItem(label = "Scan setup into scene", command = self._SetupScan)
		c.menuItem(dividerLabel = "Delete", divider = True)
		c.menuItem(label = "Delete setup", command = self._SetupDelete)
		
		# BAKING
		# self.layoutBaking = c.frameLayout(label = "BAKING", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		# c.gridLayout(parent = self.layoutButtons, numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		c.button(label = "TRANSLATION", command = partial(self._BakeVariants, 1), backgroundColor = OVLP.cLOrange)
		c.popupMenu()
		c.menuItem(label = "use offset", command = partial(self._BakeVariants, 2))
		c.button(label = "ROTATION", command = partial(self._BakeVariants, 3), backgroundColor = OVLP.cLOrange)
		c.button(label = "COMBO", command = partial(self._BakeVariants, 4), backgroundColor = OVLP.cLOrange)
		c.popupMenu()
		c.menuItem(label = "translate + rotate", command = self._BakeVariantComboTR)
		c.menuItem(label = "rotate + translate", command = self._BakeVariantComboRT)
		# c.gridLayout(parent = self.layoutBaking, numberOfColumns = 2, cellWidthHeight = (OVLP.windowWidth / 2, OVLP.lineHeight))
		c.button(label = "TO LOCATOR", command = self._BakeWorldLocator, backgroundColor = OVLP.cOrange)

		# OPTIONS
		# self.layoutOptions = c.frameLayout(label = "OPTIONS", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		# c.gridLayout(parent = self.layoutButtons, numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		_optionsResetAll = self._ResetOptions
		self.checkboxHierarchy = classCheckbox(label = "HIERARCHY", value = OVLP.checkboxesOptions[0], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxLayer = classCheckbox(label = "LAYER", value = OVLP.checkboxesOptions[1], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxLoop = classCheckbox(label = "LOOP", value = OVLP.checkboxesOptions[2], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxClean = classCheckbox(label = "CLEAN", value = OVLP.checkboxesOptions[3], menuReset = True, ccResetAll = _optionsResetAll)

		# SIMULATION SETTINGS
		self.layoutSimulation = c.frameLayout(label = "SIMULATION", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		c.columnLayout(parent = self.layoutSimulation)
		_simStartName = OVLP.nameParticle
		_simParent = self.layoutSimulation
		_simCCDefault = self._ValuesSetSimulation
		_simCCReset = partial(self._ResetSimulation, True)
		_simCCGetValues = self._GetSimulation
		self.sliderPRadius = classSlider(label = "Radius", attribute = "Shape.radius", startName = _simStartName, nameAdd = True, value = OVLP.particleRadius, minMax = OVLP.rangePRadius, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		self.sliderPConserve = classSlider(label = "Conserve", attribute = "Shape.conserve", startName = _simStartName, nameAdd = True, value = OVLP.particleConserve, minMax = OVLP.rangePConserve, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		self.sliderPDrag = classSlider(label = "Drag", attribute = "Shape.drag", startName = _simStartName, nameAdd = True, value = OVLP.particleDrag, minMax = OVLP.rangePDrag, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		self.sliderPDamp = classSlider(label = "Damp", attribute = "Shape.damp", startName = _simStartName, nameAdd = True, value = OVLP.particleDamp, minMax = OVLP.rangePDamp, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		self.sliderGSmooth = classSlider(label = "G.Smooth", attribute = "Shape.goalSmoothness", startName = _simStartName, nameAdd = True, value = OVLP.goalSmooth, minMax = OVLP.rangeGSmooth, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		self.sliderGWeight = classSlider(label = "G.Weight", attribute = "Shape.goalWeight[0]", startName = _simStartName, nameAdd = True, value = OVLP.goalWeight, minMax = OVLP.rangeGWeight, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		self.sliderNTimeScale = classSlider(label = "Time Scale", attribute = ".timeScale", startName = self.nucleus, nameAdd = False, value = OVLP.nucleusTimeScale, minMax = OVLP.rangeNTimeScale, parent = _simParent, command = _simCCDefault, ccResetAll = _simCCReset, ccScanAll = _simCCGetValues)
		
		# OFFSET SETTINGS
		self.layoutOffset = c.frameLayout(label = "OFFSET", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		c.gridLayout(numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		c.separator()
		self.checkboxMirrorX = classCheckbox(label = "MIRROR X", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		self.checkboxMirrorY = classCheckbox(label = "MIRROR Y", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		self.checkboxMirrorZ = classCheckbox(label = "MIRROR Z", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		c.columnLayout(parent = self.layoutOffset)
		_offStartName = OVLP.nameLocGoalTarget[0]
		_offParent = self.layoutOffset
		_offCCDefault = self._OffsetsUpdate
		_offCCReset = self._ResetOffsets
		_offCCGetValues = self._GetOffsets
		self.sliderOffsetX = classSlider(label = "   Local X", attribute = "_parentConstraint1.target[0].targetOffsetTranslateX", startName = _offStartName, minMax = OVLP.rangeOffsetX, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
		self.sliderOffsetY = classSlider(label = "   Local Y", attribute = "_parentConstraint1.target[0].targetOffsetTranslateY", startName = _offStartName, minMax = OVLP.rangeOffsetY, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
		self.sliderOffsetZ = classSlider(label = "   Local Z", attribute = "_parentConstraint1.target[0].targetOffsetTranslateZ", startName = _offStartName, minMax = OVLP.rangeOffsetZ, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)

		# DEV TOOLS
		self.layoutDevTools = c.frameLayout(label = "DEV TOOLS", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack, visible = False)
		c.gridLayout(parent = self.layoutDevTools, numberOfColumns = 3, cellWidthHeight = (OVLP.windowWidth / 3, OVLP.lineHeight))
		c.button(label = "DEV FUNCTION", command = self._DEVFunction, backgroundColor = OVLP.cBlack)
		c.button(label = "MOTION TRAIL", command = self._MotionTrailCreate, backgroundColor = OVLP.cBlack)
		c.popupMenu()
		c.menuItem(label = "Select", command = self._MotionTrailSelect)
		c.menuItem(divider = True)
		c.menuItem(label = "Delete", command = self._MotionTrailDelete)

		# RUN WINDOW
		c.showWindow(self.windowMain)
		self.Resize_UI()
	def Resize_UI(self, *args): # TODO get count of visible layouts
		c.window(self.windowMain, edit = True, height = 152, resizeToFitChildren = True) # OVLP.windowHeight * 6
	
	def LayoutsCollapseLogic(self, value, *args): # TODO to external class
		if (value):
			if (self.LayoutsCollapseCheck() == value):
				return
		else:
			if (self.LayoutsCollapseCheck() == value):
				return
		c.frameLayout(self.layoutButtons, edit = True, collapse = value)
		# c.frameLayout(self.layoutBaking, edit = True, collapse = value)
		# c.frameLayout(self.layoutOptions, edit = True, collapse = value)
		c.frameLayout(self.layoutSimulation, edit = True, collapse = value)
		c.frameLayout(self.layoutOffset, edit = True, collapse = value)
		c.frameLayout(self.layoutDevTools, edit = True, collapse = value)
		self.Resize_UI()
	def LayoutsCollapseCheck(self, *args): # needed to fix the window bug
		check1 = c.frameLayout(self.layoutButtons, query = True, collapse = True)
		# check2 = c.frameLayout(self.layoutBaking, query = True, collapse = True)
		# check3 = c.frameLayout(self.layoutOptions, query = True, collapse = True)
		check4 = c.frameLayout(self.layoutSimulation, query = True, collapse = True)
		check5 = c.frameLayout(self.layoutOffset, query = True, collapse = True)
		check6 = c.frameLayout(self.layoutDevTools, query = True, collapse = True)
		# if (check1 == check2 == check3 == check4 == check5 == check6):
		if (check1 == check4 == check5 == check6):
			return check1
	def LayoutDevToolsToggle(self, *args):
		_value = c.frameLayout(self.layoutDevTools, query = True, visible = True)
		c.frameLayout(self.layoutDevTools, edit = True, visible = not _value)
		self.Resize_UI()
	
	def SceneReload(self, *args): # TODO to external class
		currentScene = c.file(query = True, sceneName = True)
		if(currentScene): c.file(currentScene, open = True, force = True)
		else: c.file(new = True, force = True)
	def SceneQuit(self, *args): # TODO to external class
		c.quit(force = True)
	
	def ConvertText(self, text, direction=True, *args):
		if (direction):
			_text = text.replace("|", OVLP.replaceSymbols[0])
			_text = _text.replace(":", OVLP.replaceSymbols[1])
			return _text
		else:
			_text = text.replace(OVLP.replaceSymbols[0], "|")
			_text = _text.replace(OVLP.replaceSymbols[1], ":")
			return _text
	
	def TimeRangeScan(self, *args): # TODO to external class
		self.time[0] = c.currentTime(query = True)
		self.time[1] = c.playbackOptions(query = True, animationStartTime = True)
		self.time[2] = c.playbackOptions(query = True, min = True)
		self.time[3] = c.playbackOptions(query = True, max = True)
		self.time[4] = c.playbackOptions(query = True, animationEndTime = True)
	def TimeRangeSetCurrent(self, value, *args):
		c.currentTime(value)
	def TimeRangeSetCurrentCached(self, *args):
		c.currentTime(self.time[0])
	def TimeRangeSetMin(self, value, *args):
		c.playbackOptions(edit = True, min = value)
	def TimeRangeReset(self, *args):
		c.playbackOptions(edit = True, animationStartTime = self.time[1], min = self.time[2], max = self.time[3], animationEndTime = self.time[4])
		c.currentTime(self.time[2])

	def SelectTransformHierarchy(self, *args):# TODO from GETools class (need to merge in future)
		_selected = c.ls(selection = True)
		if (len(_selected) == 0):
			c.warning("You must select at least 1 object")
			return
		c.select(hierarchy = True)
		list = c.ls(selection = True, type = "transform", shapes = False)
		c.select(clear = True)
		for i in range(len(list)):
			c.select(list[i], add = True)
	@staticmethod
	def BakeSelected(doNotCut=True): # TODO from GETools class (need to merge in future)
		_startTime = c.playbackOptions(query = True, min = True)
		_endTime = c.playbackOptions(query = True, max = True)
		c.bakeResults(t = (_startTime, _endTime), preserveOutsideKeys = doNotCut, simulation = True)

	### LOGIC
	def _SetupInit(self, *args):
		self._SetupDelete(False)
		# Get selected objects
		self.selected = c.ls(selection = True)
		if (len(self.selected) == 0):
			c.warning("You must select at least 1 object")
			self.selected = ""
			return
		self.selected = self.selected[0]
		# Get min/max anim range time and reset time slider
		self.TimeRangeScan()
		self.TimeRangeSetCurrent(self.time[2])
		# Create group
		c.select(clear = True)
		if (c.objExists(OVLP.nameGroup)):
			c.delete(OVLP.nameGroup)
		c.group(empty = True, name = OVLP.nameGroup)
		# Run setup logic
		self._SetupCreate(self.selected)
		self._OffsetsUpdate(cacheReset = True)
		c.select(self.selected, replace = True)
	def _SetupCreate(self, objCurrent, *args):
		# Names
		_objConverted = self.ConvertText(objCurrent)
		nameLocGoal = OVLP.nameLocGoalTarget[0] + _objConverted
		nameLocParticle = OVLP.nameLocGoalTarget[1] + _objConverted
		nameParticle = OVLP.nameParticle + _objConverted
		nameLocAimBase = OVLP.nameLocAim[0] + _objConverted
		nameLocAimHidden = OVLP.nameLocAim[1] + _objConverted
		nameLocAim = OVLP.nameLocAim[2] + _objConverted
		nameLocAimUp = OVLP.nameLocAim[3] + _objConverted
		nameLoftStart = OVLP.nameLoft[0] + _objConverted
		nameLoftEnd = OVLP.nameLoft[1] + _objConverted
		nameLoftShape = OVLP.nameLoft[2] + _objConverted

		# Create locator for goal
		self.locGoalTarget[0] = c.spaceLocator(name = nameLocGoal)[0]
		c.parent(self.locGoalTarget[0], OVLP.nameGroup)
		c.matchTransform(self.locGoalTarget[0], objCurrent, position = True, rotation = True)
		c.parentConstraint(objCurrent, self.locGoalTarget[0], maintainOffset = True)
		c.setAttr(self.locGoalTarget[0] + ".visibility", 0)
		self.startPositionGoalParticle[0] = c.xform(self.locGoalTarget[0], query = True, translation = True)

		# Create particle, goal and get selected object position
		_position = c.xform(objCurrent, query = True, worldSpace = True, rotatePivot = True)
		self.particle = c.nParticle(name = nameParticle, position = _position, conserve = 1)[0]
		c.goal(useTransformAsGoal = True, goal = self.locGoalTarget[0])
		c.parent(self.particle, OVLP.nameGroup)
		# self.startPositionGoalParticle[1] = c.xform(self.particle, query = True, translation = True)
		c.setAttr(self.particle + ".overrideEnabled", 1)
		c.setAttr(self.particle + ".overrideDisplayType", 2)

		# Set simulation attributes
		c.setAttr(self.particle + "Shape.radius", self.sliderPRadius.Get())
		c.setAttr(self.particle + "Shape.solverDisplay", 1)
		c.setAttr(self.particle + "Shape.conserve", self.sliderPConserve.Get())
		c.setAttr(self.particle + "Shape.drag", self.sliderPDrag.Get())
		c.setAttr(self.particle + "Shape.damp", self.sliderPDamp.Get())
		c.setAttr(self.particle + "Shape.goalSmoothness", self.sliderGSmooth.Get())
		c.setAttr(self.particle + "Shape.goalWeight[0]", self.sliderGWeight.Get())

		# Nucleus detection
		self.nucleus = c.ls(type = "nucleus")[0]
		c.parent(self.nucleus, OVLP.nameGroup)
		self.sliderNTimeScale.startName = self.nucleus
		c.setAttr(self.nucleus + ".gravity", 0)
		c.setAttr(self.nucleus + ".timeScale", self.sliderNTimeScale.Get())
		c.setAttr(self.nucleus + ".startFrame", self.time[2])
		c.setAttr(self.nucleus + ".visibility", 0)

		# Create and connect locator to particle
		self.locGoalTarget[1] = c.spaceLocator(name = nameLocParticle)[0]
		c.parent(self.locGoalTarget[1], OVLP.nameGroup)
		c.matchTransform(self.locGoalTarget[1], objCurrent, position = True, rotation = True)
		c.connectAttr(self.particle + ".center", self.locGoalTarget[1] + ".translate", force = True)
		c.setAttr(self.locGoalTarget[1] + ".visibility", 0)

		# Create base aim locator
		self.locAim[0] = c.spaceLocator(name = nameLocAimBase)[0]
		c.parent(self.locAim[0], OVLP.nameGroup)
		c.matchTransform(self.locAim[0], objCurrent, position = True, rotation = True)
		c.parentConstraint(objCurrent, self.locAim[0], maintainOffset = True)
		c.setAttr(self.locAim[0] + ".visibility", 0)

		# Create hidden aim locator
		self.locAim[1] = c.spaceLocator(name = nameLocAimHidden)[0]
		c.matchTransform(self.locAim[1], self.locAim[0], position = True, rotation = True)
		c.parent(self.locAim[1], self.locAim[0])
		c.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		c.delete(self.locAim[1] + "_aimConstraint1")
		self.locAim[3] = c.duplicate(self.locAim[1], name = nameLocAimUp)[0]
		c.parent(self.locAim[3], self.locAim[1])
		c.setAttr(self.locAim[3] + ".ty", 100)
		c.parent(self.locAim[3], self.locAim[0])
		c.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.locAim[3]) # "scene" "object" "objectrotation" "vector" "none"
		
		# Create aim locator
		self.locAim[2] = c.spaceLocator(name = nameLocAim)[0]
		c.matchTransform(self.locAim[2], self.locAim[0], position = True, rotation = True)
		c.parent(self.locAim[2], self.locAim[0])

		# Create aim loft
		self.loft[0] = c.circle(name = nameLoftStart, degree = 1, sections = 4, normal = [0, 1, 0])[0]
		self.loft[1] = c.duplicate(self.loft[0], name = nameLoftEnd)[0]
		_scale1 = 0.001
		_scale2 = self.sliderPRadius.Get() * OVLP.loftFactor
		c.setAttr(self.loft[0] + ".scaleX", _scale1)
		c.setAttr(self.loft[0] + ".scaleY", _scale1)
		c.setAttr(self.loft[0] + ".scaleZ", _scale1)
		c.setAttr(self.loft[1] + ".scaleX", _scale2)
		c.setAttr(self.loft[1] + ".scaleY", _scale2)
		c.setAttr(self.loft[1] + ".scaleZ", _scale2)
		c.setAttr(self.loft[0] + ".visibility", 0)
		c.setAttr(self.loft[1] + ".visibility", 0)
		#
		c.matchTransform(self.loft[0], self.locAim[2], position = True, rotation = True)
		c.parent(self.loft[0], self.locAim[2])
		c.matchTransform(self.loft[1], self.locGoalTarget[1], position = True)
		c.parent(self.loft[1], self.locGoalTarget[1])
		c.aimConstraint(self.loft[0], self.loft[1], weight = 1, aimVector = (0, 1, 0), upVector = (0, 1, 0), worldUpType = "vector", worldUpVector = (0, 0, 1))
		#
		self.loft[2] = c.loft(self.loft[0], self.loft[1], name = nameLoftShape, reverseSurfaceNormals = 0, uniform = 1, polygon = 0)[0]
		c.parent(self.loft[2], OVLP.nameGroup)
		c.setAttr(self.loft[2] + ".overrideEnabled", 1)
		c.setAttr(self.loft[2] + ".overrideDisplayType", 2)
		c.setAttr(self.loft[2] + ".overrideShading", 0)
		if (self._LoftGetDistance() < OVLP.loftMinDistance):
			c.setAttr(self.loft[2] + ".visibility", 0)
	def _SetupScan(self, *args):
		# Check overlappy group
		if (not c.objExists(OVLP.nameGroup)):
			c.warning("Overlappy object doesn't exists")
			return
		# Get children of group
		_children = c.listRelatives(OVLP.nameGroup)
		if (len(_children) == 0):
			c.warning("Overlappy object has no children objects")
			return
		# Try to get suffix name
		_tempList = [OVLP.nameLocGoalTarget[0], OVLP.nameLocGoalTarget[1], OVLP.nameParticle, OVLP.nameLocAim[0], OVLP.nameLoft[2]]
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
					else: c.warning("Suffix '{0}' don't equals to '{1}'".format(_objectName, _lastName))
		_converted = self.ConvertText(_objectName, False)
		if (c.objExists(_converted)):
			self.selected = _converted
		
		def CheckAndSet(name):
			if (c.objExists(name + _objectName)):
				return name + _objectName
			else: return
		# Objects
		self.locGoalTarget[0] = CheckAndSet(OVLP.nameLocGoalTarget[0])
		self.locGoalTarget[1] = CheckAndSet(OVLP.nameLocGoalTarget[1])
		self.locAim[0] = CheckAndSet(OVLP.nameLocAim[0])
		self.locAim[1] = CheckAndSet(OVLP.nameLocAim[1])
		self.locAim[2] = CheckAndSet(OVLP.nameLocAim[2])
		self.particle = CheckAndSet(OVLP.nameParticle)
		self.loft[0] = CheckAndSet(OVLP.nameLoft[0])
		self.loft[1] = CheckAndSet(OVLP.nameLoft[1])
		self.loft[2] = CheckAndSet(OVLP.nameLoft[2])
		# Time and offset
		self.TimeRangeScan()
		self.TimeRangeSetCurrent(self.time[2])
		self.startPositionGoalParticle[0] = c.xform(self.locAim[0], query = True, translation = True)
		self.TimeRangeSetCurrentCached()
		# Nucleus
		_nucleus = c.ls(type = "nucleus")
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
		if (c.objExists(OVLP.nameGroup)):
			c.delete(OVLP.nameGroup)
		# Delete nucleus node
		_nucleus = c.ls(type = "nucleus")
		if (len(_nucleus) > 0):
			c.delete(_nucleus)
		if (deselect):
			c.select(clear = True)
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

		_checkSelected = self.selected == "" or not c.objExists(self.selected)
		_checkGoal = not c.objExists(self.locGoalTarget[0])
		_checkAim = not c.objExists(self.locAim[2])
		_checkStartPos = self.startPositionGoalParticle[0] == None
		if (_checkSelected or _checkGoal or _checkAim or _checkStartPos): return

		c.currentTime(self.time[2])
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
		c.setAttr(_goalAttributes[0], _values[0])
		c.setAttr(_goalAttributes[1], _values[1])
		c.setAttr(_goalAttributes[2], _values[2])
		# Get offset
		_goalPosition = c.xform(self.locGoalTarget[0], query = True, translation = True)
		_goalOffset = [0, 0, 0]
		_goalOffset[0] = self.startPositionGoalParticle[0][0] - _goalPosition[0]
		_goalOffset[1] = self.startPositionGoalParticle[0][1] - _goalPosition[1]
		_goalOffset[2] = self.startPositionGoalParticle[0][2] - _goalPosition[2]
		# Set particle attributes
		_particleAttributes = [0, 0, 0]
		_particleAttributes[0] = OVLP.nameParticle + self.ConvertText(self.selected) + ".translateX"
		_particleAttributes[1] = OVLP.nameParticle + self.ConvertText(self.selected) + ".translateY"
		_particleAttributes[2] = OVLP.nameParticle + self.ConvertText(self.selected) + ".translateZ"
		c.setAttr(_particleAttributes[0], self.startPositionGoalParticle[1][0] - _goalOffset[0])
		c.setAttr(_particleAttributes[1], self.startPositionGoalParticle[1][1] - _goalOffset[1])
		c.setAttr(_particleAttributes[2], self.startPositionGoalParticle[1][2] - _goalOffset[2])
		# Reposition aim up locator and reconstrain aim
		_selected = c.ls(selection = True)
		c.delete(self.locAim[1] + "_aimConstraint1")
		c.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		c.delete(self.locAim[1] + "_aimConstraint1")
		c.parent(self.locAim[3], self.locAim[1])
		c.setAttr(self.locAim[3] + ".tx", 0)
		c.setAttr(self.locAim[3] + ".ty", 100)
		c.setAttr(self.locAim[3] + ".tz", 0)
		c.parent(self.locAim[3], self.locAim[0])
		c.aimConstraint(self.locGoalTarget[1], self.locAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.locAim[3])
		c.select(_selected, replace = True)
		# Reconstrain aim locator to hidden aim
		c.setAttr(self.locAim[2] + ".rotateX", 0)
		c.setAttr(self.locAim[2] + ".rotateY", 0)
		c.setAttr(self.locAim[2] + ".rotateZ", 0)
		c.orientConstraint(self.locAim[1], self.locAim[2], maintainOffset = True)

	### SELECT
	def _Select(self, name="", *args):
		if (name != ""):
			if (c.objExists(name)):
				c.select(name, replace = True)
			else: c.warning("'{0}' object doesn't exists".format(name))
		else: c.warning("Can't select 'None'")
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
		if (not c.objExists(self.loft[1])): return
		_scale = self.sliderPRadius.Get() * OVLP.loftFactor
		c.setAttr(self.loft[1] + ".scaleX", _scale)
		c.setAttr(self.loft[1] + ".scaleY", _scale)
		c.setAttr(self.loft[1] + ".scaleZ", _scale)
		if (self._LoftGetDistance() < OVLP.loftMinDistance): c.setAttr(self.loft[2] + ".visibility", 0)
		else: c.setAttr(self.loft[2] + ".visibility", 1)
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
		if (translation): _attributesType = OVLP.attributesT
		else: _attributesType = OVLP.attributesR
		_attrs = ["", "", ""]
		for i in range(len(_attrs)):
			_attrs[i] = "{0}.{1}".format(_item, _attributesType[i])
		_attributesFiltered = []
		for i in range(len(_attrs)):
			_keyed = c.keyframe(_attrs[i], query = True)
			if(_keyed):
				_muted = c.mute(_attrs[i], query = True)
				if(_muted):
					continue
			_locked = c.getAttr(_attrs[i], lock = True)
			_keyable = c.getAttr(_attrs[i], keyable = True)
			_settable = c.getAttr(_attrs[i], settable = True)
			_constrained = False
			_connections = c.listConnections(_attrs[i])
			if(_connections):
				for item in _connections:
					_type = c.nodeType(item)
					if(_type in OVLP.constraintsNames):
						_constrained = True
			if(not _locked and _keyable and _settable and not _constrained):
				_attributesFiltered.append(_attributesType[i])
		if(len(_attributesFiltered) == 0):
			c.warning("No attributes")
			self._SetupDelete()
			return
		
		# Keyframe target attributes
		c.setKeyframe(_item, attribute = _attributesFiltered)

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
		c.setAttr(self.nucleus + ".startFrame", _startTime) # TODO bug when select ovlp objects
		
		# Start logic
		_name = "_rebake_" + self.ConvertText(_item)
		_clone = c.duplicate(_item, name = _name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		for attr in OVLP.attributesT:
			c.setAttr(_clone[0] + "." + attr, lock = False)
		for attr in OVLP.attributesR:
			c.setAttr(_clone[0] + "." + attr, lock = False)
		c.parentConstraint(parent, _clone, maintainOffset = True) # skipTranslate
		c.select(_clone, replace = True)
		
		# Bake
		OVLP.BakeSelected()
		_children = c.listRelatives(_clone, type = "constraint")
		for child in _children: c.delete(child)
		
		# Copy keys, check layer and paste keys
		c.copyKey(_clone, time = (self.time[2], self.time[3]), attribute = _attributesFiltered)
		if (self.checkboxLayer.Get()):
			_animLayer = self._LayerCreate(_item)
			_attrsLayer = []
			for item in _attributesFiltered:
				_attrsLayer.append("{0}.{1}".format(_item, item))
			c.animLayer(_animLayer, edit = True, attribute = _attrsLayer)
			c.pasteKey(_item, option = "replace", attribute = _attributesFiltered, animLayer = _animLayer)
		else:
			c.pasteKey(_item, option = "replaceCompletely", attribute = _attributesFiltered)
		c.delete(_clone)
		
		# Set time range
		if (self.checkboxLoop.Get()):
			_startTime = self.time[2]
			c.setAttr(self.nucleus + ".startFrame", _startTime)
			self.TimeRangeReset()
			c.setInfinity(_item, preInfinite = "cycle", postInfinite = "cycle")
		else:
			c.setInfinity(_item, preInfinite = "constant", postInfinite = "constant")
		
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
		_selected = c.ls(selection = True) # type = "transform"
		if (len(_selected) == 0):
			if (self.selected == ""): return None
			return 0, None
		else:
			if (self.checkboxHierarchy.Get()):
				self.SelectTransformHierarchy()
				_selected = c.ls(selection = True)
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
				c.select(_selected[1][ii], replace = True)
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
			c.select(_selected[1], replace = True)
	def _BakeVariantComboTR(self, *args):
		self._BakeVariants(1)
		self._BakeVariants(3)
	def _BakeVariantComboRT(self, *args):
		self._BakeVariants(3)
		self._BakeVariants(1)
	def _BakeWorldLocator(self, *args):
		_selected = c.ls(selection = True) # Get selected objects
		if (len(_selected) == 0):
			c.warning("You must select at least 1 object")
			return
		else:
			if (self.checkboxHierarchy.Get()):
				self.SelectTransformHierarchy()
				_selected = c.ls(selection = True)
		_locators = []
		for item in _selected: # Create locator
			_name = OVLP.nameBakedWorldLocator + "1"
			_locator = c.spaceLocator(name = _name)[0]
			c.matchTransform(_locator, item, position = True, rotation = True)
			c.parentConstraint(item, _locator, maintainOffset = True)
			c.scaleConstraint(item, _locator, maintainOffset = True)
			_scale = 50
			c.setAttr(_locator + "Shape.localScaleX", _scale)
			c.setAttr(_locator + "Shape.localScaleY", _scale)
			c.setAttr(_locator + "Shape.localScaleZ", _scale)
			_locators.append(_locator)
		c.select(_locators, replace = True) # Bake and cleanup
		OVLP.BakeSelected()
		for loc in _locators:
			_children = c.listRelatives(loc, type = "constraint")
			for child in _children:
				c.delete(child)

	### LAYERS
	def _LayerCreate(self, obj, *args):
		# Create main layer
		if(not c.objExists(OVLP.nameLayers[0])):
			self.layers[0] = c.animLayer(OVLP.nameLayers[0], override = True)
		# Create layers on selected
		_name = OVLP.nameLayers[2] + self.ConvertText(obj) + "_1"
		return c.animLayer(_name, override = True, parent = self.layers[0])
	def _LayerMoveToSafeOrBase(self, safeLayer=True, *args):
		_id = [0, 1]
		if (not safeLayer): _id = [1, 0]
		_layer1 = OVLP.nameLayers[_id[0]]
		_layer2 = OVLP.nameLayers[_id[1]]

		# Check source layer
		if(not c.objExists(_layer1)):
			c.warning("Layer '{0}' doesn't exist".format(_layer1))
			return
		# Get selected layers
		_selectedLayers = []
		for animLayer in c.ls(type = "animLayer"):
			if c.animLayer(animLayer, query = True, selected = True):
				_selectedLayers.append(animLayer)
		# Check selected count
		_children = c.animLayer(self.layers[_id[0]], query = True, children = True)
		_filteredLayers = []
		if (len(_selectedLayers) == 0):
			if (_children == None):
				c.warning("Layer '{0}' is empty".format(_layer1))
				return
			else:
				for layer in _children:
					_filteredLayers.append(layer)
		else:
			if (_children == None):
				c.warning("Layer '{0}' is empty".format(_layer1))
				return
			else:
				for layer1 in _children:
					for layer2 in _selectedLayers:
						if (layer1 == layer2):
							_filteredLayers.append(layer1)
			if (len(_filteredLayers) == 0):
				c.warning("Nothing to move")
				return
		# Create safe layer
		if(not c.objExists(_layer2)):
			self.layers[_id[1]] = c.animLayer(_layer2, override = True)
		# Move children or selected layers
		for layer in _filteredLayers:
			c.animLayer(layer, edit = True, parent = self.layers[_id[1]])
		# Delete base layer if no children
		if (len(_filteredLayers) == len(_children)):
			self._LayerDelete(_layer1)
	def _LayerDelete(self, name, *args):
		if(c.objExists(name)):
			c.delete(name)
			print("Layer '{0}' deleted".format(name))
		else:
			c.warning("Layer '{0}' doesn't exist".format(name))
	def _LayerCreate_TEST(self, *args):
		# Check selected
		_selected = c.ls(selection = True)
		if (len(_selected) == 0):
			c.warning("You must select at least 1 object")
			return
		# Create main layer
		if(not c.objExists(OVLP.nameLayers[0])):
			self.layers[0] = c.animLayer(OVLP.nameLayers[0], override = True)
		# Create layers on selected
		for item in _selected:
			_name = OVLP.nameLayers[2] + self.ConvertText(item) + "_1"
			c.animLayer(_name, override = True, parent = self.layers[0])

	### DEV TOOLS
	def _DEVFunction(self, *args):
		print("DEV Function")
	def _MotionTrailCreate(self, *args):
		_selected = c.ls(selection = True) # Get selected objects
		if (len(_selected) == 0):
			c.warning("You must select at least 1 object")
			return
		_name = "MotionTrail_1"
		_step = 1
		_start = c.playbackOptions(query = True, minTime = True)
		_end = c.playbackOptions(query = True, maxTime = True)
		c.snapshot(name = _name, motionTrail = True, increment = _step, startTime = _start, endTime = _end)
		_trails = c.ls(type = "motionTrail")
		for item in _trails:
			c.setAttr(item + "Handle" + "Shape.trailDrawMode", 1)
			c.setAttr(item + "Handle" + "Shape.template", 1)
	def _MotionTrailSelect(self, *args):
		_trails = c.ls(type = "motionTrail")
		if (len(_trails) == 0): return
		c.select(clear = True)
		for item in _trails:
			c.select(item + "Handle", add = True)
	def _MotionTrailDelete(self, *args):
		_trails = c.ls(type = "motionTrail")
		if (len(_trails) == 0): return
		for item in _trails:
			c.delete(item + "Handle")

	### EXECUTION
	def Start(self, *args):
		_OVERLAPPY.CreateUI()
	def Restart(self, *args):
		c.evalDeferred("_OVERLAPPY.Start()")

_OVERLAPPY = OVLP()
_OVERLAPPY.Start()