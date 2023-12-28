# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial

from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.utils import Install
from GETOOLS_SOURCE.utils import Layers
from GETOOLS_SOURCE.utils import MayaSettings
from GETOOLS_SOURCE.utils import MotionTrail
from GETOOLS_SOURCE.utils import Scene
from GETOOLS_SOURCE.utils import Selector

from GETOOLS_SOURCE.modules import CenterOfMass as com
from GETOOLS_SOURCE.modules import Overlappy as ovlp
from GETOOLS_SOURCE.modules import Rigging as rig
from GETOOLS_SOURCE.modules import Settings
from GETOOLS_SOURCE.modules import Tools as tls

from GETOOLS_SOURCE.values import Icons

class GeneralWindow:
	version = "v1.0.0"
	name = "GETools"
	title = name + " " + version

	def __init__(self):
		self.directory = ""
		self.frameTools = None
		self.frameRigging = None
		self.frameOverlappy = None
		self.frameCenterOfMass = None
		self.frameExperimental = None
	def CreateUI(self):
		if cmds.window(Settings.windowName, exists = True):
			cmds.deleteUI(Settings.windowName)
		cmds.window(Settings.windowName, title = GeneralWindow.title, maximizeButton = False, sizeable = True, widthHeight = (Settings.windowWidth, Settings.windowHeight))
		
		# layoutRoot = cmds.columnLayout(adjustableColumn = True, width = Settings.windowWidth)
		layoutRoot = cmds.menuBarLayout(width = Settings.windowWidth)
		self.LayoutMenuBar(layoutRoot)
		
		layoutScroll = cmds.scrollLayout(parent = layoutRoot, width = Settings.windowWidth)
		self.LayoutTools(layoutScroll)
		self.LayoutRigging(layoutScroll)
		self.LayoutOverlappy(layoutScroll)
		self.LayoutCenterOfMass(layoutScroll)
		self.LayoutExperimental(layoutScroll)

	# UI LAYOUTS
	def LayoutMenuBar(self, parentLayout):
		cmds.columnLayout("layoutMenuBar", parent = parentLayout, adjustableColumn = True, width = Settings.windowWidthScroll)
		cmds.menuBarLayout()

		cmds.menu(label = "File")
		cmds.menuItem(label = "Reload Scene (force)", command = Scene.Reload)
		cmds.menuItem(label = "Exit Maya (force)", command = Scene.ExitMaya)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Restart GETools", command = partial(self.RUN_DOCKED, "", True))
		cmds.menuItem(label = "Close GETools", command = self.DockDelete)
		
		# cmds.menu(label = "Edit", tearOff = True)
		# cmds.menuItem(label = "Save Settings")
		# cmds.menuItem(label = "Load Settings")
		# cmds.menuItem(label = "Reset Settings")

		cmds.menu(label = "Display", tearOff = True)
		cmds.menuItem(label = "Collapse All", command = partial(self.FramesCollapse, True))
		cmds.menuItem(label = "Expand All", command = partial(self.FramesCollapse, False))
		cmds.menuItem(dividerLabel = "Docking", divider = True)
		cmds.menuItem(label = "Dock Left", command = partial(self.DockToSide, Settings.dockAllowedAreas[0]))
		cmds.menuItem(label = "Dock Right", command = partial(self.DockToSide, Settings.dockAllowedAreas[1]))
		cmds.menuItem(label = "Undock", command = self.DockOff)

		def ColorsPalette(*args):
			colorCalibration = Colors.ColorsPalette()
			colorCalibration.CreateUI()
		def PrintChannelBoxAttributes(*args):
			print(Selector.GetChannelBoxAttributes())
		cmds.menu(label = "Utils", tearOff = True)
		cmds.menuItem(label = "Select Transform Hiererchy", command = Selector.SelectTransformHierarchy)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Print selected objects to console", command = Selector.PrintSelected)
		cmds.menuItem(label = "Print channel box selected attributes", command = PrintChannelBoxAttributes)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Open Colors Palette", command = ColorsPalette)
		
		self.LayoutMenuInstall()

		cmds.menu(label = "Help", tearOff = True) # , helpMenu = True
		def LinkVersionHistory(self): cmds.showHelp("https://github.com/GenEugene/GETools/blob/master/changelog.txt", absolute = True)
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/GETools", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://gumroad.com/l/iCNa", absolute = True)
		def LinkGithubWiki(self): cmds.showHelp("https://github.com/GenEugene/GETools/wiki", absolute = True)
		def LinkYoutubeTutorial(self): cmds.showHelp("", absolute = True) # TODO add new youtube link with tutorial
		def LinkLinkedin(self): cmds.showHelp("https://www.linkedin.com/in/geneugene", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True)
		def LinkDiscord(self): cmds.showHelp("https://discord.gg/heMxJhTqCz", absolute = True)
		def LinkShareIdeas(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/ideas", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/report-a-problem", absolute = True)
		
		cmds.menuItem(label = "About GETools", enable = False, image = self.directory + Icons.get) # TODO add window with information
		cmds.menuItem(label = "Version History", command = LinkVersionHistory)
		cmds.menuItem(dividerLabel = "Links", divider = True)
		cmds.menuItem(label = "GitHub", command = LinkGithub)
		cmds.menuItem(label = "Gumroad", command = LinkGumroad)
		cmds.menuItem(dividerLabel = "HOW TO USE", divider = True)
		cmds.menuItem(label = "Documentation", command = LinkGithubWiki, image = Icons.help)
		cmds.menuItem(label = "Tutorial Video", enable = False, command = LinkYoutubeTutorial, image = Icons.playblast)
		cmds.menuItem(dividerLabel = "Contacts", divider = True)
		cmds.menuItem(label = "Linkedin", command = LinkLinkedin)
		cmds.menuItem(label = "YouTube", command = LinkYoutube)
		cmds.menuItem(label = "Discord", command = LinkDiscord)
		cmds.menuItem(dividerLabel = "Support", divider = True)
		cmds.menuItem(label = "Share your Ideas", command = LinkShareIdeas, image = Icons.light)
		cmds.menuItem(label = "Report a Problem", command = LinkReport, image = Icons.warning)

		# DEV ZONE
		def LayerCreate(*args):
			Layers.Create("testLayer")
		def LayerCreateForSelected(*args):
			selected = Selector.MultipleObjects()
			if (selected == None):
				return
			Layers.CreateForSelected(selected)
		def LayerDelete(*args):
			Layers.Delete("testLayer")
		def LayerGetSelected(*args):
			Layers.GetSelected()
		def LayerMove(*args):
			selected = Layers.GetSelected()
			if (selected == None or len(selected) < 2):
				cmds.warning("Need to select at least 2 layers")
				return
			Layers.MoveChildrenToParent(selected[:-1], selected[-1]) # FIXME main problem is layers have no selection order, they just listed from top to bottom

		# cmds.menu(label = "---", enable = False)
		# cmds.menu(label = "DEV", tearOff = True)
		# cmds.menuItem(dividerLabel = "Layers", divider = True)
		# cmds.menuItem(label = "Layer Create", command = LayerCreate)
		# cmds.menuItem(label = "Layer Create For Selected", command = LayerCreateForSelected)
		# cmds.menuItem(label = "Layer Delete", command = LayerDelete)
		# cmds.menuItem(label = "Layer Get Selected", command = LayerGetSelected)
		# cmds.menuItem(label = "Layer Move", command = LayerMove)
		pass
	def LayoutMenuInstall(self):
		cmds.menu(label = "To Shelf", tearOff = True)
		###
		cmds.menuItem(subMenu = True, label = "General")
		cmds.menuItem(dividerLabel = "File", divider = True)
		cmds.menuItem(label = "Reload Scene (force)", command = partial(Install.ToShelf_ReloadScene, self.directory))
		cmds.menuItem(label = "Exit Maya (force)", command = partial(Install.ToShelf_ExitMaya, self.directory))
		cmds.menuItem(dividerLabel = "Utils", divider = True)
		cmds.menuItem(label = "Select Transform Hiererchy", command = partial(Install.ToShelf_SelectHierarchy, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(dividerLabel = "TOOLS - Locators", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Size")
		cmds.menuItem(label = "50%", command = partial(Install.ToShelf_LocatorsSizeScale50, self.directory))
		cmds.menuItem(label = "90%", command = partial(Install.ToShelf_LocatorsSizeScale90, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "110%", command = partial(Install.ToShelf_LocatorsSizeScale110, self.directory))
		cmds.menuItem(label = "200%", command = partial(Install.ToShelf_LocatorsSizeScale200, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Create")
		cmds.menuItem(label = "Locator", command = partial(Install.ToShelf_LocatorCreate, self.directory))
		cmds.menuItem(label = "Match", command = partial(Install.ToShelf_LocatorsMatch, self.directory))
		cmds.menuItem(label = "Parent", command = partial(Install.ToShelf_LocatorsParent, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Pin")
		cmds.menuItem(label = "Pin", command = partial(Install.ToShelf_LocatorsPin, self.directory))
		cmds.menuItem(label = "Without reverse constraint", command = partial(Install.ToShelf_LocatorsPinWithoutReverse, self.directory))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_LocatorsPinPos, self.directory))
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_LocatorsPinRot, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Relative")
		cmds.menuItem(label = "Relative", command = partial(Install.ToShelf_LocatorsRelative, self.directory))
		cmds.menuItem(label = "Skip last object reverse constraint", command = partial(Install.ToShelf_LocatorsRelativeSkipLast, self.directory))
		cmds.menuItem(label = "Without reverse constraint", command = partial(Install.ToShelf_LocatorsRelativeWithoutReverse, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Aim")
		minus = "-"
		plus = "+"
		axisX = "X"
		axisY = "Y"
		axisZ = "Z"
		axisXMinus = minus + axisX
		axisYMinus = minus + axisY
		axisZMinus = minus + axisZ
		axisXPlus = plus + axisX
		axisYPlus = plus + axisY
		axisZPlus = plus + axisZ
		cmds.menuItem(dividerLabel = "All", divider = True)
		cmds.menuItem(label = axisXMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXMinus, False, (-1, 0, 0)))
		cmds.menuItem(label = axisXPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXPlus, False, (1, 0, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisYMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYMinus, False, (0, -1, 0)))
		cmds.menuItem(label = axisYPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYPlus, False, (0, 1, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisZMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZMinus, False, (0, 0, -1)))
		cmds.menuItem(label = axisZPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZPlus, False, (0, 0, 1)))
		cmds.menuItem(dividerLabel = "Rotation", divider = True)
		cmds.menuItem(label = axisXMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXMinus, True, (-1, 0, 0)))
		cmds.menuItem(label = axisXPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXPlus, True, (1, 0, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisYMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYMinus, True, (0, -1, 0)))
		cmds.menuItem(label = axisYPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYPlus, True, (0, 1, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisZMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZMinus, True, (0, 0, -1)))
		cmds.menuItem(label = axisZPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZPlus, True, (0, 0, 1)))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(dividerLabel = "TOOLS - Baking", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Bake")
		cmds.menuItem(label = "Classic", command = partial(Install.ToShelf_BakeClassic, self.directory))
		cmds.menuItem(label = "Classic Cut Out", command = partial(Install.ToShelf_BakeClassicCutOut, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Custom", command = partial(Install.ToShelf_BakeCustom, self.directory))
		cmds.menuItem(label = "Custom Cut Out", command = partial(Install.ToShelf_BakeCustomCutOut, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "By Last")
		cmds.menuItem(label = "By Last", command = partial(Install.ToShelf_BakeByLast, self.directory, True, True))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_BakeByLast, self.directory, True, False))
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_BakeByLast, self.directory, False, True))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "World")
		cmds.menuItem(label = "World", command = partial(Install.ToShelf_BakeByWorld, self.directory, True, True))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_BakeByWorld, self.directory, True, False))
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_BakeByWorld, self.directory, False, True))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(dividerLabel = "TOOLS - Animation", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Delete")
		cmds.menuItem(label = "Animation", command = partial(Install.ToShelf_DeleteKeys, self.directory))
		cmds.menuItem(label = "Nonkeyable", command = partial(Install.ToShelf_DeleteNonkeyable, self.directory))
		cmds.menuItem(label = "Static", command = partial(Install.ToShelf_DeleteStatic, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(label = "Euler Filter", command = partial(Install.ToShelf_EulerFilter, self.directory))
		#
		cmds.menuItem(subMenu = True, label = "Infinity")
		cmds.menuItem(label = "Constant", command = partial(Install.ToShelf_SetInfinity, self.directory, 1))
		cmds.menuItem(label = "Linear", command = partial(Install.ToShelf_SetInfinity, self.directory, 2))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Cycle", command = partial(Install.ToShelf_SetInfinity, self.directory, 3))
		cmds.menuItem(label = "Offset", command = partial(Install.ToShelf_SetInfinity, self.directory, 4))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Oscillate", command = partial(Install.ToShelf_SetInfinity, self.directory, 5))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Offset")
		cmds.menuItem(label = "-3", command = partial(Install.ToShelf_AnimOffset, self.directory, -1, 3))
		cmds.menuItem(label = "-2", command = partial(Install.ToShelf_AnimOffset, self.directory, -1, 2))
		cmds.menuItem(label = "-1", command = partial(Install.ToShelf_AnimOffset, self.directory, -1, 1))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "+1", command = partial(Install.ToShelf_AnimOffset, self.directory, 1, 1))
		cmds.menuItem(label = "+2", command = partial(Install.ToShelf_AnimOffset, self.directory, 1, 2))
		cmds.menuItem(label = "+3", command = partial(Install.ToShelf_AnimOffset, self.directory, 1, 3))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(dividerLabel = "TOOLS - Timeline", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Timeline")
		cmds.menuItem(label = "Min Out", command = partial(Install.ToShelf_SetTimelineMinOut, self.directory))
		cmds.menuItem(label = "Min In", command = partial(Install.ToShelf_SetTimelineMinIn, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Max In", command = partial(Install.ToShelf_SetTimelineMaxIn, self.directory))
		cmds.menuItem(label = "Max Out", command = partial(Install.ToShelf_SetTimelineMaxOut, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Expand Out", command = partial(Install.ToShelf_SetTimelineExpandOut, self.directory))
		cmds.menuItem(label = "Expand In", command = partial(Install.ToShelf_SetTimelineExpandIn, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Selected Range", command = partial(Install.ToShelf_SetTimelineSet, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(dividerLabel = "RIGGING - Constraints", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Constraints")
		cmds.menuItem(label = "Parent", command = partial(Install.ToShelf_Constraint, self.directory, False, True, False, False, False))
		cmds.menuItem(label = "Point", command = partial(Install.ToShelf_Constraint, self.directory, False, False, True, False, False))
		cmds.menuItem(label = "Orient", command = partial(Install.ToShelf_Constraint, self.directory, False, False, False, True, False))
		cmds.menuItem(label = "Scale", command = partial(Install.ToShelf_Constraint, self.directory, False, False, False, False, True))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Parent with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, True, False, False, False))
		cmds.menuItem(label = "Point with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, False, True, False, False))
		cmds.menuItem(label = "Orient with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, False, False, True, False))
		cmds.menuItem(label = "Scale with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, False, False, False, True))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Connections")
		cmds.menuItem(label = "Disconnect", command = partial(Install.ToShelf_DisconnectTargets, self.directory))
		cmds.menuItem(label = "Delete Constraints", command = partial(Install.ToShelf_DeleteConstraints, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(dividerLabel = "RIGGING - Utils", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Rotate Order")
		cmds.menuItem(label = "Show", command = partial(Install.ToShelf_RotateOrder, self.directory, True))
		cmds.menuItem(label = "Hide", command = partial(Install.ToShelf_RotateOrder, self.directory, False))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Segment Scale Compensate")
		cmds.menuItem(label = "On", command = partial(Install.ToShelf_SegmentScaleCompensate, self.directory, True))
		cmds.menuItem(label = "Off", command = partial(Install.ToShelf_SegmentScaleCompensate, self.directory, False))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Joint Draw Style")
		cmds.menuItem(label = "Bone", command = partial(Install.ToShelf_JointDrawStyle, self.directory, 0))
		cmds.menuItem(label = "Hidden", command = partial(Install.ToShelf_JointDrawStyle, self.directory, 2))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(label = "Copy Skin Weights From Last Selected", command = partial(Install.ToShelf_CopySkin, self.directory))
		#
		cmds.menuItem(dividerLabel = "EXPERIMENTAL", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Motion Trail")
		cmds.menuItem(label = "Create", command = partial(Install.ToShelf_MotionTrailCreate, self.directory))
		cmds.menuItem(label = "Select", command = partial(Install.ToShelf_MotionTrailSelect, self.directory))
		cmds.menuItem(label = "Delete", command = partial(Install.ToShelf_MotionTrailDelete, self.directory))
		cmds.setParent('..', menu = True)
		#

	def LayoutTools(self, parentLayout):
		self.frameTools = cmds.frameLayout("layoutTools", parent = parentLayout, label = "1. " + tls.Tools.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		tls.Tools().UICreate(self.frameTools)
	def LayoutRigging(self, parentLayout):
		self.frameRigging = cmds.frameLayout("layoutRigging", parent = parentLayout, label = "2. " + rig.Rigging.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		rig.Rigging().UICreate(self.frameRigging)
	def LayoutOverlappy(self, parentLayout):
		self.frameOverlappy = cmds.frameLayout("layoutOverlappy", parent = parentLayout, label = "3. " + ovlp.Overlappy.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		ovlp.Overlappy().UICreate(self.frameOverlappy)
	def LayoutCenterOfMass(self, parentLayout):
		self.frameCenterOfMass = cmds.frameLayout("layoutCenterOfMass", parent = parentLayout, label = "4. " + com.CenterOfMass.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		com.CenterOfMass().UICreate(self.frameCenterOfMass)
	def LayoutExperimental(self, parentLayout):
		self.frameExperimental = cmds.frameLayout("layoutExperimental", parent = parentLayout, label = "5. " + "EXPERIMENTAL", collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		cmds.popupMenu()
		cmds.menuItem(label = "Right-Click test")
		
		countOffsets = 3
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)

		cmds.button(label = "Trails Create", command = MotionTrail.Create, backgroundColor = Colors.orange10)
		cmds.button(label = "Trails Select", command = MotionTrail.Select, backgroundColor = Colors.orange50)
		cmds.button(label = "Trails Delete", command = MotionTrail.Delete, backgroundColor = Colors.orange100)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Select", command = MotionTrail.Select)
		# cmds.menuItem(label = "Delete", command = MotionTrail.Delete)
		pass

	# WINDOW
	def WindowCheck(self, *args):
		return cmds.window(Settings.windowName, exists = True)
	def WindowShow(self, *args):
		if self.WindowCheck():
			cmds.showWindow(Settings.windowName)
			print("Window showed")
		else:
			print("No Window")
	def WindowHide(self, *args):
		if self.WindowCheck():
			cmds.window(Settings.windowName, edit = True, visible = False)
			print("Window hidden")
		else:
			print("No Window")
	def WindowDelete(self, *args):
		if self.WindowCheck():
			cmds.deleteUI(Settings.windowName)
			print("Window deleted")
		else:
			print("No Window")
	def FramesCollapse(self, value, *args): # TODO collapse function for sub frames
		if (self.frameTools != None):
			cmds.frameLayout(self.frameTools, edit = True, collapse = value)
		if (self.frameRigging != None):
			cmds.frameLayout(self.frameRigging, edit = True, collapse = value)
		if (self.frameOverlappy != None):
			cmds.frameLayout(self.frameOverlappy, edit = True, collapse = value)
		if (self.frameCenterOfMass != None):
			cmds.frameLayout(self.frameCenterOfMass, edit = True, collapse = value)
		if (self.frameExperimental != None):
			cmds.frameLayout(self.frameExperimental, edit = True, collapse = value)

	# DOCKING
	def DockCheckVisible(self, *args):
		return cmds.dockControl(Settings.dockName, query = True, visible = True)
	def DockCheck(self, *args):
		return cmds.dockControl(Settings.dockName, query = True, exists = True)
	def DockDelete(self, *args):
		if self.DockCheck():
			cmds.deleteUI(Settings.dockName, control = True)
			# print("Dock Control deleted")
		# else:
		# 	print("No Dock")
		pass
	def DockOff(self, *args):
		if self.DockCheck():
			cmds.dockControl(Settings.dockName, edit = True, floating = True, height = Settings.windowHeight)
			print("{0} undocked".format(GeneralWindow.title))
		else:
			cmds.warning("Dock Controls wasn't found")
	def DockToSide(self, areaSide, *args):
		if self.DockCheck():
			cmds.dockControl(Settings.dockName, edit = True, floating = False, area = areaSide)
		else:
			cmds.dockControl(Settings.dockName, label = GeneralWindow.title, content = Settings.windowName, area = areaSide, allowedArea = Settings.dockAllowedAreas) # , backgroundColor = Colors.lightBlue10
		print("{0} docked to {1}".format(GeneralWindow.title, areaSide))

	# EXECUTION
	def WindowCreate(self, *args):
		self.CreateUI()
		self.FramesCollapse(True)
	def RUN_DOCKED(self, path = "", forced = False, *args):
		self.directory = path

		if (forced == False and self.DockCheck()): # for script toggling. Comment these 3 lines if you need to deactivate toggling
			if (self.DockCheckVisible()):
				self.DockDelete()
				print("{0} closed".format(GeneralWindow.title))
				return

		self.DockDelete()
		self.WindowCreate()
		self.DockToSide(Settings.dockStartArea)

		MayaSettings.HelpPopupActivate()
		MayaSettings.CachedPlaybackDeactivate()

