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
# from math import pow, sqrt
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


# TODO make cycle infinity before loop bake
# TODO fix nucleus double nodes


class OverlappyAnnotations: # TODO simplify
	### Setup
	setup = "Create particle rig for first selected object. Use this step for setup settings. \nSetup runs every time for each selected object."
	setupDelete = "Delete particle rig if exists"

	### Baking
	translation = "Bake simulation for translation attributes"
	translationWithOffset = "Bake simulation for translation attributes with offset"
	rotation = "Bake simulation for rotation attributes"
	comboTranslateRotate = "Bake simulation translation and rotation"
	scale = "Bake simulation for scale attributes"

	### Layers
	layerDeleteAll = "All animation layers will be deleted"
	layerDeleteTemp = "Only Temp layer and child layers will be deleted"
	layerDeleteSafe = "Only Safe layer and child layers will be deleted"
	layerMoveTemp = "Move Temp layer sublayers to Safe layer"
	layerMoveSafe = "Move Safe layer sublayers to Temp layer"

	### Options
	# checkboxHierarchy = "Bake simulation for all child hierarhy of selected objects"
	# checkboxLayer = "Bake animation into override layers. \nIf turned off animation will be baked directly to selected objects"
	# checkboxLoop = "Use for cycles. \nImportant to have cycle constant animation curves"
	# checkboxClean = "Remove particle setup after baking end"

	### Collisions
	checkboxCollisions = "Use collisions"

	### Nucleus
	particleTimeScale = "Nucleus Time Scale"

	### Particle
	particleRadius = "Particle Radius"
	particleGoalSmooth = "This value is used to control the “smoothness” of the change in the goal forces as the weight changes from 0.0 to 1.0.\nThis is purely an aesthetic effect, with no scientific basis.\nThe higher the number, the smoother the change."
	particleGoalWeight = "Particle Goal Weight"
	particleConserve = "The Conserve value controls how much of a particle object’s velocity is retained from frame to frame.\nSpecifically, Conserve scales a particle’s velocity attribute at the beginning of each frame’s execution.\nAfter scaling the velocity, Maya applies any applicable dynamics to the particles to create the final positioning at the end of the frame."
	particleDrag = "Specifies the amount of drag applied to the current nParticle object.\nDrag is the component of aerodynamic force parallel to the relative wind which causes resistance.\nDrag is 0.05 by default."
	particleDamp = "Specifies the amount the motion of the current nParticles are damped.\nDamping progressively diminishes the movement and oscillation of nParticles by dissipating energy."

	### Aim Offset
	# offsetMirrorX = "Mirror particle offset value to opposite" # XXX
	# offsetMirrorY = offsetMirrorX # XXX
	# offsetMirrorZ = offsetMirrorX # XXX
	# offsetX = "Move particle from original object. Important to use offset for Rotation baking" # XXX
	# offsetY = offsetX # XXX
	# offsetZ = offsetX # XXX

