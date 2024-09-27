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
from ..utils import Animation
from ..utils import Attributes
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
from ..experimental import Physics
from ..experimental import PhysicsParticle


class OverlappyAnnotations:
	### Setup
	setupEnding = "Tweak values to preview the simulation.\nTo bake the rig, deselect all and press any bake button."
	setupPoint = "Simple particle rig for translation.\n" + setupEnding
	setupAim = "Aim rig for rotation using 2 particles: 1 for aim target, 1 for aim up.\n" + setupEnding
	setupCombo = "Combined rig for translation and rotation using 3 particles: 1 for translation, 1 for aim target, and 1 for aim up.\n" + setupEnding
	setupDelete = "Delete particle rig if it exists"

	### Baking
	bakeTranslation = "Bake point rig for translation attributes"
	bakeRotation = "Bake aim rig for rotation attributes"
	bakeCombo = "Bake combo rig for translation and rotation attributes"
	bakeCurrent = "Bake current rig if exist"
	# bakeScale = "Bake simulation for scale attributes"

	### Layers
	layerDeleteAll = "All animation layers will be deleted."
	layerDeleteTemp = "Only the Temp layer and its child layers will be deleted."
	layerDeleteSafe = "Only the Safe layer and its child layers will be deleted."
	layerMoveTemp = "Move Temp layer sublayers to the Safe layer."
	layerMoveSafe = "Move Safe layer sublayers to the Temp layer."

	### Options
	# checkboxHierarchy = "Bake simulation for all child hierarhy of selected objects"
	# checkboxLayer = "Bake animation into override layers. \nIf turned off animation will be baked directly to selected objects"
	# checkboxLoop = "Use for cycles. \nImportant to have cycle constant animation curves"
	# checkboxClean = "Remove particle setup after baking end"

	### Collisions
	# checkboxCollisions = "Use collisions"

	### Nucleus
	particleTimeScale = "Nucleus Time Scale"

	### Aim Offset
	aimOffset = "Particle offset from original object.\nHighly important to use non zero values for \"Aim\" and \"Combo\" modes."
	aimOffsetValue = "Offset value"
	aimOffsetAxis = "Positive axis for offset"
	aimOffsetReverse = "Reverse axis direction from positive to negative"

	### Particle
	particleRadius = "Particle sphere size. Just visual, no physics influence."
	particleGoalSmooth = "This value is used to control the \"smoothness\" of the change in the goal forces as the weight changes from 0.0 to 1.0.\nThis is purely an aesthetic effect, with no scientific basis.\nThe higher the number, the smoother the change."
	particleGoalWeight = "Particle Goal Weight. Value 1 means 100% of stiffness."
	particleConserve = "The Conserve value controls how much of a particle object's velocity is retained from frame to frame.\nSpecifically, Conserve scales a particle's velocity attribute at the beginning of each frame's execution.\nAfter scaling the velocity, Maya applies any applicable dynamics to the particles to create the final positioning at the end of the frame."
	particleDrag = "Specifies the amount of drag applied to the current nParticle object.\nDrag is the component of aerodynamic force parallel to the relative wind which causes resistance.\nDrag is 0.05 by default."
	particleDamp = "Specifies the amount the motion of the current nParticles are damped.\nDamping progressively diminishes the movement and oscillation of nParticles by dissipating energy."

class OverlappySettings: # TODO simplify and move to preset
	### NAMING
	prefix = "ovlp"
	nameGroup = prefix + "Group"
	prefixLayer = "_" + prefix
	nameLayers = (prefixLayer + "TEMP_", prefixLayer + "SAFE_", prefixLayer + "_")
		
	### SETTINGS CHECKBOXES
	optionCheckboxHierarchy = False
	optionCheckboxLayer = True
	optionCheckboxLoop = False
	optionCheckboxDeleteSetup = True
	optionCheckboxCollisions = True

	### SETTINGS NUCLEUS
	nucleusTimeScale = 1
	nucleusGravityActivated = False
	nucleusGravityValue = 9.81
	nucleusGravityDirection = (0, -1, 0)

	### PARTICLE AIM OFFSET
	particleAimOffsetsAxes = (0, 1) # Aim X, Up Y
	particleAimOffsetsValues = (10, 10) # Aim, Up

	### SETTINGS DYNAMIC PROPERTIES
	particleRadius = 1
	particleGoalSmooth = 1
	particleGoalWeight = 0.3
	particleConserve = 1
	particleDrag = 0.01
	particleDamp = 0
		
	### SLIDERS (field min/max, slider min/max)
	rangeNucleusTimeScale = (0.001, float("inf"), 0.001, 1)
	rangePRadius = (0, float("inf"), 0, 10)
	rangeGSmooth = (0, float("inf"), 0, 2)
	rangeGWeight = (0, 1, 0, 1)
	rangePConserve = (0, 1, 0, 1)
	rangePDrag = (0, float("inf"), 0, 1)
	rangePDamp = (0, float("inf"), 0, 1)

