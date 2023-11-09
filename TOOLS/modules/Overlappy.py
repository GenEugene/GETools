import maya.cmds as cmds
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
		if cmds.window(OVLP.nameWindowMain, exists = True):
			cmds.deleteUI(OVLP.nameWindowMain)
		self.windowMain = cmds.window(OVLP.nameWindowMain, title = OVLP.textTitle, maximizeButton = 0, sizeable = 0, resizeToFitChildren = True, widthHeight = (OVLP.windowWidth, OVLP.windowHeight * 6))
		self.layoutMain = cmds.columnLayout(adjustableColumn = True, height = OVLP.windowHeight)

		# CLASSES
		class classCheckbox:
			def __init__(self, label="label", value=False, command="pass", menuReset=True, enabled=True, ccResetAll="pass"):
				self.value = value
				self.checkbox = cmds.checkBox(label = label, value = value, changeCommand = command, enable = enabled)
				cmds.popupMenu()
				if (menuReset):
					cmds.menuItem(label = "reset current", command = self.Reset)
					cmds.menuItem(label = "reset all", command = ccResetAll)
			def Get(self, *args):
				return cmds.checkBox(self.checkbox, query = True, value = True)
			def Set(self, value=None, *args):
				cmds.checkBox(self.checkbox, edit = True, value = value)
			def Reset(self, *args):
				cmds.checkBox(self.checkbox, edit = True, value = self.value)
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
				cmds.flowLayout(parent = parent)
				self.slider = cmds.floatSliderGrp(label = " " + label, value = self.value, changeCommand = self.command, dragCommand = self.command, fieldMinValue = minMax[0], fieldMaxValue = minMax[1], minValue = minMax[2], maxValue = minMax[3], field = True,
														precision = self.precision, width = OVLP.windowWidth - OVLP.markerWidth, columnAlign = (1, "left"), columnWidth3 = (OVLP.sliderWidth[0], OVLP.sliderWidth[1], OVLP.sliderWidth[2]), enableKeyboardFocus = True)
				cmds.popupMenu(parent = self.slider)
				if (menuReset):
					cmds.menuItem(label = "reset current", command = self.Reset)
					cmds.menuItem(label = "reset all", command = ccResetAll)
				if (menuScan):
					cmds.menuItem(divider = True)
					cmds.menuItem(label = "scan current", command = self.Scan)
					cmds.menuItem(label = "scan all", command = ccScanAll)
				self._marker = cmds.button(label = "", enable = 0, w = OVLP.markerWidth, backgroundColor = self.markerColorDefault)
			def Get(self, *args):
				return cmds.floatSliderGrp(self.slider, query = True, value = True)
			def Set(self, value=None, *args):
				if (value == None): _value = cmds.floatSliderGrp(self.slider, query = True, value = True)
				else:
					_value = value
					cmds.floatSliderGrp(self.slider, edit = True, value = _value)
					self.command()
				# Marker update
				if (_value != self.value):
					cmds.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
				else:
					cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
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
					cmds.setAttr(_selectedName + self.attribute, _value)
				except:
					# print("Can't set value")
					pass
			def Reset(self, *args):
				cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
				cmds.floatSliderGrp(self.slider, edit = True, value = self.value)
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
					_value = cmds.getAttr(_firstName + self.attribute)
					cmds.floatSliderGrp(self.slider, edit = True, value = _value)
				except:
					# print("Can't get value")
					return
				# Marker update
				if (round(_value, 3) != self.value):
					cmds.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
				else:
					cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
			def GetCached(self, *args):
				return self.valueCached
			def SetCached(self, *args):
				self.valueCached = cmds.floatSliderGrp(self.slider, query = True, value = True)
			def ResetCached(self, *args):
				self.valueCached = 0

		# HEAD MENU
		cmds.menuBarLayout()
		#
		# cmds.menu(label = "Settings")
		# cmds.menuItem(label = "Save")
		# cmds.menuItem(label = "Save as")
		# cmds.menuItem(label = "Load")
		# cmds.menuItem(divider = True)
		# cmds.menuItem(label = "Reset")
		#
		cmds.menu(label = "Scene")
		cmds.menuItem(label = "Reload", command = self.SceneReload)
		cmds.menuItem(dividerLabel = "Be careful", divider = True)
		cmds.menuItem(label = "Quit", command = self.SceneQuit)
		#
		cmds.menu(label = "Script")
		cmds.menuItem(label = "Reload", command = self.Restart)
		cmds.menuItem(dividerLabel = "Layouts", divider = True)
		cmds.menuItem(label = "Collapse all", command = partial(self.LayoutsCollapseLogic, True))
		cmds.menuItem(label = "Expand all", command = partial(self.LayoutsCollapseLogic, False))
		cmds.menuItem(dividerLabel = "Other", divider = True)
		cmds.menuItem(label = "Dev Tools toggle", command = self.LayoutDevToolsToggle, checkBox = False)
		#
		cmds.menu(label = "Help")
		def LinkPatreon(self): cmds.showHelp("https://www.patreon.com/geneugene", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://app.gumroad.com/geneugene", absolute = True)
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/Overlappy", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://www.youtube.com/channel/UCCIzdVu6RMqUoOmxHoOEPAQ", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/Overlappy/discussions/categories/report-a-problem", absolute = True)
		cmds.menuItem(label = "About Overlappy", enable = False) # TODO add window with information
		cmds.menuItem(dividerLabel = "Links", divider = True)
		# cmds.menuItem(label = "Discord")
		cmds.menuItem(label = "Patreon", command = LinkPatreon)
		cmds.menuItem(label = "Gumroad", command = LinkGumroad)
		cmds.menuItem(label = "GitHub", command = LinkGithub)
		cmds.menuItem(label = "YouTube", command = LinkYoutube)
		cmds.menuItem(dividerLabel = "Support", divider = True)
		cmds.menuItem(label = "Report a Problem...", command = LinkReport)
		
		# BUTTONS
		self.layoutButtons = cmds.frameLayout(label = "BUTTONS", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		cmds.gridLayout(parent = self.layoutButtons, numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		cmds.button(label = "RESET ALL", command = self._ResetAllValues, backgroundColor = OVLP.cYellow)
		cmds.button(label = "SELECT", command = self.SelectTransformHierarchy, backgroundColor = OVLP.cLBlue)
		cmds.popupMenu()
		cmds.menuItem(dividerLabel = "Created objects", divider = True)
		cmds.menuItem(label = "Objects", command = self._SelectObjects)
		cmds.menuItem(label = "Particle", command = self._SelectParticle)
		cmds.menuItem(label = "Nucleus", command = self._SelectNucleus)
		cmds.menuItem(label = "Target", command = self._SelectTarget)
		cmds.menuItem(label = "Aim", command = self._SelectAim)
		cmds.button(label = "LAYERS", command = partial(self._LayerMoveToSafeOrBase, True), backgroundColor = OVLP.cBlue) # _LayerCreate_TEST - old func for tests
		cmds.popupMenu()
		cmds.menuItem(dividerLabel = "Move", divider = True)
		cmds.menuItem(label = "Move to Base layer", command = partial(self._LayerMoveToSafeOrBase, False))
		cmds.menuItem(dividerLabel = "Delete", divider = True)
		cmds.menuItem(label = "Delete '{0}'".format(OVLP.nameLayers[0]), command = partial(self._LayerDelete, OVLP.nameLayers[0]))
		cmds.menuItem(label = "Delete '{0}'".format(OVLP.nameLayers[1]), command = partial(self._LayerDelete, OVLP.nameLayers[1]))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Delete 'BaseAnimation'", command = partial(self._LayerDelete, "BaseAnimation"))
		cmds.button(label = "SETUP", command = self._SetupInit, backgroundColor = OVLP.cGreen)
		cmds.popupMenu()
		cmds.menuItem(label = "Scan setup into scene", command = self._SetupScan)
		cmds.menuItem(dividerLabel = "Delete", divider = True)
		cmds.menuItem(label = "Delete setup", command = self._SetupDelete)
		
		# BAKING
		# self.layoutBaking = cmds.frameLayout(label = "BAKING", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		# cmds.gridLayout(parent = self.layoutButtons, numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		cmds.button(label = "TRANSLATION", command = partial(self._BakeVariants, 1), backgroundColor = OVLP.cLOrange)
		cmds.popupMenu()
		cmds.menuItem(label = "use offset", command = partial(self._BakeVariants, 2))
		cmds.button(label = "ROTATION", command = partial(self._BakeVariants, 3), backgroundColor = OVLP.cLOrange)
		cmds.button(label = "COMBO", command = partial(self._BakeVariants, 4), backgroundColor = OVLP.cLOrange)
		cmds.popupMenu()
		cmds.menuItem(label = "translate + rotate", command = self._BakeVariantComboTR)
		cmds.menuItem(label = "rotate + translate", command = self._BakeVariantComboRT)
		# cmds.gridLayout(parent = self.layoutBaking, numberOfColumns = 2, cellWidthHeight = (OVLP.windowWidth / 2, OVLP.lineHeight))
		cmds.button(label = "TO LOCATOR", command = self._BakeWorldLocator, backgroundColor = OVLP.cOrange)

		# OPTIONS
		# self.layoutOptions = cmds.frameLayout(label = "OPTIONS", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		# cmds.gridLayout(parent = self.layoutButtons, numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		_optionsResetAll = self._ResetOptions
		self.checkboxHierarchy = classCheckbox(label = "HIERARCHY", value = OVLP.checkboxesOptions[0], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxLayer = classCheckbox(label = "LAYER", value = OVLP.checkboxesOptions[1], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxLoop = classCheckbox(label = "LOOP", value = OVLP.checkboxesOptions[2], menuReset = True, ccResetAll = _optionsResetAll)
		self.checkboxClean = classCheckbox(label = "CLEAN", value = OVLP.checkboxesOptions[3], menuReset = True, ccResetAll = _optionsResetAll)

		# SIMULATION SETTINGS
		self.layoutSimulation = cmds.frameLayout(label = "SIMULATION", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		cmds.columnLayout(parent = self.layoutSimulation)
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
		self.layoutOffset = cmds.frameLayout(label = "OFFSET", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack)
		cmds.gridLayout(numberOfColumns = 4, cellWidthHeight = (OVLP.windowWidth / 4, OVLP.lineHeight))
		cmds.separator()
		self.checkboxMirrorX = classCheckbox(label = "MIRROR X", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		self.checkboxMirrorY = classCheckbox(label = "MIRROR Y", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		self.checkboxMirrorZ = classCheckbox(label = "MIRROR Z", command = partial(self._OffsetsUpdate, True), menuReset = True, enabled = True, ccResetAll = self._ResetOffsets)
		cmds.columnLayout(parent = self.layoutOffset)
		_offStartName = OVLP.nameLocGoalTarget[0]
		_offParent = self.layoutOffset
		_offCCDefault = self._OffsetsUpdate
		_offCCReset = self._ResetOffsets
		_offCCGetValues = self._GetOffsets
		self.sliderOffsetX = classSlider(label = "   Local X", attribute = "_parentConstraint1.target[0].targetOffsetTranslateX", startName = _offStartName, minMax = OVLP.rangeOffsetX, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
		self.sliderOffsetY = classSlider(label = "   Local Y", attribute = "_parentConstraint1.target[0].targetOffsetTranslateY", startName = _offStartName, minMax = OVLP.rangeOffsetY, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)
		self.sliderOffsetZ = classSlider(label = "   Local Z", attribute = "_parentConstraint1.target[0].targetOffsetTranslateZ", startName = _offStartName, minMax = OVLP.rangeOffsetZ, parent = _offParent, command = _offCCDefault, ccResetAll = _offCCReset, ccScanAll = _offCCGetValues)

		# DEV TOOLS
		self.layoutDevTools = cmds.frameLayout(label = "DEV TOOLS", parent = self.layoutMain, collapseCommand = self.Resize_UI, expandCommand = self.Resize_UI, collapsable = True, borderVisible = True, backgroundColor = OVLP.cBlack, visible = False)
		cmds.gridLayout(parent = self.layoutDevTools, numberOfColumns = 3, cellWidthHeight = (OVLP.windowWidth / 3, OVLP.lineHeight))
		cmds.button(label = "DEV FUNCTION", command = self._DEVFunction, backgroundColor = OVLP.cBlack)
		cmds.button(label = "MOTION TRAIL", command = self._MotionTrailCreate, backgroundColor = OVLP.cBlack)
		cmds.popupMenu()
		cmds.menuItem(label = "Select", command = self._MotionTrailSelect)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Delete", command = self._MotionTrailDelete)

		# RUN WINDOW
		cmds.showWindow(self.windowMain)
		self.Resize_UI()
	
	def UILayout(self, layoutMain): # TODO
		pass
		# settings = GeneralWindow.GeneralWindow()
		# windowWidthMargin = settings.windowWidthMargin
		# minMaxWeight = settings.minMaxWeight
		
		
	def Resize_UI(self, *args): # TODO get count of visible layouts
		cmds.window(self.windowMain, edit = True, height = 152, resizeToFitChildren = True) # OVLP.windowHeight * 6
	
	def LayoutsCollapseLogic(self, value, *args): # TODO to external class
		if (value):
			if (self.LayoutsCollapseCheck() == value):
				return
		else:
			if (self.LayoutsCollapseCheck() == value):
				return
		cmds.frameLayout(self.layoutButtons, edit = True, collapse = value)
		# cmds.frameLayout(self.layoutBaking, edit = True, collapse = value)
		# cmds.frameLayout(self.layoutOptions, edit = True, collapse = value)
		cmds.frameLayout(self.layoutSimulation, edit = True, collapse = value)
		cmds.frameLayout(self.layoutOffset, edit = True, collapse = value)
		cmds.frameLayout(self.layoutDevTools, edit = True, collapse = value)
		self.Resize_UI()
	def LayoutsCollapseCheck(self, *args): # needed to fix the window bug
		check1 = cmds.frameLayout(self.layoutButtons, query = True, collapse = True)
		# check2 = cmds.frameLayout(self.layoutBaking, query = True, collapse = True)
		# check3 = cmds.frameLayout(self.layoutOptions, query = True, collapse = True)
		check4 = cmds.frameLayout(self.layoutSimulation, query = True, collapse = True)
		check5 = cmds.frameLayout(self.layoutOffset, query = True, collapse = True)
		check6 = cmds.frameLayout(self.layoutDevTools, query = True, collapse = True)
		# if (check1 == check2 == check3 == check4 == check5 == check6):
		if (check1 == check4 == check5 == check6):
			return check1
	def LayoutDevToolsToggle(self, *args):
		_value = cmds.frameLayout(self.layoutDevTools, query = True, visible = True)
		cmds.frameLayout(self.layoutDevTools, edit = True, visible = not _value)
		self.Resize_UI()
	
	def SceneReload(self, *args): # TODO to external class
		currentScene = cmds.file(query = True, sceneName = True)
		if(currentScene): cmds.file(currentScene, open = True, force = True)
		else: cmds.file(new = True, force = True)
	def SceneQuit(self, *args): # TODO to external class
		cmds.quit(force = True)
	
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

	def SelectTransformHierarchy(self, *args):# TODO from GETools class (need to merge in future)
		_selected = cmds.ls(selection = True)
		if (len(_selected) == 0):
			cmds.warning("You must select at least 1 object")
			return
		cmds.select(hierarchy = True)
		list = cmds.ls(selection = True, type = "transform", shapes = False)
		cmds.select(clear = True)
		for i in range(len(list)):
			cmds.select(list[i], add = True)
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
		if (cmds.objExists(OVLP.nameGroup)):
			cmds.delete(OVLP.nameGroup)
		cmds.group(empty = True, name = OVLP.nameGroup)
		# Run setup logic
		self._SetupCreate(self.selected)
		self._OffsetsUpdate(cacheReset = True)
		cmds.select(self.selected, replace = True)
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
		self.locGoalTarget[0] = cmds.spaceLocator(name = nameLocGoal)[0]
		cmds.parent(self.locGoalTarget[0], OVLP.nameGroup)
		cmds.matchTransform(self.locGoalTarget[0], objCurrent, position = True, rotation = True)
		cmds.parentConstraint(objCurrent, self.locGoalTarget[0], maintainOffset = True)
		cmds.setAttr(self.locGoalTarget[0] + ".visibility", 0)
		self.startPositionGoalParticle[0] = cmds.xform(self.locGoalTarget[0], query = True, translation = True)

		# Create particle, goal and get selected object position
		_position = cmds.xform(objCurrent, query = True, worldSpace = True, rotatePivot = True)
		self.particle = cmds.nParticle(name = nameParticle, position = _position, conserve = 1)[0]
		cmds.goal(useTransformAsGoal = True, goal = self.locGoalTarget[0])
		cmds.parent(self.particle, OVLP.nameGroup)
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
		cmds.parent(self.nucleus, OVLP.nameGroup)
		self.sliderNTimeScale.startName = self.nucleus
		cmds.setAttr(self.nucleus + ".gravity", 0)
		cmds.setAttr(self.nucleus + ".timeScale", self.sliderNTimeScale.Get())
		cmds.setAttr(self.nucleus + ".startFrame", self.time[2])
		cmds.setAttr(self.nucleus + ".visibility", 0)

		# Create and connect locator to particle
		self.locGoalTarget[1] = cmds.spaceLocator(name = nameLocParticle)[0]
		cmds.parent(self.locGoalTarget[1], OVLP.nameGroup)
		cmds.matchTransform(self.locGoalTarget[1], objCurrent, position = True, rotation = True)
		cmds.connectAttr(self.particle + ".center", self.locGoalTarget[1] + ".translate", force = True)
		cmds.setAttr(self.locGoalTarget[1] + ".visibility", 0)

		# Create base aim locator
		self.locAim[0] = cmds.spaceLocator(name = nameLocAimBase)[0]
		cmds.parent(self.locAim[0], OVLP.nameGroup)
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
		_scale2 = self.sliderPRadius.Get() * OVLP.loftFactor
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
		cmds.parent(self.loft[2], OVLP.nameGroup)
		cmds.setAttr(self.loft[2] + ".overrideEnabled", 1)
		cmds.setAttr(self.loft[2] + ".overrideDisplayType", 2)
		cmds.setAttr(self.loft[2] + ".overrideShading", 0)
		if (self._LoftGetDistance() < OVLP.loftMinDistance):
			cmds.setAttr(self.loft[2] + ".visibility", 0)
	def _SetupScan(self, *args):
		# Check overlappy group
		if (not cmds.objExists(OVLP.nameGroup)):
			cmds.warning("Overlappy object doesn't exists")
			return
		# Get children of group
		_children = cmds.listRelatives(OVLP.nameGroup)
		if (len(_children) == 0):
			cmds.warning("Overlappy object has no children objects")
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
					else: cmds.warning("Suffix '{0}' don't equals to '{1}'".format(_objectName, _lastName))
		_converted = self.ConvertText(_objectName, False)
		if (cmds.objExists(_converted)):
			self.selected = _converted
		
		def CheckAndSet(name):
			if (cmds.objExists(name + _objectName)):
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
		if (cmds.objExists(OVLP.nameGroup)):
			cmds.delete(OVLP.nameGroup)
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
		_particleAttributes[0] = OVLP.nameParticle + self.ConvertText(self.selected) + ".translateX"
		_particleAttributes[1] = OVLP.nameParticle + self.ConvertText(self.selected) + ".translateY"
		_particleAttributes[2] = OVLP.nameParticle + self.ConvertText(self.selected) + ".translateZ"
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
		_scale = self.sliderPRadius.Get() * OVLP.loftFactor
		cmds.setAttr(self.loft[1] + ".scaleX", _scale)
		cmds.setAttr(self.loft[1] + ".scaleY", _scale)
		cmds.setAttr(self.loft[1] + ".scaleZ", _scale)
		if (self._LoftGetDistance() < OVLP.loftMinDistance): cmds.setAttr(self.loft[2] + ".visibility", 0)
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
		if (translation): _attributesType = OVLP.attributesT
		else: _attributesType = OVLP.attributesR
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
					if(_type in OVLP.constraintsNames):
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
		_name = "_rebake_" + self.ConvertText(_item)
		_clone = cmds.duplicate(_item, name = _name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		for attr in OVLP.attributesT:
			cmds.setAttr(_clone[0] + "." + attr, lock = False)
		for attr in OVLP.attributesR:
			cmds.setAttr(_clone[0] + "." + attr, lock = False)
		cmds.parentConstraint(parent, _clone, maintainOffset = True) # skipTranslate
		cmds.select(_clone, replace = True)
		
		# Bake
		OVLP.BakeSelected()
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
			_name = OVLP.nameBakedWorldLocator + "1"
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
		OVLP.BakeSelected()
		for loc in _locators:
			_children = cmds.listRelatives(loc, type = "constraint")
			for child in _children:
				cmds.delete(child)

	### LAYERS
	def _LayerCreate(self, obj, *args):
		# Create main layer
		if(not cmds.objExists(OVLP.nameLayers[0])):
			self.layers[0] = cmds.animLayer(OVLP.nameLayers[0], override = True)
		# Create layers on selected
		_name = OVLP.nameLayers[2] + self.ConvertText(obj) + "_1"
		return cmds.animLayer(_name, override = True, parent = self.layers[0])
	def _LayerMoveToSafeOrBase(self, safeLayer=True, *args):
		_id = [0, 1]
		if (not safeLayer): _id = [1, 0]
		_layer1 = OVLP.nameLayers[_id[0]]
		_layer2 = OVLP.nameLayers[_id[1]]

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
		if(not cmds.objExists(OVLP.nameLayers[0])):
			self.layers[0] = cmds.animLayer(OVLP.nameLayers[0], override = True)
		# Create layers on selected
		for item in _selected:
			_name = OVLP.nameLayers[2] + self.ConvertText(item) + "_1"
			cmds.animLayer(_name, override = True, parent = self.layers[0])

	### DEV TOOLS
	def _DEVFunction(self, *args):
		print("DEV Function")
	def _MotionTrailCreate(self, *args):
		_selected = cmds.ls(selection = True) # Get selected objects
		if (len(_selected) == 0):
			cmds.warning("You must select at least 1 object")
			return
		_name = "MotionTrail_1"
		_step = 1
		_start = cmds.playbackOptions(query = True, minTime = True)
		_end = cmds.playbackOptions(query = True, maxTime = True)
		cmds.snapshot(name = _name, motionTrail = True, increment = _step, startTime = _start, endTime = _end)
		_trails = cmds.ls(type = "motionTrail")
		for item in _trails:
			cmds.setAttr(item + "Handle" + "Shape.trailDrawMode", 1)
			cmds.setAttr(item + "Handle" + "Shape.template", 1)
	def _MotionTrailSelect(self, *args):
		_trails = cmds.ls(type = "motionTrail")
		if (len(_trails) == 0): return
		cmds.select(clear = True)
		for item in _trails:
			cmds.select(item + "Handle", add = True)
	def _MotionTrailDelete(self, *args):
		_trails = cmds.ls(type = "motionTrail")
		if (len(_trails) == 0): return
		for item in _trails:
			cmds.delete(item + "Handle")

	### EXECUTION
	def Start(self, *args):
		_OVERLAPPY.CreateUI()
	def Restart(self, *args):
		cmds.evalDeferred("_OVERLAPPY.Start()")
	
	# # EXECUTION
	# def RUN(self, *args):
	# 	self.CreateUI()

_OVERLAPPY = OVLP()
_OVERLAPPY.Start()