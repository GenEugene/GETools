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
from ..experimental import Physics
from ..experimental import PhysicsParticle


# TODO make cycle infinity before loop bake


class OverlappyAnnotations: # TODO simplify
	### Setup
	setup = "Create particle rig for first selected object. Use this step for setup settings. \nSetup runs every time for each selected object."
	setupDelete = "Delete particle rig if exists"

	### Baking
	translation = "Bake simulation for translation attributes"
	translationWithOffset = "Bake simulation for translation attributes with offset"
	rotation = "Bake simulation for rotation attributes"
	comboTranslateRotate = "Bake translation and rotation in order"
	comboRotateTranslate = "Bake rotation and translation in order"
	scale = "Bake simulation for scale attributes"

	### Layers
	layerDeleteBase = "All animation layers will be deleted"
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

	### Particle
	particleRadius = "Particle Radius"
	particleConserve = "Particle Conserve"
	particleDrag = "Particle Drag"
	particleDamp = "Particle Damp"
	particleGoalSmooth = "Particle Goal Smooth"
	particleGoalWeight = "Particle Goal Weight"
	particleTimeScale = "Nucleus Time Scale"

	### Offset
	offsetMirrorX = "Mirror particle offset value to opposite"
	offsetMirrorY = offsetMirrorX
	offsetMirrorZ = offsetMirrorX
	offsetX = "Move particle from original object. Important to use offset for Rotation baking"
	offsetY = offsetX
	offsetZ = offsetX