class Overlappy:
	_version = "v3.0"
	_name = "OVERLAPPY"
	_title = _name + " " + _version

	# HACK use only for code editor # TODO try to find better way to get access to other classes with cross import
	# from ..modules import GeneralWindow
	# def __init__(self, generalInstance: GeneralWindow.GeneralWindow):
	def __init__(self, generalInstance):
		self.generalInstance = generalInstance

		### VALUES
		self.setupCreated = False
		self.setupCreatedPoint = False
		self.setupCreatedAim = False
		self.setupCreatedCombo = False

		self.time = Timeline.TimeRangeHandler()
		
		### OBJECTS
		self.selectedObjects = ""
		self.layers = ["", ""]
		self.nucleus1 = ""
		self.nucleus2 = ""
		self.bakingObject = ""
		## self.colliderObjects = [] # TODO
		## self.colliderNodes = [] # TODO

		### PARTICLE SIMULATION OBJECTS
		self.particleAimOffsetTarget = [0, 0, 0]
		self.particleAimOffsetUp = [0, 0, 0]
		self.particleBase = ""
		self.particleTarget = ""
		self.particleUp = ""
		self.particleLocator = ""
		self.particleLocatorGoalOffset = ""
		self.particleLocatorGoalOffsetUp = ""
		self.particleLocatorAim = ""
		self.particleLocatorGoalOffsetStartPosition = (0, 0, 0)
		self.particleLocatorGoalOffsetUpStartPosition = (0, 0, 0)
		
		### UI LAYOUTS
		self.layoutLayers = None
		# self.layoutCollisions = None # TODO
		# self.layoutChainMode = None # TODO
		# self.layoutChainButtons = None # TODO
		# self.layoutChainDynamicProperties = None # TODO
		self.layoutNucleusProperties = None
		self.layoutParticleMode = None
		self.layoutParticleButtons = None
		self.layoutParticleOffset = None
		self.layoutParticleDynamicProperties = None
		
		### UI MENU OPTIONS
		self.menuCheckboxHierarchy = None
		self.menuCheckboxLayer = None
		self.menuCheckboxLoop = None
		self.menuCheckboxDeleteSetup = None
		# self.menuCheckboxCollisions = None # TODO
		self.menuRadioButtonsLoop = [None, None, None, None, None]

		### UI NUCLEUS PROPERTIES
		self.nucleusTimeScaleSlider = None
		self.nucleusGravityCheckbox = None
		self.nucleusGravityFloatField = None
		self.nucleusGravityDirectionFloatFieldGrp = None

		### UI AIM OFFSET
		## self.checkboxAutoOffset = None # TODO
		self.aimOffsetFloatGroup = [None, None] # text, float
		self.aimOffsetRadioCollection = [None, None, None]
		self.aimOffsetCheckbox = None
		self.aimOffsetUpFloatGroup = [None, None] # text, float
		self.aimOffsetUpRadioCollection = [None, None, None]
		self.aimOffsetUpCheckbox = None
		
		### UI PARTICLE DYNAMIC PROPERTIES
		self.sliderParticleRadius = None
		self.sliderParticleGoalSmooth = None
		self.sliderParticleGoalWeight = None
		self.sliderParticleConserve = None
		self.sliderParticleDrag = None
		self.sliderParticleDamp = None

		### UI SCROLL LISTS
		self.scrollListColliders = None
	def UICreate(self, layoutMain):
		self.UILayoutMenuBar(layoutMain)
		self.UILayoutLayers(layoutMain)
		## self.UILayoutCollisions(layoutMain) # TODO
		## self.UILayoutChainMode(layoutMain) # TODO
		self.UILayoutNucleus(layoutMain)
		self.UILayoutParticle(layoutMain)


	### MAIN UI
	def UILayoutMenuBar(self, layoutMain):
		cmds.columnLayout(parent = layoutMain, adjustableColumn = True, width = Settings.windowWidthMargin)
		cmds.menuBarLayout()

		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Reset Settings", command = self.ResetAllSettings, image = Icons.rotateClockwise)
		
		cmds.menu(label = "Options", tearOff = True)
		self.menuCheckboxHierarchy = UI.MenuCheckbox(label = "Use Hierarchy", value = OverlappySettings.optionCheckboxHierarchy, valueDefault = OverlappySettings.optionCheckboxHierarchy)
		self.menuCheckboxLayer = UI.MenuCheckbox(label = "Bake To Override Layer", value = OverlappySettings.optionCheckboxLayer, valueDefault = OverlappySettings.optionCheckboxLayer)
		self.menuCheckboxLoop = UI.MenuCheckbox(label = "Loop", value = OverlappySettings.optionCheckboxLoop, valueDefault = OverlappySettings.optionCheckboxLoop)
		self.menuCheckboxDeleteSetup = UI.MenuCheckbox(label = "Delete Setup After Bake", value = OverlappySettings.optionCheckboxDeleteSetup, valueDefault = OverlappySettings.optionCheckboxDeleteSetup)
		# self.menuCheckboxCollisions = UI.MenuCheckbox(label = "Collisions", value = OverlappySettings.optionCheckboxCollisions, valueDefault = OverlappySettings.optionCheckboxCollisions)

		cmds.menuItem(dividerLabel = "Pre Loop Cycles", divider = True)
		cmds.radioMenuItemCollection()
		self.menuRadioButtonsLoop[0] = cmds.menuItem(label = "0", radioButton = True)
		self.menuRadioButtonsLoop[1] = cmds.menuItem(label = "1", radioButton = True)
		self.menuRadioButtonsLoop[2] = cmds.menuItem(label = "2", radioButton = True)
		self.menuRadioButtonsLoop[3] = cmds.menuItem(label = "3", radioButton = True)
		self.menuRadioButtonsLoop[4] = cmds.menuItem(label = "4", radioButton = True)
		cmds.menuItem(self.menuRadioButtonsLoop[2], edit = True, radioButton = True)

		cmds.menu(label = "Select", tearOff = True)
		cmds.menuItem(label = "Nucleus", command = self.SelectNucleus, image = Icons.nucleus)
		cmds.menuItem(label = "Particles", command = self.SelectParticles, image = Icons.particle)

	def UILayoutLayers(self, layoutMain):
		self.layoutLayers = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "LAYERS", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutLayers, adjustableColumn = True)

		sizesDelete = (120, 70, 70)
		cmds.rowLayout(parent = layoutColumn, numberOfColumns = 3, columnWidth3 = sizesDelete) # recomputeSize = True
		cmds.button(label = "Delete All Layers", width = sizesDelete[0], command = partial(Layers.Delete, "BaseAnimation"), backgroundColor = Colors.red50, annotation = OverlappyAnnotations.layerDeleteAll)
		cmds.button(label = "Delete Temp", width = sizesDelete[1], command = partial(Layers.Delete, OverlappySettings.nameLayers[0]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteTemp)
		cmds.button(label = "Delete Safe", width = sizesDelete[2], command = partial(Layers.Delete, OverlappySettings.nameLayers[1]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteSafe)

		sizesMove = (120, 120)
		cmds.rowLayout(parent = layoutColumn, numberOfColumns = 2, columnWidth2 = sizesMove)
		cmds.button(label = "Move To Safe Layer", width = sizesMove[0], command = partial(self.LayerMoveToSafeOrTemp, True), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveTemp)
		cmds.button(label = "Move To Temp Layer", width = sizesMove[1], command = partial(self.LayerMoveToSafeOrTemp, False), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveSafe)
	# def UILayoutCollisions(self, layoutMain): # TODO
	# 	self.layoutCollisions = cmds.frameLayout("layoutCollisions", label = Settings.frames2Prefix + "COLLISIONS - WORK IN PROGRESS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
	# 	layoutColumn = cmds.columnLayout(parent = self.layoutCollisions, adjustableColumn = True)
		
	# 	count = 4
	# 	cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
	# 	cmds.button(label = "Add", backgroundColor = Colors.green10)
	# 	cmds.button(label = "Remove", backgroundColor = Colors.red10)
	# 	cmds.button(label = "Refresh", backgroundColor = Colors.yellow10)
	# 	cmds.button(label = "Clear", backgroundColor = Colors.red50)

	# 	# TODO Scroll list with colliders
	# 	## https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/textScrollList.html
	# 	layoutScroll = cmds.frameLayout("layoutScroll", label = "Colliders List", labelIndent = 80, parent = self.layoutCollisions, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
	# 	self.scrollListColliders = cmds.textScrollList(parent = layoutScroll, allowMultiSelection = True, height = 120)

	# 	for i in range(20): # test list items
	# 		cmds.textScrollList(self.scrollListColliders, edit = True, append = "item {0}".format(i)) # append, selectItem, deselectAll, removeAll, doubleClickCommand
	def UILayoutNucleus(self, layoutMain):
		self.layoutNucleusProperties = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "NUCLEUS PROPERTIES", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutNucleusProperties, adjustableColumn = True)

		### Time Scale
		self.nucleusTimeScaleSlider = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "Time Scale",
			annotation = OverlappyAnnotations.particleTimeScale,
			value = OverlappySettings.nucleusTimeScale,
			minMax = OverlappySettings.rangeNucleusTimeScale,
			menuReset = True,
		)

		### Gravity
		layoutRow = cmds.rowLayout(parent = layoutColumn, numberOfColumns = 4, columnWidth4 = (14, 35, 40, 200))
		self.nucleusGravityCheckbox = cmds.checkBox(parent = layoutRow, changeCommand = self.UpdateParticleSettings, value = OverlappySettings.nucleusGravityActivated)
		cmds.text(parent = layoutRow, label = "Gravity")
		self.nucleusGravityFloatField = cmds.floatField(parent = layoutRow, changeCommand = self.UpdateParticleSettings, value = OverlappySettings.nucleusGravityValue, precision = 2)
		self.nucleusGravityDirectionFloatFieldGrp = cmds.floatFieldGrp(parent = layoutRow, changeCommand = self.UpdateParticleSettings, numberOfFields = 3, columnWidth4 = [48, 40, 40, 40], label = "Direction", value = (OverlappySettings.nucleusGravityDirection[0], OverlappySettings.nucleusGravityDirection[1], OverlappySettings.nucleusGravityDirection[2], 0))
		self.nucleusGravityDirectionFloatFieldGrp = self.nucleusGravityDirectionFloatFieldGrp.replace(Settings.windowName + "|", "") # HACK fix for docked window only. Don't know how to avoid issue


	### CHAIN UI
	# def UILayoutChainMode(self, layoutMain): # TODO
		# self.layoutChainMode = cmds.frameLayout("layoutChainMode", label = Settings.frames2Prefix + "CHAIN MODE - WORK IN PROGRESS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		
		# cmds.menuBarLayout()
		# cmds.menu(label = "Edit")
		# cmds.menuItem(label = "Reset Settings", command = self._ResetAllChainValues, image = Icons.rotateClockwise)
				
		## self.UILayoutChainButtons(self.layoutChainMode)
		# self.UILayoutChainDynamicProperties(self.layoutChainMode)
		# pass
	# def UILayoutChainButtons(self, layoutMain): # TODO
		## SETUP
		# self.layoutChainButtons = cmds.frameLayout("layoutChainButtons", label = "Buttons", labelIndent = 100, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		# layoutColumn = cmds.columnLayout(parent = self.layoutChainButtons, adjustableColumn = True)

		## count = 2
		## cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		##
		## cmds.button(label = "Create", command = PhysicsHair.CreateNHairOnSelected, backgroundColor = Colors.green10)
		## cmds.button(label = "Remove", command = self._SetupDelete, backgroundColor = Colors.red10, annotation = OverlappyAnnotations.setupDelete)
		# pass
	# def UILayoutChainDynamicProperties(self, layoutMain): # TODO
		# self.layoutChainDynamicProperties = cmds.frameLayout("layoutChainDynamicProperties", label = "Dynamic Properties", labelIndent = 70, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
	

	### PARTICLE UI
	def UILayoutParticle(self, layoutMain):
		self.layoutParticleMode = cmds.frameLayout(parent = layoutMain, label = Settings.frames2Prefix + "PARTICLE SIMULATION", collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		self.UILayoutParticleSetup(self.layoutParticleMode)
		self.UILayoutParticleAimOffset(self.layoutParticleMode)
		self.UILayoutParticleDynamicProperties(self.layoutParticleMode)
	def UILayoutParticleSetup(self, layoutMain):
		self.layoutParticleButtons = cmds.frameLayout(parent = layoutMain, label = "Setup And Bake", labelIndent = 87, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleButtons, adjustableColumn = True)
		
		count = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Point", command = self.ParticleSetupPoint, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setupPoint)
		cmds.button(label = "Aim", command = self.ParticleSetupAim, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setupAim)
		cmds.button(label = "Combo", command = self.ParticleSetupCombo, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setupCombo)
		cmds.button(label = "Remove", command = partial(self.ParticleSetupDelete, False, True), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.setupDelete)

		count = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Bake Point", command = partial(self.BakeParticleVariants, 1), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.bakeTranslation)
		cmds.button(label = "Bake Aim", command = partial(self.BakeParticleVariants, 2), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.bakeRotation)
		cmds.button(label = "Bake Combo", command = partial(self.BakeParticleVariants, 3), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.bakeCombo)
		cmds.button(label = "Bake Current", command = partial(self.BakeParticleVariants, 0), backgroundColor = Colors.orange50, annotation = OverlappyAnnotations.bakeCurrent)
	def UILayoutParticleAimOffset(self, layoutMain):
		self.layoutParticleOffset = cmds.frameLayout(parent = layoutMain, label = "Aim Offset", labelIndent = 100, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleOffset, adjustableColumn = True)
		
		# self.checkboxAutoOffset = UI.Checkbox(label = "Auto") # TODO

		def CustomRadioButtonGroup(label="label", value=0):
			layout = cmds.rowLayout(parent = layoutColumn, numberOfColumns = 6, columnWidth6 = (40, 55, 35, 35, 35, 60), columnAlign = [1, "center"], columnAttach = [(1, "both", 0)])
			text = cmds.text(label = label, annotation = OverlappyAnnotations.aimOffset)
			floatField = cmds.floatField(value = value, changeCommand = self.UpdateParticleAimOffsetSettings, precision = 1, minValue = 0, annotation = OverlappyAnnotations.aimOffsetValue)
			cmds.radioCollection()
			radioButton1 = cmds.radioButton(label = "X", onCommand = self.UpdateParticleAimOffsetSettings, annotation = OverlappyAnnotations.aimOffsetAxis)
			radioButton2 = cmds.radioButton(label = "Y", onCommand = self.UpdateParticleAimOffsetSettings, annotation = OverlappyAnnotations.aimOffsetAxis)
			radioButton3 = cmds.radioButton(label = "Z", onCommand = self.UpdateParticleAimOffsetSettings, annotation = OverlappyAnnotations.aimOffsetAxis)
			checkbox = cmds.checkBox(label = "Reverse", value = False, changeCommand = self.UpdateParticleAimOffsetSettings, annotation = OverlappyAnnotations.aimOffsetReverse)
			return layout, text, floatField, radioButton1, radioButton2, radioButton3, checkbox
		
		radioGroup1 = CustomRadioButtonGroup(label = "Aim", value = OverlappySettings.particleAimOffsetsValues[0])
		self.aimOffsetFloatGroup[0] = radioGroup1[1]
		self.aimOffsetFloatGroup[1] = radioGroup1[2]
		self.aimOffsetRadioCollection[0] = radioGroup1[3]
		self.aimOffsetRadioCollection[1] = radioGroup1[4]
		self.aimOffsetRadioCollection[2] = radioGroup1[5]
		self.aimOffsetCheckbox = radioGroup1[6]
		cmds.radioButton(self.aimOffsetRadioCollection[OverlappySettings.particleAimOffsetsAxes[0]], edit = True, select = True)

		radioGroup2 = CustomRadioButtonGroup(label = "Up", value = OverlappySettings.particleAimOffsetsValues[1])
		self.aimOffsetUpFloatGroup[0] = radioGroup2[1]
		self.aimOffsetUpFloatGroup[1] = radioGroup2[2]
		self.aimOffsetUpRadioCollection[0] = radioGroup2[3]
		self.aimOffsetUpRadioCollection[1] = radioGroup2[4]
		self.aimOffsetUpRadioCollection[2] = radioGroup2[5]
		self.aimOffsetUpCheckbox = radioGroup2[6]
		cmds.radioButton(self.aimOffsetUpRadioCollection[OverlappySettings.particleAimOffsetsAxes[1]], edit = True, select = True)
	def UILayoutParticleDynamicProperties(self, layoutMain):
		self.layoutParticleDynamicProperties = cmds.frameLayout(parent = layoutMain, label = "Dynamic Properties", labelIndent = 80, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleDynamicProperties, adjustableColumn = True)

		self.sliderParticleRadius = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "Radius",
			annotation = OverlappyAnnotations.particleRadius,
			value = OverlappySettings.particleRadius,
			minMax = OverlappySettings.rangePRadius,
			menuReset = True,
		)

		cmds.separator(parent = layoutColumn, style = "in")
		
		self.sliderParticleGoalSmooth = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "G.Smooth",
			annotation = OverlappyAnnotations.particleGoalSmooth,
			value = OverlappySettings.particleGoalSmooth,
			minMax = OverlappySettings.rangeGSmooth,
			menuReset = True,
		)
		
		self.sliderParticleGoalWeight = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "G.Weight",
			annotation = OverlappyAnnotations.particleGoalWeight,
			value = OverlappySettings.particleGoalWeight,
			minMax = OverlappySettings.rangeGWeight,
			menuReset = True,
		)
		
		cmds.separator(parent = layoutColumn, style = "in")

		self.sliderParticleConserve = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "Conserve",
			annotation = OverlappyAnnotations.particleConserve,
			value = OverlappySettings.particleConserve,
			minMax = OverlappySettings.rangePConserve,
			menuReset = True,
		)
		
		self.sliderParticleDrag = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "Drag",
			annotation = OverlappyAnnotations.particleDrag,
			value = OverlappySettings.particleDrag,
			minMax = OverlappySettings.rangePDrag,
			menuReset = True,
		)
		
		self.sliderParticleDamp = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = self.UpdateParticleSettings,
			label = "Damp",
			annotation = OverlappyAnnotations.particleDamp,
			value = OverlappySettings.particleDamp,
			minMax = OverlappySettings.rangePDamp,
			menuReset = True,
		)


	### PARTICLE LOGIC
	def CompileParticleAimOffset(self):
		### Get aim offset values from UI
		valueAimFloat = cmds.floatField(self.aimOffsetFloatGroup[1], query = True, value = True)
		valueAimAxisX = cmds.radioButton(self.aimOffsetRadioCollection[0], query = True, select = True)
		valueAimAxisY = cmds.radioButton(self.aimOffsetRadioCollection[1], query = True, select = True)
		valueAimAxisZ = cmds.radioButton(self.aimOffsetRadioCollection[2], query = True, select = True)
		valueAimCheckbox = cmds.checkBox(self.aimOffsetCheckbox, query = True, value = True)
		
		valueAimUpFloat = cmds.floatField(self.aimOffsetUpFloatGroup[1], query = True, value = True)
		valueAimUpAxisX = cmds.radioButton(self.aimOffsetUpRadioCollection[0], query = True, select = True)
		valueAimUpAxisY = cmds.radioButton(self.aimOffsetUpRadioCollection[1], query = True, select = True)
		valueAimUpAxisZ = cmds.radioButton(self.aimOffsetUpRadioCollection[2], query = True, select = True)
		valueAimUpCheckbox = cmds.checkBox(self.aimOffsetUpCheckbox, query = True, value = True)

		### Compile aim target value
		self.particleAimOffsetTarget = [0, 0, 0]
		valueAimTarget = valueAimFloat * (-1 if valueAimCheckbox else 1)
		if (valueAimAxisX):
			self.particleAimOffsetTarget = [valueAimTarget, 0, 0]
		if (valueAimAxisY):
			self.particleAimOffsetTarget = [0, valueAimTarget, 0]
		if (valueAimAxisZ):
			self.particleAimOffsetTarget = [0, 0, valueAimTarget]
		
		### Compile aim up value
		self.particleAimOffsetUp = [0, 0, 0]
		valueAimUp = valueAimUpFloat * (-1 if valueAimUpCheckbox else 1)
		if (valueAimUpAxisX):
			self.particleAimOffsetUp = [valueAimUp, 0, 0]
		if (valueAimUpAxisY):
			self.particleAimOffsetUp = [0, valueAimUp, 0]
		if (valueAimUpAxisZ):
			self.particleAimOffsetUp = [0, 0, valueAimUp]
	def ParticleSetupInit(self, *args):
		### Get selected objects
		self.selectedObjects = Selector.MultipleObjects(minimalCount = 1)
		if (self.selectedObjects == None):
			return False
		
		### Remove previous setup if exists
		self.ParticleSetupDelete(clearCache = True)
		
		### Get min/max anim range time and reset time slider
		self.time.Scan()
		self.time.SetCurrent(self.time.values[2])
		
		### Get first selected object
		self.selectedObjects = self.selectedObjects[0] # HACK is it ok to limit only by first element?

		### Create group
		cmds.select(clear = True)
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		cmds.group(empty = True, name = OverlappySettings.nameGroup)

		### Create nucleus node
		self.nucleus1 = Physics.CreateNucleus(name = OverlappySettings.prefix + PhysicsParticle._defaultNameNucleus + "_01", parent = OverlappySettings.nameGroup)
		cmds.select(clear = True)

		# TODO Need to define colliderObject before this logic
		### TODO Connect collision nRigid nodes to nucleus
		# self.colliderNodes[0] = cmds.createNode("nRigid", name = "myNRigid")
		# cmds.connectAttr("time1.outTime", self.colliderNodes[0] + ".currentTime")
		# cmds.connectAttr(self.colliderObjects[0] + ".worldMesh[0]", self.colliderNodes[0] + ".inputMesh")
		# cmds.connectAttr(self.colliderNodes[0] + ".currentState", self.nucleus1 + ".inputPassive[0]")
		# cmds.connectAttr(self.colliderNodes[0] + ".startState", self.nucleus1 + ".inputPassiveStart[0]")
		# cmds.connectAttr(self.nucleus1 + ".startFrame", self.colliderNodes[0] + ".startFrame")
		return True
	def ParticleSetupPoint(self, *args):
		isInitDone = self.ParticleSetupInit()
		if (not isInitDone):
			return

		particleSetup = PhysicsParticle.CreateParticleSetup(targetObject = self.selectedObjects, nucleusNode = self.nucleus1, parentGroup = OverlappySettings.nameGroup)
		self.setupCreatedPoint = True
		self.setupCreated = True

		### Cache setup elements names
		self.particleBase = particleSetup[4]
		self.particleLocator = particleSetup[6]

		self.bakingObject = self.particleLocator

		### End
		self.UpdateParticleSettings()
		cmds.select(self.selectedObjects, replace = True)
	def ParticleSetupAim(self, *args):
		isInitDone = self.ParticleSetupInit()
		if (not isInitDone):
			return
		
		self.CompileParticleAimOffset()
		
		### Create aim setup
		particleSetup = PhysicsParticle.CreateParticleSetup(targetObject = self.selectedObjects, nucleusNode = self.nucleus1, parentGroup = OverlappySettings.nameGroup, positionOffset = self.particleAimOffsetTarget)
		particleAimSetup = PhysicsParticle.CreateAimSetup(particleSetup, positionOffset = self.particleAimOffsetUp)
		self.setupCreatedAim = True
		self.setupCreated = True

		### Cache setup elements names
		self.particleTarget = particleSetup[4]
		self.particleUp = particleAimSetup[1][4]
		self.particleLocator = particleSetup[6]
		self.particleLocatorGoalOffset = particleSetup[7]
		self.particleLocatorGoalOffsetStartPosition = cmds.xform(self.particleLocatorGoalOffset, query = True, translation = True, worldSpace = True)
		self.particleLocatorGoalOffsetUp = particleAimSetup[1][7]
		self.particleLocatorGoalOffsetUpStartPosition = cmds.xform(self.particleLocatorGoalOffsetUp, query = True, translation = True, worldSpace = True)
		self.particleLocatorAim = particleAimSetup[0]

		### Set baking object
		self.bakingObject = self.particleLocatorAim

		### End
		self.UpdateParticleSettings()
		cmds.select(self.selectedObjects, replace = True)
	def ParticleSetupCombo(self, *args):
		isInitDone = self.ParticleSetupInit()
		if (not isInitDone):
			return
		
		self.CompileParticleAimOffset()

		### Create particle base setup
		particleSetupBase = PhysicsParticle.CreateParticleSetup(targetObject = self.selectedObjects, nucleusNode = self.nucleus1, parentGroup = OverlappySettings.nameGroup)
		
		### Create second nucleus node
		self.nucleus2 = Physics.CreateNucleus(name = OverlappySettings.prefix + PhysicsParticle._defaultNameNucleus + "_02", parent = OverlappySettings.nameGroup)
		cmds.select(clear = True)
		
		### Create particle aim setup
		particleSetupOffset = PhysicsParticle.CreateParticleSetup(targetObject = particleSetupBase[6], nucleusNode = self.nucleus2, parentGroup = OverlappySettings.nameGroup, positionOffset = self.particleAimOffsetTarget)
		particleAimSetup = PhysicsParticle.CreateAimSetup(particleSetupOffset, positionOffset = self.particleAimOffsetUp)
		self.setupCreatedCombo = True
		self.setupCreated = True

		### Cache setup elements names
		self.particleBase = particleSetupBase[4]
		self.particleTarget = particleSetupOffset[4]
		self.particleUp = particleAimSetup[1][4]
		self.particleLocator = particleSetupOffset[6]
		self.particleLocatorGoalOffset = particleSetupOffset[7]
		self.particleLocatorGoalOffsetStartPosition = cmds.xform(self.particleLocatorGoalOffset, query = True, translation = True, worldSpace = True)
		self.particleLocatorGoalOffsetUp = particleAimSetup[1][7]
		self.particleLocatorGoalOffsetUpStartPosition = cmds.xform(self.particleLocatorGoalOffsetUp, query = True, translation = True, worldSpace = True)
		self.particleLocatorAim = particleAimSetup[0]

		### Set baking object
		self.bakingObject = self.particleLocatorAim

		### End
		self.UpdateParticleSettings()
		cmds.select(self.selectedObjects, replace = True)
	def ParticleSetupDelete(self, deselect=False, clearCache=True, *args):
		### Deselect objects
		if (deselect):
			cmds.select(clear = True)
		
		### Delete group
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		
		### Reset flags
		if (clearCache):
			self.setupCreated = False
			self.setupCreatedPoint = False
			self.setupCreatedAim = False
			self.setupCreatedCombo = False


	### SELECT
	def SelectNucleus(self, *args):		
		if (cmds.objExists(self.nucleus1)):
			cmds.select(self.nucleus1, replace = True)
		if (cmds.objExists(self.nucleus2)):
			cmds.select(self.nucleus2, add = True)
	def SelectParticles(self, *args):
		if (cmds.objExists(self.particleBase)):
			cmds.select(self.particleBase, replace = True)
		if (cmds.objExists(self.particleTarget)):
			cmds.select(self.particleTarget, add = True)
		if (cmds.objExists(self.particleUp)):
			cmds.select(self.particleUp, add = True)
	

	### SETTINGS
	def UpdateParticleAllSettings(self, *args):
		self.UpdateParticleAimOffsetSettings()
		self.UpdateParticleSettings()
	def UpdateParticleAimOffsetSettings(self, *args):
		def SetParticleAimOffset(nameLocator, nameParticle, goalStartPosition, offset=(0, 0, 0)):
			if (cmds.objExists(nameLocator)):
				cmds.setAttr(nameLocator + ".translateX", offset[0])
				cmds.setAttr(nameLocator + ".translateY", offset[1])
				cmds.setAttr(nameLocator + ".translateZ", offset[2])
			
			if (cmds.objExists(nameParticle)):
				goalPosition = cmds.xform(nameLocator, query = True, translation = True, worldSpace = True)
				cmds.setAttr(nameParticle + ".translateX", goalPosition[0] - goalStartPosition[0])
				cmds.setAttr(nameParticle + ".translateY", goalPosition[1] - goalStartPosition[1])
				cmds.setAttr(nameParticle + ".translateZ", goalPosition[2] - goalStartPosition[2])
		
		self.CompileParticleAimOffset()
		
		self.time.SetCurrent(self.time.values[2])
		SetParticleAimOffset(nameLocator = self.particleLocatorGoalOffset, nameParticle = self.particleTarget, goalStartPosition = self.particleLocatorGoalOffsetStartPosition, offset = self.particleAimOffsetTarget)
		SetParticleAimOffset(nameLocator = self.particleLocatorGoalOffsetUp, nameParticle = self.particleUp, goalStartPosition = self.particleLocatorGoalOffsetUpStartPosition, offset = self.particleAimOffsetUp)
	def UpdateParticleSettings(self, *args):
		### Nucleus
		def SetNucleusAttributes(name):
			if (cmds.objExists(name)):
				cmds.setAttr(name + ".timeScale", self.nucleusTimeScaleSlider.Get())
				cmds.setAttr(name + ".gravity", cmds.floatField(self.nucleusGravityFloatField, query = True, value = True))
				direction = cmds.floatFieldGrp(self.nucleusGravityDirectionFloatFieldGrp, query = True, value = True)
				cmds.setAttr(name + ".gravityDirectionX", direction[0])
				cmds.setAttr(name + ".gravityDirectionY", direction[1])
				cmds.setAttr(name + ".gravityDirectionZ", direction[2])
		SetNucleusAttributes(self.nucleus1)
		SetNucleusAttributes(self.nucleus2)

		### Particles
		def SetParticleDynamicAttributes(name):
			if (cmds.objExists(name)):
				useGravity = not cmds.checkBox(self.nucleusGravityCheckbox, query = True, value = True)
				cmds.setAttr(name + "Shape.ignoreSolverGravity", useGravity)
				cmds.setAttr(name + "Shape.radius", self.sliderParticleRadius.Get())
				cmds.setAttr(name + "Shape.goalSmoothness", self.sliderParticleGoalSmooth.Get())
				cmds.setAttr(name + "Shape.goalWeight[0]", self.sliderParticleGoalWeight.Get())
				cmds.setAttr(name + "Shape.conserve", self.sliderParticleConserve.Get())
				cmds.setAttr(name + "Shape.drag", self.sliderParticleDrag.Get())
				cmds.setAttr(name + "Shape.damp", self.sliderParticleDamp.Get())
		SetParticleDynamicAttributes(name = self.particleBase)
		SetParticleDynamicAttributes(name = self.particleTarget)
		SetParticleDynamicAttributes(name = self.particleUp)
	
	def ResetAllSettings(self, *args):
		### Options
		self.menuCheckboxHierarchy.Reset()
		self.menuCheckboxLayer.Reset()
		self.menuCheckboxLoop.Reset()
		self.menuCheckboxDeleteSetup.Reset()
		# self.menuCheckboxCollisions.Reset()

		### Loop cycles
		cmds.menuItem(self.menuRadioButtonsLoop[2], edit = True, radioButton = True) # TODO move to settings

		### Nucleus
		self.nucleusTimeScaleSlider.Reset()
		cmds.checkBox(self.nucleusGravityCheckbox, edit = True, value = OverlappySettings.nucleusGravityActivated)
		cmds.floatField(self.nucleusGravityFloatField, edit = True, value = OverlappySettings.nucleusGravityValue)
		cmds.floatFieldGrp(self.nucleusGravityDirectionFloatFieldGrp, edit = True, value = (OverlappySettings.nucleusGravityDirection[0], OverlappySettings.nucleusGravityDirection[1], OverlappySettings.nucleusGravityDirection[2], 0))

		### Aim offset target
		cmds.floatField(self.aimOffsetFloatGroup[1], edit = True, value = OverlappySettings.particleAimOffsetsValues[0])
		cmds.checkBox(self.aimOffsetCheckbox, edit = True, value = False)
		cmds.radioButton(self.aimOffsetRadioCollection[OverlappySettings.particleAimOffsetsAxes[0]], edit = True, select = True) # TODO move to settings

		### Aim offset up
		cmds.floatField(self.aimOffsetUpFloatGroup[1], edit = True, value = OverlappySettings.particleAimOffsetsValues[1])
		cmds.checkBox(self.aimOffsetUpCheckbox, edit = True, value = False)
		cmds.radioButton(self.aimOffsetUpRadioCollection[OverlappySettings.particleAimOffsetsAxes[1]], edit = True, select = True) # TODO move to settings

		### Particle dynamic properties
		self.sliderParticleRadius.Reset()
		self.sliderParticleGoalSmooth.Reset()
		self.sliderParticleGoalWeight.Reset()
		self.sliderParticleConserve.Reset()
		self.sliderParticleDrag.Reset()
		self.sliderParticleDamp.Reset()

		### Update all settings
		self.UpdateParticleAllSettings()
	

	### GET VALUES
	def GetLoopCyclesIndex(self):
		for i, item in enumerate(self.menuRadioButtonsLoop):
			if cmds.menuItem(item, query = True, radioButton = True):
				return i
		return -1


	### BAKE ANIMATION
	def BakeParticleLogic(self):
		### Check created setups
		if (not self.setupCreated):
			cmds.warning("Particle setup is not created")
			return False

		### Get raw attributes
		attributesType = ()
		if (self.setupCreatedPoint):
			attributesType = Enums.Attributes.translateLong
		elif (self.setupCreatedAim):
			attributesType = attributesType + Enums.Attributes.rotateLong
		elif (self.setupCreatedCombo):
			attributesType = Enums.Attributes.translateLong + Enums.Attributes.rotateLong
		if (len(attributesType) == 0):
			cmds.warning("No baking attributes specified")
			return False

		### Construct attributes with object name
		attributes = []
		for i in range(len(attributesType)):
			attributes.append("{0}.{1}".format(self.selectedObjects, attributesType[i]))
		
		### Filter attributes
		attributesFiltered = Attributes.FilterAttributesAnimatable(attributes = attributes, skipMutedKeys = True)
		if (attributesFiltered == None):
			self.ParticleSetupDelete(clearCache = True)
			return False
		
		### Cut object name from attributes
		for i in range(len(attributesFiltered)):
			attributesFiltered[i] = attributesFiltered[i].replace(self.selectedObjects + ".", "")

		### Set keys for target object attributes
		cmds.setKeyframe(self.selectedObjects, attribute = attributesFiltered)
		
		### Set time range
		self.time.Scan()
		startTime = self.time.values[2]
		self.time.SetCurrent(startTime)
		if (self.menuCheckboxLoop.Get()):
			startTime = self.time.values[2] - self.time.values[3] * self.GetLoopCyclesIndex()
			self.time.SetMin(startTime)
			self.time.SetCurrent(startTime)
		cmds.setAttr(self.nucleus1 + ".startFrame", startTime)
		if (cmds.objExists(self.nucleus2)):
			cmds.setAttr(self.nucleus2 + ".startFrame", startTime)

		### Start logic
		name = "_rebake_" + Text.ConvertSymbols(self.selectedObjects)
		objectDuplicate = cmds.duplicate(self.selectedObjects, name = name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)[0]
		cmds.select(clear = True)
		for attributeTranslate in Enums.Attributes.translateLong:
			cmds.setAttr(objectDuplicate + "." + attributeTranslate, lock = False)
		for attributeRotate in Enums.Attributes.rotateLong:
			cmds.setAttr(objectDuplicate + "." + attributeRotate, lock = False)
		Constraints.ConstrainSecondToFirstObject(self.bakingObject, objectDuplicate, maintainOffset = True, parent = True)
		cmds.select(objectDuplicate, replace = True)

		### Bake animation
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		Constraints.DeleteConstraints(objectDuplicate)

		### Copy keys, create layers and paste keys
		cmds.copyKey(objectDuplicate, time = (self.time.values[2], self.time.values[3]), attribute = attributesFiltered)
		useLayers = self.menuCheckboxLayer.Get()
		if (useLayers):
			name = OverlappySettings.nameLayers[2] + self.selectedObjects
			animLayer = self.LayerCreate(name)
			attrsLayer = []
			for attributeFiltered in attributesFiltered:
				attrsLayer.append("{0}.{1}".format(self.selectedObjects, attributeFiltered))
			cmds.animLayer(animLayer, edit = True, attribute = attrsLayer)
			cmds.pasteKey(self.selectedObjects, option = "replace", attribute = attributesFiltered, animLayer = animLayer)
		else:
			cmds.pasteKey(self.selectedObjects, option = "replaceCompletely", attribute = attributesFiltered)
		cmds.delete(objectDuplicate)

		### Set time range
		if (self.menuCheckboxLoop.Get()):
			startTime = self.time.values[2]
			cmds.setAttr(self.nucleus1 + ".startFrame", startTime)
			if (cmds.objExists(self.nucleus2)):
				cmds.setAttr(self.nucleus2 + ".startFrame", startTime)
			self.time.Reset()
			Animation.SetInfinityCycle(self.selectedObjects)
		else:
			Animation.SetInfinityConstant(self.selectedObjects)
		
		### Delete setup
		if (self.menuCheckboxDeleteSetup.Get()):
			self.ParticleSetupDelete(clearCache = True)
		return True
	def BakeParticleVariants(self, variant, *args):
		selected = Selector.MultipleObjects(minimalCount = 1)
		if (selected == None):
			if (not self.setupCreated):
				cmds.warning("Can't bake animation. Nothing selected and particle setup is not created")
				return
		
		### Check zero particle offset
		self.CompileParticleAimOffset()
		sumOffsetTarget = self.particleAimOffsetTarget[0] + self.particleAimOffsetTarget[1] + self.particleAimOffsetTarget[2]
		sumOffsetUp = self.particleAimOffsetUp[0] + self.particleAimOffsetUp[1] + self.particleAimOffsetUp[2]
		isBakingAimOrCombo = variant in [2, 3]
		isBakingCurrent = variant == 0 and (self.setupCreatedAim or self.setupCreatedCombo)
		if (isBakingAimOrCombo or isBakingCurrent):
				if (sumOffsetTarget == 0 or sumOffsetUp == 0):
					dialogResult = cmds.confirmDialog(
						title = "Zero particle aim offset detected",
						message = "For baking using aim, set the aim offset to non-zero values.\nIf aim or up offsets are zero, the particle probably will stay in the same position as the original object, and no rotation will occur.\n",
						messageAlign = "left",
						icon = "warning",
						button = ["Continue anyway", "Cancel"],
						annotation = ["Proceed with zero offset, no useful animation will be baked", "Cancel baking operation"],
						defaultButton = "Cancel",
						cancelButton = "Cancel",
						dismissString = "TODO: dismissString"
						)
					if (dialogResult == "Cancel"):
						cmds.warning("Overlappy Rotation Baking cancelled")
						return

		MayaSettings.CachedPlaybackDeactivate()

		### Run baking process
		if (variant == 0 or selected == None):
			wasBakedSuccessfully = self.BakeParticleLogic()
			if (wasBakedSuccessfully):
				cmds.select(self.selectedObjects, replace = True)
		else:
			### Check hierarchy and get objects
			if (self.menuCheckboxHierarchy.Get()):
				selected = Selector.SelectHierarchyTransforms()
			### Bake
			for i in range(len(selected)):
				cmds.select(selected[i], replace = True)
				if (variant == 1):
					self.ParticleSetupPoint()
				elif (variant == 2):
					self.ParticleSetupAim()
				elif (variant == 3):
					self.ParticleSetupCombo()
				self.BakeParticleLogic()
			### Select original objects
			cmds.select(selected, replace = True)


	### LAYERS
	def LayerCreate(self, name):
		### Create main layer
		if (not cmds.objExists(OverlappySettings.nameLayers[0])):
			self.layers[0] = Layers.Create(layerName = OverlappySettings.nameLayers[0])
		
		### Create layers on selected
		layerName = Text.ConvertSymbols(name) + "_1"
		return Layers.Create(layerName = layerName, parent = self.layers[0])
	def LayerMoveToSafeOrTemp(self, safeLayer=True, *args): # TODO rework
		id = [0, 1]
		
		if (not safeLayer):
			id = [1, 0]
		
		nameLayer1 = OverlappySettings.nameLayers[id[0]]
		nameLayer2 = OverlappySettings.nameLayers[id[1]]

		### Check source layer
		if (not cmds.objExists(nameLayer1)):
			cmds.warning("Layer \"{0}\" doesn't exist".format(nameLayer1))
			return
		
		### Get selected layers
		selectedLayers = []
		for animLayer in cmds.ls(type = "animLayer"):
			if cmds.animLayer(animLayer, query = True, selected = True):
				selectedLayers.append(animLayer)
				
		### Check selected count
		childrenLayers = cmds.animLayer(self.layers[id[0]], query = True, children = True)
		filteredLayers = []
		if (len(selectedLayers) == 0):
			if (childrenLayers == None):
				cmds.warning("Layer \"{0}\" is empty".format(nameLayer1))
				return
			else:
				for layer in childrenLayers:
					filteredLayers.append(layer)
		else:
			if (childrenLayers == None):
				cmds.warning("Layer \"{0}\" is empty".format(nameLayer1))
				return
			else:
				for childLayer in childrenLayers:
					for selectedLayer in selectedLayers:
						if (childLayer == selectedLayer):
							filteredLayers.append(childLayer)
			if (len(filteredLayers) == 0):
				cmds.warning("Nothing to move")
				return
		
		### Create safe layer
		if (not cmds.objExists(nameLayer2)):
			self.layers[id[1]] = cmds.animLayer(nameLayer2, override = True)
		
		### Move children or selected layers
		for layer in filteredLayers:
			cmds.animLayer(layer, edit = True, parent = self.layers[id[1]])
		
		### Delete TEMP layer if no children
		if (len(filteredLayers) == len(childrenLayers)):
			Layers.Delete(nameLayer1)