class OverlappySettings: # TODO simplify and move to preset
	# NAMING
	prefix = "ovlp"
	prefixLayer = "_" + prefix
	nameLayers = (prefixLayer + "TEMP_", prefixLayer + "SAFE_", "pos_", "rot_", "combo_")
	nameGroup = prefix + "Group"
		
	# SETTINGS CHECKBOXES
	optionCheckboxHierarchy = False
	optionCheckboxLayer = True
	optionCheckboxLoop = False
	optionCheckboxDeleteSetup = True
	optionCheckboxCollisions = True

	# SETTINGS DYNAMIC PROPERTIES
	nucleusTimeScale = 1
	particleRadius = 1
	particleGoalSmooth = 1
	particleGoalWeight = 0.3
	particleConserve = 1
	particleDrag = 0.01
	particleDamp = 0
		
	# SLIDERS (field min/max, slider min/max)
	rangeNucleusTimeScale = (0.001, float("inf"), 0.001, 1)
	rangePRadius = (0, float("inf"), 0, 10)
	rangeGSmooth = (0, float("inf"), 0, 10)
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

		self.setupCreatedPoint = False
		self.setupCreatedAim = False
		self.setupCreatedCombo = False

		### VALUES
		self.time = Timeline.TimeRangeHandler()
		
		### OBJECTS
		self.selectedObjects = ""
		self.layers = ["", ""]
		self.nucleus1 = ""
		self.nucleus2 = ""
		## self.colliderObjects = [] # XXX
		## self.colliderNodes = [] # XXX

		### PARTICLE MODE
		self.particleAimOffsetTarget = [0, 0, 0]
		self.particleAimOffsetUp = [0, 0, 0]
		self.particleBase = ""
		self.particleTarget = ""
		self.particleUp = ""
		self.particleLocator = ""
		self.particleLocatorAim = ""
		# self.particleGoalStartPosition = [None, (0, 0, 0)] # TODO simplify
		
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

		### UI AIM OFFSET
		## self.checkboxAutoOffset = None # TODO
		self.aimOffsetFloatGroup = [None, None] # text, float
		self.aimOffsetRadioCollection = [None, [None, None, None]] # collection, (element 1, 2, 3)
		self.aimOffsetCheckbox = None
		self.aimOffsetUpFloatGroup = [None, None] # text, float
		self.aimOffsetUpRadioCollection = [None, [None, None, None]] # collection, (element 1, 2, 3)
		self.aimOffsetUpCheckbox = None

		### UI SLIDERS NUCLEUS PROPERTIES
		self.sliderNucleusTimeScale = None
		
		### UI SLIDERS PARTICLE DYNAMIC PROPERTIES
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
		cmds.columnLayout("layoutMenuBar", parent = layoutMain, adjustableColumn = True, width = Settings.windowWidthMargin)
		cmds.menuBarLayout()

		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Reset Settings", command = self.ResetSettings, image = Icons.rotateClockwise)
		
		cmds.menu(label = "Options", tearOff = True)
		self.menuCheckboxHierarchy = UI.MenuCheckbox(label = "Use Hierarchy", value = OverlappySettings.optionCheckboxHierarchy, valueDefault = OverlappySettings.optionCheckboxHierarchy)
		self.menuCheckboxLayer = UI.MenuCheckbox(label = "Bake To Layer", value = OverlappySettings.optionCheckboxLayer, valueDefault = OverlappySettings.optionCheckboxLayer)
		self.menuCheckboxLoop = UI.MenuCheckbox(label = "Loop", value = OverlappySettings.optionCheckboxLoop, valueDefault = OverlappySettings.optionCheckboxLoop)
		self.menuCheckboxDeleteSetup = UI.MenuCheckbox(label = "Delete Setup After Bake", value = OverlappySettings.optionCheckboxDeleteSetup, valueDefault = OverlappySettings.optionCheckboxDeleteSetup)
		# self.menuCheckboxCollisions = UI.MenuCheckbox(label = "Collisions", value = OverlappySettings.optionCheckboxCollisions, valueDefault = OverlappySettings.optionCheckboxCollisions)

		cmds.menuItem(dividerLabel = "Pre Loop Cycles", divider = True)
		
		self.menuRadioButtonsLoop[0] = cmds.menuItem(label = "0", radioButton = True) # , command = lambda *args: print("Option 0 selected")
		self.menuRadioButtonsLoop[1] = cmds.menuItem(label = "1", radioButton = True)
		self.menuRadioButtonsLoop[2] = cmds.menuItem(label = "2", radioButton = True)
		self.menuRadioButtonsLoop[3] = cmds.menuItem(label = "3", radioButton = True)
		self.menuRadioButtonsLoop[4] = cmds.menuItem(label = "4", radioButton = True)
		cmds.menuItem(self.menuRadioButtonsLoop[2], edit = True, radioButton = True)
	def UILayoutLayers(self, layoutMain):
		self.layoutLayers = cmds.frameLayout("layoutLayers", label = Settings.frames2Prefix + "LAYERS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutLayers, adjustableColumn = True)
		
		count = 1
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Delete All Layers", command = partial(Layers.Delete, "BaseAnimation"), backgroundColor = Colors.red50, annotation = OverlappyAnnotations.layerDeleteAll)

		count = 2
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Delete Temp layer", command = partial(Layers.Delete, OverlappySettings.nameLayers[0]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteTemp)
		cmds.button(label = "Move To Safe Layer", command = partial(self.LayerMoveToSafeOrTemp, True), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveTemp)
		
		cmds.button(label = "Delete Safe layer", command = partial(Layers.Delete, OverlappySettings.nameLayers[1]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteSafe)
		cmds.button(label = "Move To Temp Layer", command = partial(self.LayerMoveToSafeOrTemp, False), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveSafe)
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
		self.layoutNucleusProperties = cmds.frameLayout("layoutNucleusProperties", label = Settings.frames2Prefix + "NUCLEUS PROPERTIES", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutNucleusProperties, adjustableColumn = True)

		commandDefault = self.UpdateSettings

		self.sliderNucleusTimeScale = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
			label = "Time Scale",
			annotation = OverlappyAnnotations.particleTimeScale,
			value = OverlappySettings.nucleusTimeScale,
			minMax = OverlappySettings.rangeNucleusTimeScale,
			menuReset = True,
		)

		# self.sliderNucleusTimeScale = UI.Slider( # TODO
		# 	parent = layoutColumn,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "**Gravity",
		# 	annotation = OverlappyAnnotations.particleTimeScale,
		# 	value = OverlappySettings.nucleusTimeScale,
		# 	minMax = OverlappySettings.rangeNucleusTimeScale,
		# 	menuReset = True,
		# )

	
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
		## cmds.button(label = "CREATE", command = PhysicsHair.CreateNHairOnSelected, backgroundColor = Colors.green10) # TODO annotation
		## cmds.button(label = "REMOVE", command = self._SetupDelete, backgroundColor = Colors.red10, annotation = OverlappyAnnotations.setupDelete)
		# pass
	# def UILayoutChainDynamicProperties(self, layoutMain): # TODO
		# self.layoutChainDynamicProperties = cmds.frameLayout("layoutChainDynamicProperties", label = "Dynamic Properties", labelIndent = 70, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		# layoutColumn = cmds.columnLayout(parent = self.layoutSimulation, adjustableColumn = True)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Right-Click") # TODO add reset all function

		# commandDefault = self._UpdateParticleAttributes

		# layoutSliders1 = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)
		# self.sliderPRadius = UI.Slider(
		# 	parent = layoutSliders1,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "Radius",
		# 	annotation = OverlappyAnnotations.particleRadius,
		# 	value = OverlappySettings.particleRadius,
		# 	minMax = OverlappySettings.rangePRadius,
		# 	menuReset = True,
		# )

		# cmds.separator(parent = layoutColumn, style = "in")
		
		# layoutSliders2 = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)
		# self.sliderPConserve = UI.Slider(
		# 	parent = layoutSliders2,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "Conserve",
		# 	annotation = OverlappyAnnotations.particleConserve,
		# 	value = OverlappySettings.particleConserve,
		# 	minMax = OverlappySettings.rangePConserve,
		# 	menuReset = True,
		# )
		
		# self.sliderPDrag = UI.Slider(
		# 	parent = layoutSliders2,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "Drag",
		# 	annotation = OverlappyAnnotations.particleDrag,
		# 	value = OverlappySettings.particleDrag,
		# 	minMax = OverlappySettings.rangePDrag,
		# 	menuReset = True,
		# )
		
		# self.sliderPDamp = UI.Slider(
		# 	parent = layoutSliders2,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "Damp",
		# 	annotation = OverlappyAnnotations.particleDamp,
		# 	value = OverlappySettings.particleDamp,
		# 	minMax = OverlappySettings.rangePDamp,
		# 	menuReset = True,
		# )
		
		# self.sliderGSmooth = UI.Slider(
		# 	parent = layoutSliders2,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "G.Smooth",
		# 	annotation = OverlappyAnnotations.particleGoalSmooth,
		# 	value = OverlappySettings.particleGoalSmooth,
		# 	minMax = OverlappySettings.rangeGSmooth,
		# 	menuReset = True,
		# )
		
		# self.sliderGWeight = UI.Slider(
		# 	parent = layoutSliders2,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "G.Weight",
		# 	annotation = OverlappyAnnotations.particleGoalWeight,
		# 	value = OverlappySettings.particleGoalWeight,
		# 	minMax = OverlappySettings.rangeGWeight,
		# 	menuReset = True,
		# )
		
		# self.sliderNTimeScale = UI.Slider(
		# 	parent = layoutSliders2,
		# 	widthWindow = Settings.windowWidthMargin,
		# 	widthMarker = Settings.sliderWidthMarker,
		# 	columnWidth3 = Settings.sliderWidth,
		# 	command = commandDefault,
		# 	label = "Time Scale",
		# 	annotation = OverlappyAnnotations.particleTimeScale,
		# 	value = OverlappySettings.nucleusTimeScale,
		# 	minMax = OverlappySettings.rangeNTimeScale,
		# 	menuReset = True,
		# )

		# pass
	
	
	### PARTICLE UI
	def UILayoutParticle(self, layoutMain):
		self.layoutParticleMode = cmds.frameLayout("layoutParticleMode", label = Settings.frames2Prefix + "PARTICLE MODE", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		
		# cmds.menuBarLayout() # TODO simplify
		# cmds.menu(label = "Edit")
		# cmds.menuItem(label = "Reset Settings", command = self._ResetAllParticleValues, image = Icons.rotateClockwise)

		# cmds.menu(label = "Select", tearOff = True) # TODO simplify
		# cmds.menuItem(label = "Object", command = self.SelectSelectedObjects, image = Icons.cursor)
		# cmds.menuItem(label = "Particle", command = self.SelectParticleObject, image = Icons.particle)
		# cmds.menuItem(label = "Nucleus", command = self.SelectNucleus, image = Icons.nucleus)
		# cmds.menuItem(label = "Target locator", command = self.SelectParticleTarget, image = Icons.locator)
		# cmds.menuItem(label = "Aim locator", command = self.SelectParticleAim, image = Icons.locator)
		
		self.UILayoutParticleSetup(self.layoutParticleMode)
		self.UILayoutParticleAimOffset(self.layoutParticleMode)
		self.UILayoutParticleDynamicProperties(self.layoutParticleMode)
	def UILayoutParticleSetup(self, layoutMain):
		self.layoutParticleButtons = cmds.frameLayout("layoutParticleButtons", label = "Setup and Bake", labelIndent = 77, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleButtons, adjustableColumn = True)
		
		count = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Point", command = self.ParticleSetupPoint, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setup)
		cmds.button(label = "Aim", command = self.ParticleSetupAim, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setup)
		cmds.button(label = "Combo", command = self.ParticleSetupCombo, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setup)
		cmds.button(label = "Remove", command = self.ParticleSetupDelete, backgroundColor = Colors.red10, annotation = OverlappyAnnotations.setupDelete)

		count = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		cmds.button(label = "Bake Point", command = partial(self.BakeParticleVariants, 1), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.translation)
		cmds.button(label = "Bake Aim", command = partial(self.BakeParticleVariants, 2), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.rotation)
		cmds.button(label = "Bake Combo", command = partial(self.BakeParticleVariants, 3), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.comboTranslateRotate)
	def UILayoutParticleAimOffset(self, layoutMain): # TODO
		self.layoutParticleOffset = cmds.frameLayout("layoutParticleOffset", label = "Aim Offset", labelIndent = 88, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleOffset, adjustableColumn = True)
		# self.checkboxAutoOffset = UI.Checkbox(label = "Auto") # TODO

		count = 6
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		
		self.aimOffsetFloatGroup[0] = cmds.text(label = "Aim")
		self.aimOffsetFloatGroup[1] = cmds.floatField(value = 10, precision = 1, minValue = 0)
		self.aimOffsetRadioCollection[0] = cmds.radioCollection()
		self.aimOffsetRadioCollection[1][0] = cmds.radioButton(label = "X")
		self.aimOffsetRadioCollection[1][1] = cmds.radioButton(label = "Y")
		self.aimOffsetRadioCollection[1][2] = cmds.radioButton(label = "Z")
		self.aimOffsetCheckbox = UI.Checkbox(label = "-", annotation = "Reverse Axis")
		cmds.radioCollection(self.aimOffsetRadioCollection[0], edit = True, select = self.aimOffsetRadioCollection[1][0])

		self.aimOffsetUpFloatGroup[0] = cmds.text(label = "Up")
		self.aimOffsetUpFloatGroup[1] = cmds.floatField(value = 10, precision = 1, minValue = 0)
		self.aimOffsetUpRadioCollection[0] = cmds.radioCollection()
		self.aimOffsetUpRadioCollection[1][0] = cmds.radioButton(label = "X")
		self.aimOffsetUpRadioCollection[1][1] = cmds.radioButton(label = "Y")
		self.aimOffsetUpRadioCollection[1][2] = cmds.radioButton(label = "Z")
		self.aimOffsetUpCheckbox = UI.Checkbox(label = "-", annotation = "Reverse Axis")
		cmds.radioCollection(self.aimOffsetUpRadioCollection[0], edit = True, select = self.aimOffsetUpRadioCollection[1][1])
	def UILayoutParticleDynamicProperties(self, layoutMain):
		self.layoutParticleDynamicProperties = cmds.frameLayout("layoutParticleDynamicProperties", label = "Dynamic Properties", labelIndent = 72, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleDynamicProperties, adjustableColumn = True)
		## cmds.popupMenu()
		## cmds.menuItem(label = "Right-Click") # TODO add reset all function

		commandDefault = self.UpdateSettings

		self.sliderParticleRadius = UI.Slider(
			parent = layoutColumn,
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

		cmds.separator(parent = layoutColumn, style = "in")
		
		self.sliderParticleGoalSmooth = UI.Slider(
			parent = layoutColumn,
			widthWindow = Settings.windowWidthMargin,
			widthMarker = Settings.sliderWidthMarker,
			columnWidth3 = Settings.sliderWidth,
			command = commandDefault,
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
			command = commandDefault,
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
			command = commandDefault,
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
			command = commandDefault,
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
			command = commandDefault,
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
		valueAimAxisX = cmds.radioButton(self.aimOffsetRadioCollection[1][0], query = True, select = True)
		valueAimAxisY = cmds.radioButton(self.aimOffsetRadioCollection[1][1], query = True, select = True)
		valueAimAxisZ = cmds.radioButton(self.aimOffsetRadioCollection[1][2], query = True, select = True)
		valueAimCheckbox = self.aimOffsetCheckbox.Get()
		
		valueAimUpFloat = cmds.floatField(self.aimOffsetUpFloatGroup[1], query = True, value = True)
		valueAimUpAxisX = cmds.radioButton(self.aimOffsetUpRadioCollection[1][0], query = True, select = True)
		valueAimUpAxisY = cmds.radioButton(self.aimOffsetUpRadioCollection[1][1], query = True, select = True)
		valueAimUpAxisZ = cmds.radioButton(self.aimOffsetUpRadioCollection[1][2], query = True, select = True)
		valueAimUpCheckbox = self.aimOffsetUpCheckbox.Get()

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
		self.ParticleSetupDelete()
		
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

		### Cache setup elements names
		self.particleTarget = particleSetup[4]
		self.particleLocator = particleSetup[6]

		### End
		self.UpdateSettings()
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

		### Cache setup elements names
		self.particleTarget = particleSetup[4]
		self.particleUp = particleAimSetup[1][4]
		self.particleLocator = particleSetup[6]
		self.particleLocatorAim = particleAimSetup[0]

		### End
		self.UpdateSettings()
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

		### Cache setup elements names
		self.particleBase = particleSetupBase[4]
		self.particleTarget = particleSetupOffset[4]
		self.particleUp = particleAimSetup[1][4]
		self.particleLocator = particleSetupOffset[6]
		self.particleLocatorAim = particleAimSetup[0]

		### End
		self.UpdateSettings()
		cmds.select(self.selectedObjects, replace = True)
	# def ParticleAimOffsetUpdate(self, cacheReset=False, *args): # TODO rework with new aim offset logic
	# 	if (type(cacheReset) is float):
	# 		cacheReset = False
		
		# if (cacheReset):
		# 	self.slidersParticleOffset[0].ResetCached()
		# 	self.slidersParticleOffset[1].ResetCached()
		# 	self.slidersParticleOffset[2].ResetCached()
		
		### Check and set cached value
		# checkX = self.slidersParticleOffset[0].GetCached() != self.slidersParticleOffset[0].Get()
		# checkY = self.slidersParticleOffset[1].GetCached() != self.slidersParticleOffset[1].Get()
		# checkZ = self.slidersParticleOffset[2].GetCached() != self.slidersParticleOffset[2].Get()
		
		# if (checkX or checkY or checkZ):
		# 	self.slidersParticleOffset[0].SetCached()
		# 	self.slidersParticleOffset[1].SetCached()
		# 	self.slidersParticleOffset[2].SetCached()
		# else:
		# 	return

		# self._UpdateSettings()

		# checkSelected = self.selectedObjects == "" or not cmds.objExists(self.selectedObjects)
		# checkGoal = not cmds.objExists(self.particleLocator[0])
		# checkAim = not cmds.objExists(self.particleLocatorAim[2])
		# checkStartPos = self.particleGoalStartPosition[0] == None
		
		# if (checkSelected or checkGoal or checkAim or checkStartPos):
		# 	return

		# cmds.currentTime(self.time.values[2])

		### TODO Mirrors
		# mirror = [1, 1, 1]
		# if (self.checkboxesParticleMirror[0].Get()):
		# 	mirror[0] = -1
		# if (self.checkboxesParticleMirror[1].Get()):
		# 	mirror[1] = -1
		# if (self.checkboxesParticleMirror[2].Get()):
		# 	mirror[2] = -1
		
		### TODO Get values from sliders # simplify
		# values = (
		# 	self.slidersParticleOffset[0].Get() * mirror[0],
		# 	self.slidersParticleOffset[1].Get() * mirror[1],
		# 	self.slidersParticleOffset[2].Get() * mirror[2],
		# 	)
		
		### TODO Set locGoal constraint offset # simplify
		# goalAttributes = (
		# 	self.particleLocator[0] + "_parentConstraint1.target[0].targetOffsetTranslateX",
		# 	self.particleLocator[0] + "_parentConstraint1.target[0].targetOffsetTranslateY",
		# 	self.particleLocator[0] + "_parentConstraint1.target[0].targetOffsetTranslateZ",
		# 	)
		# cmds.setAttr(goalAttributes[0], values[0])
		# cmds.setAttr(goalAttributes[1], values[1])
		# cmds.setAttr(goalAttributes[2], values[2])
		
		### TODO Get offset
		# goalPosition = cmds.xform(self.particleLocator[0], query = True, translation = True)
		# goalOffset = (
		# 	self.particleGoalStartPosition[0][0] - goalPosition[0],
		# 	self.particleGoalStartPosition[0][1] - goalPosition[1],
		# 	self.particleGoalStartPosition[0][2] - goalPosition[2],
		# 	)
		
		### TODO Set particle attributes
		# particleAttributes = (
		# 	self.particleTarget + Text.ConvertSymbols(self.selectedObjects) + ".translateX",
		# 	self.particleTarget + Text.ConvertSymbols(self.selectedObjects) + ".translateY",
		# 	self.particleTarget + Text.ConvertSymbols(self.selectedObjects) + ".translateZ",
		# 	)

		# cmds.setAttr(particleAttributes[0], self.particleGoalStartPosition[1][0] - goalOffset[0])
		# cmds.setAttr(particleAttributes[1], self.particleGoalStartPosition[1][1] - goalOffset[1])
		# cmds.setAttr(particleAttributes[2], self.particleGoalStartPosition[1][2] - goalOffset[2])
		
		### Reposition aim up locator and reconstrain aim
		# selected = cmds.ls(selection = True)
		# cmds.delete(self.particleLocatorAim[1] + "_aimConstraint1")
		# cmds.aimConstraint(self.particleLocator[1], self.particleLocatorAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		# cmds.delete(self.particleLocatorAim[1] + "_aimConstraint1")
		# cmds.parent(self.particleLocatorAim[3], self.particleLocatorAim[1])
		# cmds.setAttr(self.particleLocatorAim[3] + ".tx", 0)
		# cmds.setAttr(self.particleLocatorAim[3] + ".ty", 100)
		# cmds.setAttr(self.particleLocatorAim[3] + ".tz", 0)
		# cmds.parent(self.particleLocatorAim[3], self.particleLocatorAim[0])
		# cmds.aimConstraint(self.particleLocator[1], self.particleLocatorAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.particleLocatorAim[3])
		# cmds.select(selected, replace = True)
		
		### Reconstrain aim locator to hidden aim
		# cmds.setAttr(self.particleLocatorAim[2] + ".rotateX", 0)
		# cmds.setAttr(self.particleLocatorAim[2] + ".rotateY", 0)
		# cmds.setAttr(self.particleLocatorAim[2] + ".rotateZ", 0)
		# cmds.orientConstraint(self.particleLocatorAim[1], self.particleLocatorAim[2], maintainOffset = True)
	def ParticleSetupDelete(self, deselect=False, *args):
		### Deselect objects
		if (deselect):
			cmds.select(clear = True)
		
		### Delete group
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		
		### Reset flags
		self.setupCreatedPoint = False
		self.setupCreatedAim = False


	### SELECT
	# def Select(self, name="", *args):
		# if (name != ""):
		# 	if (cmds.objExists(name)):
		# 		cmds.select(name, replace = True)
		# 	else:
		# 		cmds.warning("\"{0}\" object doesn't exists".format(name))
		# else:
		# 	cmds.warning("Object name is not specified")
	# def SelectSelectedObjects(self, *args): self.Select(self.selectedObjects)
	# def SelectNucleus(self, *args): self.Select(self.nucleus1)
	

	### SETTINGS
	def UpdateSettings(self, *args): # TODO adapt for new features
		### TODO Set aim offset
		# self._SetSliderValue(self.slidersParticleOffset[0].Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateX")

		### Nucleus
		if (cmds.objExists(self.nucleus1)):
			cmds.setAttr(self.nucleus1 + ".timeScale", self.sliderNucleusTimeScale.Get())
		
		if (cmds.objExists(self.nucleus2)):
			cmds.setAttr(self.nucleus2 + ".timeScale", self.sliderNucleusTimeScale.Get())

		### Particles
		def SetParticleAttributes(name):
			if (cmds.objExists(name)):
				cmds.setAttr(name + "Shape.radius", self.sliderParticleRadius.Get())
				cmds.setAttr(name + "Shape.goalSmoothness", self.sliderParticleGoalSmooth.Get())
				cmds.setAttr(name + "Shape.goalWeight[0]", self.sliderParticleGoalWeight.Get())
				cmds.setAttr(name + "Shape.conserve", self.sliderParticleConserve.Get())
				cmds.setAttr(name + "Shape.drag", self.sliderParticleDrag.Get())
				cmds.setAttr(name + "Shape.damp", self.sliderParticleDamp.Get())
		
		SetParticleAttributes(self.particleBase)
		SetParticleAttributes(self.particleTarget)
		SetParticleAttributes(self.particleUp)
	def ResetSettings(self, *args): # TODO move values to settings
		### Options
		self.menuCheckboxHierarchy.Reset()
		self.menuCheckboxLayer.Reset()
		self.menuCheckboxLoop.Reset()
		self.menuCheckboxDeleteSetup.Reset()
		# self.menuCheckboxCollisions.Reset()

		### Loop cycles
		cmds.menuItem(self.menuRadioButtonsLoop[2], edit = True, radioButton = True)

		### Aim offset target
		cmds.floatField(self.aimOffsetFloatGroup[1], edit = True, value = 10)
		self.aimOffsetCheckbox.Reset()
		cmds.radioCollection(self.aimOffsetRadioCollection[0], edit = True, select = self.aimOffsetRadioCollection[1][0])

		### Aim offset up
		cmds.floatField(self.aimOffsetUpFloatGroup[1], edit = True, value = 10)
		self.aimOffsetUpCheckbox.Reset()
		cmds.radioCollection(self.aimOffsetUpRadioCollection[0], edit = True, select = self.aimOffsetUpRadioCollection[1][1])

		### Nucleus
		self.sliderNucleusTimeScale.Reset()

		### Particle dynamic properties
		self.sliderParticleRadius.Reset()
		self.sliderParticleGoalSmooth.Reset()
		self.sliderParticleGoalWeight.Reset()
		self.sliderParticleConserve.Reset()
		self.sliderParticleDrag.Reset()
		self.sliderParticleDamp.Reset()
	

	### VALUES
	def GetLoopCyclesIndex(self):
		for i, item in enumerate(self.menuRadioButtonsLoop):
			if cmds.menuItem(item, query = True, radioButton = True):
				return i
		return -1


	### BAKE ANIMATION
	def BakeParticleLogic(self, parent, translation=False, rotation=False, combo=False, *args):
		### Check created setups
		if (not combo):
			if (translation and not self.setupCreatedPoint):
				cmds.warning("Point setup is not created")
				return
			if (rotation and not self.setupCreatedAim):
				cmds.warning("Aim setup is not created")
				return

		### Get raw attributes
		attributesType = ()
		if (combo):
			attributesType = Enums.Attributes.translateLong + Enums.Attributes.rotateLong
		else:
			if (translation):
				attributesType = Enums.Attributes.translateLong
			if (rotation):
				attributesType = attributesType + Enums.Attributes.rotateLong
			if (len(attributesType) == 0):
				cmds.warning("No baking attributes specified")
				return
		
		### Construct attributes with object name
		attributes = []
		for i in range(len(attributesType)):
			attributes.append("{0}.{1}".format(self.selectedObjects, attributesType[i]))
		
		### Filter attributes
		attributesFiltered = Attributes.FilterAttributesAnimatable(attributes = attributes, skipMutedKeys = True)
		if (attributesFiltered == None):
			self.ParticleSetupDelete()
			return
		
		### Cut object name from attributes
		for i in range(len(attributesFiltered)):
			attributesFiltered[i] = attributesFiltered[i].replace(self.selectedObjects + ".", "")
		
		### Set time range
		self.time.Scan()
		startTime = self.time.values[2]
		self.time.SetCurrent(startTime)
		if (self.menuCheckboxLoop.Get()):
			startTime = self.time.values[2] - self.time.values[3] * self.GetLoopCyclesIndex()
			self.time.SetMin(startTime)
			self.time.SetCurrent(startTime)
		cmds.setAttr(self.nucleus1 + ".startFrame", startTime) # TODO bug when select ovlp objects
		if (cmds.objExists(self.nucleus2)):
			cmds.setAttr(self.nucleus2 + ".startFrame", startTime)

		### Set key for target object attributes
		cmds.setKeyframe(self.selectedObjects, attribute = attributesFiltered)

		### Start logic
		name = "_rebake_" + Text.ConvertSymbols(self.selectedObjects)
		objectDuplicate = cmds.duplicate(self.selectedObjects, name = name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		cmds.select(clear = True)
		for attribute in Enums.Attributes.translateLong:
			cmds.setAttr(objectDuplicate[0] + "." + attribute, lock = False)
		for attribute in Enums.Attributes.rotateLong:
			cmds.setAttr(objectDuplicate[0] + "." + attribute, lock = False)
		cmds.parentConstraint(parent, objectDuplicate, maintainOffset = True) # skipTranslate
		cmds.select(objectDuplicate, replace = True)

		### Bake animation
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		Constraints.DeleteConstraints(objectDuplicate)

		### Copy keys, create layers and paste keys
		cmds.copyKey(objectDuplicate, time = (self.time.values[2], self.time.values[3]), attribute = attributesFiltered)
		if (self.menuCheckboxLayer.Get()):
			if (combo):
				name = OverlappySettings.nameLayers[4] + self.selectedObjects
			else:
				if (translation):
					name = OverlappySettings.nameLayers[2] + self.selectedObjects
				elif (rotation):
					name = OverlappySettings.nameLayers[3] + self.selectedObjects
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
			self.ParticleSetupDelete()
	def BakeParticleVariants(self, variant, *args): # TODO rework
		# selected = Selector.MultipleObjects()
		# if (selected == None):
		# 	return
		
		### TODO Check zero particle offset
		# if variant in [3, 4, 5]:
		# 	checkOffsetX = self.slidersParticleOffset[0].Get() == 0
		# 	checkOffsetY = self.slidersParticleOffset[1].Get() == 0
		# 	checkOffsetZ = self.slidersParticleOffset[2].Get() == 0
		# 	if (checkOffsetX and checkOffsetY and checkOffsetZ):
		# 		dialogResult = cmds.confirmDialog(
		# 			title = "Zero particle offset detected",
		# 			message = "For ROTATION BAKING, set the particle offset to non-zero values.\nIf all XYZ values are zero, the particle will stay in the same position as the original object, and no rotation will occur.\n",
		# 			messageAlign = "left",
		# 			icon = "warning",
		# 			button = ["Continue anyway", "Cancel"],
		# 			annotation = ["Bake with zero offset, no useful animation will be baked", "Cancel baking operation"],
		# 			defaultButton = "Cancel",
		# 			cancelButton = "Cancel",
		# 			dismissString = "TODO: dismissString"
		# 			)
		# 		if (dialogResult == "Cancel"):
		# 			cmds.warning("Overlappy Rotation Baking cancelled")
		# 			return

		MayaSettings.CachedPlaybackDeactivate()

		### TODO Check hierarchy and get objects
		# if (self.menuCheckboxHierarchy.Get()):
		# 	selected = Selector.SelectHierarchyTransforms()

		### Run baking process
		if (variant == 1): # Translation
			self.BakeParticleLogic(self.particleLocator, translation = True)
		elif (variant == 2): # Rotation
			self.BakeParticleLogic(self.particleLocatorAim, rotation = True)
		elif (variant == 3): # Translation + Rotation
			self.BakeParticleLogic(self.particleLocatorAim, combo = True)
		
		### TODO
		# for i in range(len(selected)):
		# 	cmds.select(selected[i], replace = True)
			# self._ParticleSetupPoint()
			# RunBakeLogicVariant()
		
		### TODO Select original objects
		# cmds.select(selected, replace = True)


	### LAYERS
	def LayerCreate(self, name, *args): # TODO additional naming for translation and rotation
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
		
		layer1 = OverlappySettings.nameLayers[id[0]]
		layer2 = OverlappySettings.nameLayers[id[1]]


		### Check source layer
		if (not cmds.objExists(layer1)):
			cmds.warning("Layer \"{0}\" doesn't exist".format(layer1))
			return
		

		### Get selected layers
		selectedLayers = []
		for animLayer in cmds.ls(type = "animLayer"):
			if cmds.animLayer(animLayer, query = True, selected = True):
				selectedLayers.append(animLayer)
		

		### Check selected count
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
		

		### Create safe layer
		if (not cmds.objExists(layer2)):
			self.layers[id[1]] = cmds.animLayer(layer2, override = True)
		

		### Move children or selected layers
		for layer in filteredLayers:
			cmds.animLayer(layer, edit = True, parent = self.layers[id[1]])
		

		### Delete TEMP layer if no children
		if (len(filteredLayers) == len(children)):
			Layers.Delete(layer1)