class OverlappySettings: # TODO simplify
	# NAMING
	prefix = "ovlp"
	prefixLayer = "_" + prefix
	nameLayers = (prefixLayer + "TEMP_", prefixLayer + "SAFE_", "pos_", "rot_")
	nameGroup = prefix + "Group"

	# XXX remove later
	# nameNucleus = prefix + "Nucleus"
	# nameParticleTarget = prefix + "ParticleTarget"
	# nameLocGoalTarget = (prefix + "LocGoal", prefix + "LocTarget")
	# nameLocAim = (prefix + "LocAimBase", prefix + "LocAimHidden", prefix + "LocAim", prefix + "LocAimUp")
		
	# SETTINGS CHECKBOXES # TODO: move to preset
	optionCheckboxHierarchy = False
	optionCheckboxLayer = True
	optionCheckboxLoop = False
	optionCheckboxClean = True
	optionCheckboxCollisions = True

	loopBakeOffset = 2 # TODO set count of pre cycles via ui

	# SETTINGS DYNAMIC PROPERTIES # TODO: move to preset
	particleRadius = 5
	particleConserve = 1
	particleDrag = 0.01
	particleDamp = 0
	particleGoalSmooth = 1
	particleGoalWeight = 0.2
	nucleusTimeScale = 1
	
	# SLIDERS (field min/max, slider min/max)
	rangePRadius = (0, float("inf"), 0, 10)
	rangePConserve = (0, 1, 0, 1)
	rangePDrag = (0, 10, 0, 1)
	rangePDamp = (0, 10, 0, 1)
	rangeGSmooth = (0, 100, 0, 10)
	rangeGWeight = (0, 1, 0, 1)
	rangeNucleusTimeScale = (0.001, 100, 0.001, 4)
	# rangeOffsetX = (float("-inf"), float("inf"), 0, 100) # XXX
	# rangeOffsetY = (float("-inf"), float("inf"), 0, 100) # XXX
	# rangeOffsetZ = (float("-inf"), float("inf"), 0, 100) # XXX

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
		self.time = Timeline.TimeRangeHandler()
		
		### OBJECTS
		self.selectedObjects = ""
		self.layers = ["", ""]
		self.nucleus = ""
		# self.nucleusNodesBefore = [""] # TODO
		# self.nucleusNodesAfter = [""] # TODO
		## self.colliderObjects = [] # XXX
		## self.colliderNodes = [] # XXX

		### PARTICLE MODE
		self.particle = "" # TODO rename later to "self.particleTarget"
		# self.particleUp = ""
		self.particleLocGoalTarget = ["", ""]
		self.particleLocAim = ["", "", "", ""]
		self.particleGoalStartPosition = [None, (0, 0, 0)] # TODO simplify
		
		### UI LAYOUTS
		self.layoutBake = None
		self.layoutLayers = None
		self.layoutCollisions = None # TODO
		self.layoutChainMode = None # TODO
		self.layoutChainButtons = None
		self.layoutChainDynamicProperties = None # TODO
		self.layoutParticleMode = None
		self.layoutParticleButtons = None
		self.layoutParticleDynamicProperties = None
		self.layoutParticleOffset = None
		
		### UI MENU OPTIONS
		self.menuCheckboxHierarchy = None
		self.menuCheckboxLayer = None
		self.menuCheckboxLoop = None
		self.menuCheckboxClean = None
		self.menuCheckboxCollisions = None # TODO
		self.menuRadioButtonsLoop = [None, None, None, None]

		### UI AIM OFFSET
		## self.checkboxAutoOffset = None # TODO
		self.aimOffsetFloatGroup = [None, None] # text, float
		self.aimOffsetRadioCollection = [None, [None, None, None]] # collection, (element 1, 2, 3)
		self.aimOffsetCheckbox = None
		self.aimOffsetUpFloatGroup = [None, None] # text, float
		self.aimOffsetUpRadioCollection = [None, [None, None, None]] # collection, (element 1, 2, 3)
		self.aimOffsetUpCheckbox = None
		
		### UI SLIDERS PARTICLE DYNAMIC PROPERTIES
		self.sliderParticleRadius = None
		self.sliderParticleConserve = None
		self.sliderParticleDrag = None
		self.sliderParticleDamp = None
		self.sliderParticleGoalSmooth = None
		self.sliderParticleGoalWeight = None
		self.sliderNucleusTimeScale = None
		# self.slidersParticleOffset = [None, None, None] # XXX

		### UI SCROLL LISTS
		self.scrollListColliders = None
	def UICreate(self, layoutMain):
		self.UILayoutMenuBar(layoutMain)
		self.UILayoutBake(layoutMain)
		self.UILayoutLayers(layoutMain)
		## self.UILayoutCollisions(layoutMain) # TODO
		## self.UILayoutChainMode(layoutMain) # TODO
		self.UILayoutParticleMode(layoutMain)
	

	### MAIN UI
	def UILayoutMenuBar(self, layoutMain):
		cmds.columnLayout("layoutMenuBar", parent = layoutMain, adjustableColumn = True, width = Settings.windowWidthMargin)
		cmds.menuBarLayout()

		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Reset Settings", command = self._ResetAllValues, image = Icons.rotateClockwise)
		
		cmds.menu(label = "Options", tearOff = True)
		self.menuCheckboxHierarchy = UI.MenuCheckbox(label = "Use Hierarchy", value = OverlappySettings.optionCheckboxHierarchy, valueDefault = OverlappySettings.optionCheckboxHierarchy)
		self.menuCheckboxLayer = UI.MenuCheckbox(label = "Bake To Layer", value = OverlappySettings.optionCheckboxLayer, valueDefault = OverlappySettings.optionCheckboxLayer)
		self.menuCheckboxLoop = UI.MenuCheckbox(label = "Loop Mode", value = OverlappySettings.optionCheckboxLoop, valueDefault = OverlappySettings.optionCheckboxLoop)
		self.menuCheckboxClean = UI.MenuCheckbox(label = "Clean After Bake", value = OverlappySettings.optionCheckboxClean, valueDefault = OverlappySettings.optionCheckboxClean)
		self.menuCheckboxCollisions = UI.MenuCheckbox(label = "Collisions", value = OverlappySettings.optionCheckboxCollisions, valueDefault = OverlappySettings.optionCheckboxCollisions)

		cmds.menuItem(dividerLabel = "Pre Loop Cycles", divider = True)
		
		# TODO connect loop settings
		cmds.radioCollection()
		self.menuRadioButtonsLoop[0] = cmds.menuItem(label = "0", radioButton = True, command = lambda *args: print("Option 0 selected"))
		self.menuRadioButtonsLoop[1] = cmds.menuItem(label = "1", radioButton = True, command = lambda *args: print("Option 1 selected"))
		self.menuRadioButtonsLoop[2] = cmds.menuItem(label = "2", radioButton = True, command = lambda *args: print("Option 2 selected"))
		self.menuRadioButtonsLoop[3] = cmds.menuItem(label = "3", radioButton = True, command = lambda *args: print("Option 3 selected"))
		cmds.menuItem(self.menuRadioButtonsLoop[2], edit = True, radioButton = True)
	def UILayoutBake(self, layoutMain):
		### SETUP
		self.layoutBake = cmds.frameLayout("layoutBake", label = Settings.frames2Prefix + "BAKE", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutBake, adjustableColumn = True)

		count = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		##
		cmds.button(label = "Translation", command = partial(self._BakeParticleVariants, 1), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.translation)
		cmds.popupMenu()
		cmds.menuItem(label = "Translate With Offset", command = partial(self._BakeParticleVariants, 2)) # TODO popup message if offsets are zero
		##
		cmds.button(label = "Rotation", command = partial(self._BakeParticleVariants, 3), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.rotation) # TODO popup message if offsets are zero
		##
		cmds.button(label = "Combo", command = partial(self._BakeParticleVariants, 4), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.comboTranslateRotate) # TODO popup message if offsets are zero
		cmds.popupMenu()
		cmds.menuItem(label = "Rotate + Translate", command = partial(self._BakeParticleVariants, 5))
		##
		## cmds.button(label = "SCALE", command = partial(self._BakeParticleVariants, 6), backgroundColor = Colors.orange10, annotation = OverlappyAnnotations.scale) # TODO implement scale simulation
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
		cmds.button(label = "Move To Safe Layer", command = partial(self._LayerMoveToSafeOrTemp, True), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveTemp)
		
		cmds.button(label = "Delete Safe layer", command = partial(Layers.Delete, OverlappySettings.nameLayers[1]), backgroundColor = Colors.red10, annotation = OverlappyAnnotations.layerDeleteSafe)
		cmds.button(label = "Move To Temp Layer", command = partial(self._LayerMoveToSafeOrTemp, False), backgroundColor = Colors.blue10, annotation = OverlappyAnnotations.layerMoveSafe)
	def UILayoutCollisions(self, layoutMain): # TODO
		self.layoutCollisions = cmds.frameLayout("layoutCollisions", label = Settings.frames2Prefix + "COLLISIONS - WORK IN PROGRESS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutCollisions, adjustableColumn = True)
		
		count = 4
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		##
		cmds.button(label = "Add", backgroundColor = Colors.green10)
		cmds.button(label = "Remove", backgroundColor = Colors.red10)
		cmds.button(label = "Refresh", backgroundColor = Colors.yellow10)
		cmds.button(label = "Clear", backgroundColor = Colors.red50)

		# TODO Scroll list with colliders
		## https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/textScrollList.html
		layoutScroll = cmds.frameLayout("layoutScroll", label = "Colliders List", labelIndent = 80, parent = self.layoutCollisions, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		self.scrollListColliders = cmds.textScrollList(parent = layoutScroll, allowMultiSelection = True, height = 120)

		for i in range(20): # test list items
			cmds.textScrollList(self.scrollListColliders, edit = True, append = "item {0}".format(i))

		## append
		## selectItem
		## deselectAll
		## removeAll
		## doubleClickCommand
	
	
	### CHAIN UI
	def UILayoutChainMode(self, layoutMain): # TODO
		self.layoutChainMode = cmds.frameLayout("layoutChainMode", label = Settings.frames2Prefix + "CHAIN MODE - WORK IN PROGRESS", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		
		# cmds.menuBarLayout()
		# cmds.menu(label = "Edit")
		# cmds.menuItem(label = "Reset Settings", command = self._ResetAllChainValues, image = Icons.rotateClockwise)
				
		## self.UILayoutChainButtons(self.layoutChainMode)
		self.UILayoutChainDynamicProperties(self.layoutChainMode)
	def UILayoutChainButtons(self, layoutMain): # TODO
		## SETUP
		self.layoutChainButtons = cmds.frameLayout("layoutChainButtons", label = "Buttons", labelIndent = 100, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutChainButtons, adjustableColumn = True)

		## count = 2
		## cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		##
		## cmds.button(label = "CREATE", command = PhysicsHair.CreateNHairOnSelected, backgroundColor = Colors.green10) # TODO annotation
		## cmds.button(label = "REMOVE", command = self._SetupDelete, backgroundColor = Colors.red10, annotation = OverlappyAnnotations.setupDelete)
	def UILayoutChainDynamicProperties(self, layoutMain): # TODO
		self.layoutChainDynamicProperties = cmds.frameLayout("layoutChainDynamicProperties", label = "Dynamic Properties", labelIndent = 70, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
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

		pass
	
	
	### PARTICLE UI
	def UILayoutParticleMode(self, layoutMain):
		self.layoutParticleMode = cmds.frameLayout("layoutParticleMode", label = Settings.frames2Prefix + "PARTICLE MODE", parent = layoutMain, collapsable = True, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		
		cmds.menuBarLayout()
		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Reset Settings", command = self._ResetAllParticleValues, image = Icons.rotateClockwise)

		cmds.menu(label = "Select", tearOff = True)
		cmds.menuItem(label = "Object", command = self._SelectSelectedObjects, image = Icons.cursor)
		# cmds.menuItem(label = "Particle", command = self._SelectParticleObject, image = Icons.particle)
		# cmds.menuItem(label = "Nucleus", command = self._SelectNucleus, image = Icons.nucleus)
		# cmds.menuItem(label = "Target locator", command = self._SelectParticleTarget, image = Icons.locator)
		# cmds.menuItem(label = "Aim locator", command = self._SelectParticleAim, image = Icons.locator)
		
		self.UILayoutParticleButtons(self.layoutParticleMode)
		self.UILayoutParticleOffset(self.layoutParticleMode)
		self.UILayoutParticleDynamicProperties(self.layoutParticleMode)
	def UILayoutParticleButtons(self, layoutMain):
		### SETUP
		self.layoutParticleButtons = cmds.frameLayout("layoutParticleButtons", label = "Create Particle Rig", labelIndent = 70, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleButtons, adjustableColumn = True)

		count = 3
		cmds.gridLayout(parent = layoutColumn, numberOfColumns = count, cellWidth = Settings.windowWidthMargin / count, cellHeight = Settings.lineHeight)
		##
		cmds.button(label = "Point", command = self._ParticleSetupPoint, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setup)
		cmds.button(label = "Aim", command = self._ParticleSetupAim, backgroundColor = Colors.green10, annotation = OverlappyAnnotations.setup)
		## cmds.button(label = "Scan setup in scene", command = self._SetupScan, backgroundColor = Colors.green10)
		cmds.button(label = "Remove", command = self._ParticleSetupDelete, backgroundColor = Colors.red10, annotation = OverlappyAnnotations.setupDelete)
	def UILayoutParticleOffset(self, layoutMain): # TODO
		self.layoutParticleOffset = cmds.frameLayout("layoutParticleOffset", label = "Aim Offset", labelIndent = 85, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
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
	def GetAimOffsetValues(self):
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
		
		return (valueAimFloat, (valueAimAxisX, valueAimAxisY, valueAimAxisZ), valueAimCheckbox), (valueAimUpFloat, (valueAimUpAxisX, valueAimUpAxisY, valueAimUpAxisZ), valueAimUpCheckbox) # aimTarget, aimUp
	def UILayoutParticleDynamicProperties(self, layoutMain):
		self.layoutParticleDynamicProperties = cmds.frameLayout("layoutParticleDynamicProperties", label = "Dynamic Properties", labelIndent = 70, parent = layoutMain, collapsable = False, backgroundColor = Settings.frames2Color, marginWidth = 0, marginHeight = 0)
		layoutColumn = cmds.columnLayout(parent = self.layoutParticleDynamicProperties, adjustableColumn = True)
		## cmds.popupMenu()
		## cmds.menuItem(label = "Right-Click") # TODO add reset all function

		commandDefault = self._ParticleDynamicPropertiesUpdate

		layoutSliders1 = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)
		self.sliderParticleRadius = UI.Slider(
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

		## cmds.separator(parent = self.layoutSimulation, style = "in", height = 1)
		cmds.separator(parent = layoutColumn, style = "in")
		
		layoutSliders2 = cmds.gridLayout(parent = layoutColumn, numberOfColumns = 1, cellWidth = Settings.windowWidthMargin, cellHeight = Settings.lineHeight)
		self.sliderParticleConserve = UI.Slider(
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
		
		self.sliderParticleDrag = UI.Slider(
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
		
		self.sliderParticleDamp = UI.Slider(
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
		
		self.sliderParticleGoalSmooth = UI.Slider(
			parent = layoutSliders2,
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
			parent = layoutSliders2,
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
		
		self.sliderNucleusTimeScale = UI.Slider(
			parent = layoutSliders2,
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


	### PARTICLE LOGIC
	def _ParticleSetupInit(self, *args):
		### Get min/max anim range time and reset time slider
		self.time.Scan()
		self.time.SetCurrent(self.time.values[2])
		
		### Remove previous setup if exists
		self._ParticleSetupDelete(deselect = False)
		
		### Get selected objects
		self.selectedObjects = Selector.MultipleObjects(minimalCount = 1)
		if (self.selectedObjects == None):
			self.selectedObjects = ""
			return
		
		self.selectedObjects = self.selectedObjects[0]

		### Create group
		cmds.select(clear = True)
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		cmds.group(empty = True, name = OverlappySettings.nameGroup)

		### Create nucleus node
		self.nucleus = Physics.CreateNucleus(name = OverlappySettings.prefix + PhysicsParticle._defaultNameNucleus, parent = OverlappySettings.nameGroup)
		cmds.select(clear = True)

	def _ParticleSetupPoint(self, *args):
		self._ParticleSetupInit()
		particleSetup = PhysicsParticle.CreateParticleSetup(targetObject = self.selectedObjects, nucleusNode = self.nucleus, parentGroup = OverlappySettings.nameGroup)
		cmds.select(self.selectedObjects, replace = True)

		self.particle = particleSetup[4]


	def _ParticleSetupAim(self, *args):
		self._ParticleSetupInit()

		### Get aim offset values from UI and put to aim target offset and aim up offset
		valuesAimOffset = self.GetAimOffsetValues()

		valueAimTarget = valuesAimOffset[0][0] * (-1 if valuesAimOffset[0][2] else 1)
		valueAimUp = valuesAimOffset[1][0] * (-1 if valuesAimOffset[1][2] else 1)

		offsetTarget = [0, 0, 0]
		offsetUp = [0, 0, 0]

		if (valuesAimOffset[0][1][0]):
			offsetTarget = [valueAimTarget, 0, 0]
		if (valuesAimOffset[0][1][1]):
			offsetTarget = [0, valueAimTarget, 0]
		if (valuesAimOffset[0][1][2]):
			offsetTarget = [0, 0, valueAimTarget]
		
		if (valuesAimOffset[1][1][0]):
			offsetUp = [valueAimUp, 0, 0]
		if (valuesAimOffset[1][1][1]):
			offsetUp = [0, valueAimUp, 0]
		if (valuesAimOffset[1][1][2]):
			offsetUp = [0, 0, valueAimUp]
		
		particleSetup = PhysicsParticle.CreateParticleSetup(targetObject = self.selectedObjects, nucleusNode = self.nucleus, parentGroup = OverlappySettings.nameGroup, positionOffset = offsetTarget)
		particleAimSetup = PhysicsParticle.CreateAimSetup(particleSetup, positionOffset = offsetUp)


		### TODO Names
		# objConverted = Text.ConvertSymbols(self.selectedObjects)
		# nameLocGoal = OverlappySettings.nameLocGoalTarget[0] + objConverted
		# nameLocParticle = OverlappySettings.nameLocGoalTarget[1] + objConverted
		# nameNucleus = OverlappySettings.nameNucleus + objConverted
		# nameParticle = OverlappySettings.nameParticleTarget + objConverted
		# nameLocAimBase = OverlappySettings.nameLocAim[0] + objConverted
		# nameLocAimHidden = OverlappySettings.nameLocAim[1] + objConverted
		# nameLocAim = OverlappySettings.nameLocAim[2] + objConverted
		# nameLocAimUp = OverlappySettings.nameLocAim[3] + objConverted

		### TODO Create locator for goal
		# self.particleLocGoalTarget[0] = cmds.spaceLocator(name = nameLocGoal)[0]
		# cmds.parent(self.particleLocGoalTarget[0], OverlappySettings.nameGroup)
		# cmds.matchTransform(self.particleLocGoalTarget[0], self.selectedObjects, position = True, rotation = True)
		# cmds.parentConstraint(self.selectedObjects, self.particleLocGoalTarget[0], maintainOffset = True)
		# cmds.setAttr(self.particleLocGoalTarget[0] + ".visibility", 0)
		# self.particleGoalStartPosition[0] = cmds.xform(self.particleLocGoalTarget[0], query = True, translation = True)

		### TODO Nucleus node
		# self.nucleusNodesBefore = cmds.ls(type = "nucleus")
		# self.nucleus = cmds.createNode("nucleus", name = nameNucleus)
		# cmds.connectAttr("time1.outTime", self.nucleus + ".currentTime")
		# cmds.parent(self.nucleus, OverlappySettings.nameGroup)
		# ## self.sliderNTimeScale.startName = self.nucleus
		# cmds.setAttr(self.nucleus + ".gravity", 0)
		# cmds.setAttr(self.nucleus + ".timeScale", self.sliderNucleusTimeScale.Get())
		# cmds.setAttr(self.nucleus + ".startFrame", self.time.values[2])
		# cmds.setAttr(self.nucleus + ".visibility", 0)


		### TODO Connect collision nRigid nodes to nucleus # TODO Need to define colliderObject before this logic
		# self.colliderNodes[0] = cmds.createNode("nRigid", name = "myNRigid")
		# cmds.connectAttr("time1.outTime", self.colliderNodes[0] + ".currentTime")
		# cmds.connectAttr(self.colliderObjects[0] + ".worldMesh[0]", self.colliderNodes[0] + ".inputMesh")
		# cmds.connectAttr(self.colliderNodes[0] + ".currentState", self.nucleus + ".inputPassive[0]")
		# cmds.connectAttr(self.colliderNodes[0] + ".startState", self.nucleus + ".inputPassiveStart[0]")
		# cmds.connectAttr(self.nucleus + ".startFrame", self.colliderNodes[0] + ".startFrame")


		### TODO Create particle, goal and get selected object position
		# position = cmds.xform(self.selectedObjects, query = True, worldSpace = True, rotatePivot = True)
		# self.particle = cmds.nParticle(name = nameParticle, position = position, conserve = 1)[0]
		# cmds.goal(useTransformAsGoal = True, goal = self.particleLocGoalTarget[0])
		# cmds.parent(self.particle, OverlappySettings.nameGroup)
		# ## self.startPositionGoalParticle[1] = cmds.xform(self.particle, query = True, translation = True)
		# cmds.setAttr(self.particle + ".overrideEnabled", 1)
		# cmds.setAttr(self.particle + ".overrideDisplayType", 2)

		### TODO Reconnect particle to temp nucleus and remove extra nodes
		# mel.eval("assignNSolver {0}".format(nameNucleus))
		# self.nucleusNodesAfter = cmds.ls(type = "nucleus")
		# nodesForRemoving = [item for item in self.nucleusNodesAfter if item not in self.nucleusNodesBefore]
		# for item in nodesForRemoving:
		# 	if (item != self.nucleus):
		# 		## cmds.warning("extra node deleted {0}".format(item))
		# 		cmds.delete(item)

		### TODO Set simulation attributes
		# cmds.setAttr(self.particle + "Shape.radius", self.sliderParticleRadius.Get())
		# cmds.setAttr(self.particle + "Shape.solverDisplay", 1)
		# cmds.setAttr(self.particle + "Shape.conserve", self.sliderParticleConserve.Get())
		# cmds.setAttr(self.particle + "Shape.drag", self.sliderParticleDrag.Get())
		# cmds.setAttr(self.particle + "Shape.damp", self.sliderParticleDamp.Get())
		# cmds.setAttr(self.particle + "Shape.goalSmoothness", self.sliderParticleGoalSmooth.Get())
		# cmds.setAttr(self.particle + "Shape.goalWeight[0]", self.sliderParticleGoalWeight.Get())

		### TODO Create and connect locator to particle
		# self.particleLocGoalTarget[1] = cmds.spaceLocator(name = nameLocParticle)[0]
		# cmds.parent(self.particleLocGoalTarget[1], OverlappySettings.nameGroup)
		# cmds.matchTransform(self.particleLocGoalTarget[1], self.selectedObjects, position = True, rotation = True)
		# cmds.connectAttr(self.particle + ".center", self.particleLocGoalTarget[1] + ".translate", force = True)
		# cmds.setAttr(self.particleLocGoalTarget[1] + ".visibility", 0)

		### TODO Create base aim locator
		# self.particleLocAim[0] = cmds.spaceLocator(name = nameLocAimBase)[0]
		# cmds.parent(self.particleLocAim[0], OverlappySettings.nameGroup)
		# cmds.matchTransform(self.particleLocAim[0], self.selectedObjects, position = True, rotation = True)
		# cmds.parentConstraint(self.selectedObjects, self.particleLocAim[0], maintainOffset = True)
		# cmds.setAttr(self.particleLocAim[0] + ".visibility", 0)

		### TODO Create hidden aim locator
		# self.particleLocAim[1] = cmds.spaceLocator(name = nameLocAimHidden)[0]
		# cmds.matchTransform(self.particleLocAim[1], self.particleLocAim[0], position = True, rotation = True)
		# cmds.parent(self.particleLocAim[1], self.particleLocAim[0])
		# cmds.aimConstraint(self.particleLocGoalTarget[1], self.particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		# cmds.delete(self.particleLocAim[1] + "_aimConstraint1")
		# self.particleLocAim[3] = cmds.duplicate(self.particleLocAim[1], name = nameLocAimUp)[0]
		# cmds.parent(self.particleLocAim[3], self.particleLocAim[1])
		# cmds.setAttr(self.particleLocAim[3] + ".ty", 100)
		# cmds.parent(self.particleLocAim[3], self.particleLocAim[0])
		# cmds.aimConstraint(self.particleLocGoalTarget[1], self.particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.particleLocAim[3]) # "scene" "object" "objectrotation" "vector" "none"
		
		### TODO Create aim locator
		# self.particleLocAim[2] = cmds.spaceLocator(name = nameLocAim)[0]
		# cmds.matchTransform(self.particleLocAim[2], self.particleLocAim[0], position = True, rotation = True)
		# cmds.parent(self.particleLocAim[2], self.particleLocAim[0])

		### Offset
		# self._ParticleOffsetsUpdate(cacheReset = True) # TODO
		cmds.select(self.selectedObjects, replace = True)
	
	# def _ParticleSetupScan(self, *args): # TODO extract old logic and delete
	# 	# Check overlappy group
	# 	if (not cmds.objExists(OverlappySettings.nameGroup)):
	# 		cmds.warning("Overlappy object doesn't exists")
	# 		return
		
	# 	# Get children of group
	# 	children = cmds.listRelatives(OverlappySettings.nameGroup)
	# 	if (len(children) == 0):
	# 		cmds.warning("Overlappy object has no children objects")
	# 		return
		
	# 	# Try to get suffix name
	# 	tempList = (OverlappySettings.nameLocGoalTarget[0], OverlappySettings.nameLocGoalTarget[1], self.particle, OverlappySettings.nameLocAim[0])
	# 	objectName = ""
	# 	for child in children:
	# 		for item in tempList:
	# 			splitNames = child.split(item)
	# 			if (len(splitNames) < 2):
	# 				continue
	# 			lastName = splitNames[-1]
	# 			if (objectName == ""):
	# 				objectName = lastName
	# 			else:
	# 				if (objectName == lastName):
	# 					continue
	# 				else:
	# 					cmds.warning("Suffix \"{0}\" don't equals to \"{1}\"".format(objectName, lastName))
	# 	converted = Text.ConvertSymbols(objectName, False)
	# 	if (cmds.objExists(converted)):
	# 		self.selectedObjects = converted
		
	# 	def CheckAndSet(name):
	# 		if (cmds.objExists(name + objectName)):
	# 			return name + objectName
	# 		else:
	# 			return
		
	# 	# Objects
	# 	self.particleLocGoalTarget[0] = CheckAndSet(OverlappySettings.nameLocGoalTarget[0])
	# 	self.particleLocGoalTarget[1] = CheckAndSet(OverlappySettings.nameLocGoalTarget[1])
	# 	self.particleLocAim[0] = CheckAndSet(OverlappySettings.nameLocAim[0])
	# 	self.particleLocAim[1] = CheckAndSet(OverlappySettings.nameLocAim[1])
	# 	self.particleLocAim[2] = CheckAndSet(OverlappySettings.nameLocAim[2])
	# 	self.particle = CheckAndSet(self.particle)
		
	# 	# Time and offset
	# 	self.time.Scan()
	# 	self.time.SetCurrent(self.time.values[2])
	# 	self.particleGoalStartPosition[0] = cmds.xform(self.particleLocAim[0], query = True, translation = True)
	# 	self.time.SetCurrentCached()
		
	# 	# Nucleus
	# 	# _nucleus = cmds.ls(type = "nucleus")
	# 	# if (len(_nucleus) > 0):
	# 	# 	self.nucleus = _nucleus[0]
	# 		# self.sliderNTimeScale.startName = self.nucleus
		
	# 	# Get sliders
	# 	# self.sliderPRadius.Scan()
	# 	# self._GetSimulation()
	# 	# self._GetOffsets()
	# 	pass
	
	
	def _ParticleSetupDelete(self, deselect=True, *args): # TODO simplify redundancy
		self.selectedObjects = ""
		self.particleLocGoalTarget = ["", ""]
		self.particleLocAim = ["", "", "", ""]
		self.particle = ""
		self.nucleus = ""
		
		### Delete group
		if (cmds.objExists(OverlappySettings.nameGroup)):
			cmds.delete(OverlappySettings.nameGroup)
		
		if (deselect):
			cmds.select(clear = True)
	def _ParticleOffsetsUpdate(self, cacheReset=False, *args): # TODO rework with new aim offset logic
		if (type(cacheReset) is float):
			cacheReset = False
		
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

		self._ParticleOffsetSetValues()

		checkSelected = self.selectedObjects == "" or not cmds.objExists(self.selectedObjects)
		checkGoal = not cmds.objExists(self.particleLocGoalTarget[0])
		checkAim = not cmds.objExists(self.particleLocAim[2])
		checkStartPos = self.particleGoalStartPosition[0] == None
		
		if (checkSelected or checkGoal or checkAim or checkStartPos):
			return

		cmds.currentTime(self.time.values[2])

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
		# 	self.particleLocGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateX",
		# 	self.particleLocGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateY",
		# 	self.particleLocGoalTarget[0] + "_parentConstraint1.target[0].targetOffsetTranslateZ",
		# 	)
		# cmds.setAttr(goalAttributes[0], values[0])
		# cmds.setAttr(goalAttributes[1], values[1])
		# cmds.setAttr(goalAttributes[2], values[2])
		
		### TODO Get offset
		goalPosition = cmds.xform(self.particleLocGoalTarget[0], query = True, translation = True)
		goalOffset = (
			self.particleGoalStartPosition[0][0] - goalPosition[0],
			self.particleGoalStartPosition[0][1] - goalPosition[1],
			self.particleGoalStartPosition[0][2] - goalPosition[2],
			)
		
		### TODO Set particle attributes
		particleAttributes = (
			self.particle + Text.ConvertSymbols(self.selectedObjects) + ".translateX",
			self.particle + Text.ConvertSymbols(self.selectedObjects) + ".translateY",
			self.particle + Text.ConvertSymbols(self.selectedObjects) + ".translateZ",
			)

		cmds.setAttr(particleAttributes[0], self.particleGoalStartPosition[1][0] - goalOffset[0])
		cmds.setAttr(particleAttributes[1], self.particleGoalStartPosition[1][1] - goalOffset[1])
		cmds.setAttr(particleAttributes[2], self.particleGoalStartPosition[1][2] - goalOffset[2])
		
		### Reposition aim up locator and reconstrain aim
		selected = cmds.ls(selection = True)
		cmds.delete(self.particleLocAim[1] + "_aimConstraint1")
		cmds.aimConstraint(self.particleLocGoalTarget[1], self.particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "none")
		cmds.delete(self.particleLocAim[1] + "_aimConstraint1")
		cmds.parent(self.particleLocAim[3], self.particleLocAim[1])
		cmds.setAttr(self.particleLocAim[3] + ".tx", 0)
		cmds.setAttr(self.particleLocAim[3] + ".ty", 100)
		cmds.setAttr(self.particleLocAim[3] + ".tz", 0)
		cmds.parent(self.particleLocAim[3], self.particleLocAim[0])
		cmds.aimConstraint(self.particleLocGoalTarget[1], self.particleLocAim[1], weight = 1, aimVector = (1, 0, 0), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = self.particleLocAim[3])
		cmds.select(selected, replace = True)
		
		### Reconstrain aim locator to hidden aim
		cmds.setAttr(self.particleLocAim[2] + ".rotateX", 0)
		cmds.setAttr(self.particleLocAim[2] + ".rotateY", 0)
		cmds.setAttr(self.particleLocAim[2] + ".rotateZ", 0)
		cmds.orientConstraint(self.particleLocAim[1], self.particleLocAim[2], maintainOffset = True)


	### SELECT
	def _Select(self, name="", *args):
		if (name != ""):
			if (cmds.objExists(name)):
				cmds.select(name, replace = True)
			else:
				cmds.warning("\"{0}\" object doesn't exists".format(name))
		else:
			cmds.warning("Object name is not specified")
	def _SelectSelectedObjects(self, *args): self._Select(self.selectedObjects)
	def _SelectNucleus(self, *args): self._Select(self.nucleus)
	

	### PARTICLE VALUES
	def _ParticleOffsetSetValues(self, *args): # TODO rework with new aim offset logic
		# self._SetSliderValue(self.slidersParticleOffset[0].Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateX")
		# self._SetSliderValue(self.slidersParticleOffset[1].Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateY")
		# self._SetSliderValue(self.slidersParticleOffset[2].Get(), OverlappySettings.nameLocGoalTarget[0], "_parentConstraint1.target[0].targetOffsetTranslateZ")
		cmds.warning("TODO: _ParticleOffsetSetValues")
	def _ParticleDynamicPropertiesUpdate(self, *args):
		cmds.setAttr(self.particle + "Shape.radius", self.sliderParticleRadius.Get())
		cmds.setAttr(self.particle + "Shape.conserve", self.sliderParticleConserve.Get())
		cmds.setAttr(self.particle + "Shape.drag", self.sliderParticleDrag.Get())
		cmds.setAttr(self.particle + "Shape.damp", self.sliderParticleDamp.Get())
		cmds.setAttr(self.particle + "Shape.goalSmoothness", self.sliderParticleGoalSmooth.Get())
		cmds.setAttr(self.particle + "Shape.goalWeight[0]", self.sliderParticleGoalWeight.Get())
		cmds.setAttr(self.nucleus + ".timeScale", self.sliderNucleusTimeScale.Get())
	

	### RESET VALUES
	def _ResetAllValues(self, *args):
		self._ResetOptions()
		# self._ResetAllChainValues()
		self._ResetAllParticleValues()
	# def _ResetAllChainValues(self, *args): # TODO Reset Chain Values
	# 	cmds.warning("TODO: Reset Chain Values")
	# 	pass
	def _ResetAllParticleValues(self, *args):
		self._ResetParticleDynamicProperties()
		self._ResetParticleOffsets()
	def _ResetOptions(self, *args):
		self.menuCheckboxHierarchy.Reset()
		self.menuCheckboxLayer.Reset()
		self.menuCheckboxLoop.Reset()
		self.menuCheckboxClean.Reset()
		self.menuCheckboxCollisions.Reset()
	def _ResetParticleOffsets(self, *args): # TODO
		# self.checkboxesParticleMirror[0].Reset()
		# self.checkboxesParticleMirror[1].Reset()
		# self.checkboxesParticleMirror[2].Reset()
		# self.slidersParticleOffset[0].Reset()
		# self.slidersParticleOffset[1].Reset()
		# self.slidersParticleOffset[2].Reset()
		cmds.warning("TODO: _ResetParticleOffsets")
		self._ParticleOffsetSetValues()
	def _ResetParticleDynamicProperties(self, *args):
		self.sliderParticleRadius.Reset()
		self.sliderParticleConserve.Reset()
		self.sliderParticleDrag.Reset()
		self.sliderParticleDamp.Reset()
		self.sliderParticleGoalSmooth.Reset()
		self.sliderParticleGoalWeight.Reset()
		self.sliderNucleusTimeScale.Reset() # TODO move out from particle specific logic
		self._ParticleDynamicPropertiesUpdate()
	

	### BAKE
	def _BakeParticleLogic(self, parent, zeroOffsets=False, translation=True, deleteSetupLock=False, *args):
		### Filter attributes
		if (translation):
			attributesType = Enums.Attributes.translateLong
		else:
			attributesType = Enums.Attributes.rotateLong
		attrs = ["", "", ""]
		
		selected = self.selectedObjects
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
			self._ParticleSetupDelete()
			return
		
		### Keyframe target attributes
		cmds.setKeyframe(selected, attribute = attributesFiltered)

		### TODO Zero offsets
		# if (zeroOffsets):
		# 	value1 = self.slidersParticleOffset[0].Get()
		# 	value2 = self.slidersParticleOffset[1].Get()
		# 	value3 = self.slidersParticleOffset[2].Get()
		# 	self.slidersParticleOffset[0].Reset()
		# 	self.slidersParticleOffset[1].Reset()
		# 	self.slidersParticleOffset[2].Reset()
		
		### Set time range
		self.time.Scan()
		startTime = self.time.values[2]
		if (self.menuCheckboxLoop.Get()):
			startTime = self.time.values[2] - self.time.values[3] * OverlappySettings.loopBakeOffset
			self.time.SetMin(startTime)
			self.time.SetCurrent(startTime)
		cmds.setAttr(self.nucleus + ".startFrame", startTime) # TODO bug when select ovlp objects
		
		### Start logic
		name = "_rebake_" + Text.ConvertSymbols(selected)
		clone = cmds.duplicate(selected, name = name, parentOnly = True, transformsOnly = True, smartTransform = True, returnRootsOnly = True)
		
		for attribute in Enums.Attributes.translateLong:
			cmds.setAttr(clone[0] + "." + attribute, lock = False)
		for attribute in Enums.Attributes.rotateLong:
			cmds.setAttr(clone[0] + "." + attribute, lock = False)
		
		cmds.parentConstraint(parent, clone, maintainOffset = True) # skipTranslate
		cmds.select(clone, replace = True)
		
		### Bake
		Baker.BakeSelected(classic = True, preserveOutsideKeys = True, euler = self.generalInstance.menuCheckboxEulerFilter.Get())
		Constraints.DeleteConstraints(clone)
		
		### Copy keys, create layers and paste keys
		cmds.copyKey(clone, time = (self.time.values[2], self.time.values[3]), attribute = attributesFiltered)
		
		if (self.menuCheckboxLayer.Get()):
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
		
		### Set time range
		if (self.menuCheckboxLoop.Get()):
			startTime = self.time.values[2]
			cmds.setAttr(self.nucleus + ".startFrame", startTime)
			self.time.Reset()
			Animation.SetInfinityCycle(selected)
		else:
			Animation.SetInfinityConstant(selected)
		
		### Delete setup
		if (self.menuCheckboxClean.Get()):
			if (not deleteSetupLock):
				self._ParticleSetupDelete()
		
		### TODO Restore offsets sliders
		# if (zeroOffsets):
		# 	self.slidersParticleOffset[0].Set(value1)
		# 	self.slidersParticleOffset[1].Set(value2)
		# 	self.slidersParticleOffset[2].Set(value3)
		# 	self._ParticleOffsetsUpdate(True)
	def _BakeParticleVariants(self, variant, *args): # TODO
		selected = Selector.MultipleObjects()
		if (selected == None):
			return
		
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

		if (self.menuCheckboxHierarchy.Get()):
			selected = Selector.SelectHierarchyTransforms()
		
		def RunBakeLogicVariant():
			if (variant == 1):
				self._BakeParticleLogic(self.particleLocGoalTarget[1], zeroOffsets = True)
			elif (variant == 2):
				self._BakeParticleLogic(self.particleLocGoalTarget[1])
			elif (variant == 3):
				self._BakeParticleLogic(self.particleLocAim[2], translation = False)
			elif (variant == 4):
				self._BakeParticleLogic(self.particleLocGoalTarget[1], zeroOffsets = True, deleteSetupLock = True)
				self._BakeParticleLogic(self.particleLocAim[2], translation = False)
			elif (variant == 5):
				self._BakeParticleLogic(self.particleLocAim[2], translation = False, deleteSetupLock = True)
				self._BakeParticleLogic(self.particleLocGoalTarget[1], zeroOffsets = True)
		
		for i in range(len(selected)):
			cmds.select(selected[i], replace = True)
			self._ParticleSetupPoint()
			RunBakeLogicVariant()
		
		cmds.select(selected, replace = True)


	### LAYERS
	def _LayerCreate(self, name, *args): # TODO additional naming for translation and rotation
		### Create main layer
		if (not cmds.objExists(OverlappySettings.nameLayers[0])):
			self.layers[0] = Layers.Create(layerName = OverlappySettings.nameLayers[0])
		
		### Create layers on selected
		layerName = Text.ConvertSymbols(name) + "_1"
		return Layers.Create(layerName = layerName, parent = self.layers[0])
	def _LayerMoveToSafeOrTemp(self, safeLayer=True, *args): # TODO rework
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

