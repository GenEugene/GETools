# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial

from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.utils import Scene
from GETOOLS_SOURCE.utils import Layers
from GETOOLS_SOURCE.utils import Selector
from GETOOLS_SOURCE.utils import MotionTrail
from GETOOLS_SOURCE.utils import MayaSettings
from GETOOLS_SOURCE.modules import Tools as tls
from GETOOLS_SOURCE.modules import Overlappy as ovlp
from GETOOLS_SOURCE.modules import CenterOfMass as com

class GeneralWindowSettings:
	windowName = "windowGETools"
	dockName = "dockGETools"
	dockAllowedAreas = ["left", "right"]
	dockStartArea = dockAllowedAreas[0] # used for start docking state, 0 - left, 1 - right
	
	windowHeight = 500 # used for vertical window size when undocked
	windowWidth = 320
	windowWidthScrollSpace = 16
	lineHeight = 30
	margin = 4

	sliderWidth = (60, 60, 10)
	sliderWidthMarker = 14

	windowWidthScroll = windowWidth - windowWidthScrollSpace
	windowWidthMargin = windowWidthScroll - margin * 2

class GeneralWindow:
	version = "v0.0.9"
	name = "GETools"
	title = name + " " + version

	def __init__(self):
		self.frameTools = None
		self.frameOverlappy = None
		self.frameCenterOfMass = None
		self.frameExperimental = None
	def CreateUI(self):
		if cmds.window(GeneralWindowSettings.windowName, exists = True):
			cmds.deleteUI(GeneralWindowSettings.windowName)
		cmds.window(GeneralWindowSettings.windowName, title = GeneralWindow.title, maximizeButton = False, sizeable = True, widthHeight = (GeneralWindowSettings.windowWidth, GeneralWindowSettings.windowHeight))
		
		# layoutRoot = cmds.columnLayout(adjustableColumn = True, width = GeneralWindowSettings.windowWidth)
		layoutRoot = cmds.menuBarLayout(width = GeneralWindowSettings.windowWidth)
		self.LayoutMenuBar(layoutRoot)
		
		layoutScroll = cmds.scrollLayout(parent = layoutRoot, width = GeneralWindowSettings.windowWidth)
		self.LayoutTools(layoutScroll)
		self.LayoutOverlappy(layoutScroll)
		self.LayoutCenterOfMass(layoutScroll)
		self.LayoutExperimental(layoutScroll)

	# UI LAYOUTS
	def LayoutMenuBar(self, parentLayout):
		cmds.columnLayout("layoutMenuBar", parent = parentLayout, adjustableColumn = True, width = GeneralWindowSettings.windowWidthScroll)
		cmds.menuBarLayout()

		cmds.menu(label = "File", tearOff = True)
		cmds.menuItem(label = "Reload Scene (force)", command = Scene.Reload)
		cmds.menuItem(label = "Exit Maya (force)", command = Scene.ExitMaya)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Restart GETools", command = self.RUN_DOCKED)
		cmds.menuItem(label = "Close GETools", command = self.DockDelete)
		
		# cmds.menu(label = "Edit", tearOff = True)
		# cmds.menuItem(label = "Save Settings")
		# cmds.menuItem(label = "Load Settings")
		# cmds.menuItem(label = "Reset Settings")

		cmds.menu(label = "Display", tearOff = True)
		cmds.menuItem(label = "Collapse All", command = partial(self.FramesCollapse, True))
		cmds.menuItem(label = "Expand All", command = partial(self.FramesCollapse, False))
		cmds.menuItem(dividerLabel = "Docking", divider = True)
		cmds.menuItem(label = "Dock Left", command = partial(self.DockToSide, GeneralWindowSettings.dockAllowedAreas[0]))
		cmds.menuItem(label = "Dock Right", command = partial(self.DockToSide, GeneralWindowSettings.dockAllowedAreas[1]))
		cmds.menuItem(label = "Undock", command = self.DockOff)

		cmds.menu(label = "Help", helpMenu = True, tearOff = True)
		def LinkVersionHistory(self): cmds.showHelp("https://github.com/GenEugene/GETools/blob/master/changelog.txt", absolute = True)
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/GETools", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://gumroad.com/l/iCNa", absolute = True)
		def LinkYoutubeTutorial(self): cmds.showHelp("", absolute = True) # TODO add new youtube link with tutorial
		def LinkLinkedin(self): cmds.showHelp("https://www.linkedin.com/in/geneugene", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True)
		def LinkDiscord(self): cmds.showHelp("https://discord.gg/heMxJhTqCz", absolute = True)
		def LinkShareIdeas(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/ideas", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/report-a-problem", absolute = True)
		
		cmds.menuItem(label = "About GETools", enable = False) # TODO add window with information
		cmds.menuItem(label = "Version History", command = LinkVersionHistory)
		cmds.menuItem(dividerLabel = "Links", divider = True)
		cmds.menuItem(label = "GitHub", command = LinkGithub)
		cmds.menuItem(label = "Gumroad", command = LinkGumroad)
		cmds.menuItem(label = "Tutorial Video", enable = False, command = LinkYoutubeTutorial)
		cmds.menuItem(dividerLabel = "Contacts", divider = True)
		cmds.menuItem(label = "Linkedin", command = LinkLinkedin)
		cmds.menuItem(label = "YouTube", command = LinkYoutube)
		cmds.menuItem(label = "Discord", command = LinkDiscord)
		cmds.menuItem(dividerLabel = "Support", divider = True)
		cmds.menuItem(label = "Share your Ideas", command = LinkShareIdeas)
		cmds.menuItem(label = "Report a Problem", command = LinkReport)


		# DEBUG ZONE
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

		cmds.menu(label = "DEV", tearOff = True)
		cmds.menuItem(label = "Layer Create", command = LayerCreate)
		cmds.menuItem(label = "Layer Create For Selected", command = LayerCreateForSelected)
		cmds.menuItem(label = "Layer Delete", command = LayerDelete)
		cmds.menuItem(label = "Layer Get Selected", command = LayerGetSelected)
		cmds.menuItem(label = "Layer Move", command = LayerMove)
	
	def LayoutTools(self, parentLayout):
		self.frameTools = cmds.frameLayout("layoutTools", parent = parentLayout, label = tls.Tools.title, collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		tls.Tools().UICreate(self.frameTools)
	def LayoutOverlappy(self, parentLayout):
		self.frameOverlappy = cmds.frameLayout("layoutOverlappy", parent = parentLayout, label = ovlp.Overlappy.title, collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		ovlp.Overlappy().UICreate(self.frameOverlappy)
	def LayoutCenterOfMass(self, parentLayout):
		self.frameCenterOfMass = cmds.frameLayout("layoutCenterOfMass", parent = parentLayout, label = com.CenterOfMass.title, collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		com.CenterOfMass().UICreate(self.frameCenterOfMass)
	def LayoutExperimental(self, parentLayout):
		self.frameExperimental = cmds.frameLayout("layoutExperimental", parent = parentLayout, label = "EXPERIMENTAL", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		cmds.popupMenu()
		cmds.menuItem(label = "Right-Click test")
		
		countOffsets = 3
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = GeneralWindowSettings.windowWidthMargin / countOffsets, cellHeight = GeneralWindowSettings.lineHeight)

		cmds.button(label = "Trails Create", command = MotionTrail.Create, backgroundColor = Colors.orange10)
		cmds.button(label = "Trails Select", command = MotionTrail.Select, backgroundColor = Colors.orange50)
		cmds.button(label = "Trails Delete", command = MotionTrail.Delete, backgroundColor = Colors.orange100)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Select", command = MotionTrail.Select)
		# cmds.menuItem(label = "Delete", command = MotionTrail.Delete)
		pass

	# WINDOW
	def WindowCheck(self, *args):
		return cmds.window(GeneralWindowSettings.windowName, exists = True)
	def WindowShow(self, *args):
		if self.WindowCheck():
			cmds.showWindow(GeneralWindowSettings.windowName)
			print("Window showed")
		else:
			print("No Window")
	def WindowHide(self, *args):
		if self.WindowCheck():
			cmds.window(GeneralWindowSettings.windowName, edit = True, visible = False)
			print("Window hidden")
		else:
			print("No Window")
	def WindowDelete(self, *args):
		if self.WindowCheck():
			cmds.deleteUI(GeneralWindowSettings.windowName)
			print("Window deleted")
		else:
			print("No Window")
	def FramesCollapse(self, value, *args): # TODO collapse function for sub frames
		if (self.frameTools != None):
			cmds.frameLayout(self.frameTools, edit = True, collapse = value)
		if (self.frameOverlappy != None):
			cmds.frameLayout(self.frameOverlappy, edit = True, collapse = value)
		if (self.frameCenterOfMass != None):
			cmds.frameLayout(self.frameCenterOfMass, edit = True, collapse = value)
		if (self.frameExperimental != None):
			cmds.frameLayout(self.frameExperimental, edit = True, collapse = value)

	# DOCKING
	def DockCheck(self, *args):
		return cmds.dockControl(GeneralWindowSettings.dockName, query = True, exists = True)
	def DockDelete(self, *args):
		if self.DockCheck():
			cmds.deleteUI(GeneralWindowSettings.dockName, control = True)
			print("Dock Control deleted")
		else:
			print("No Dock")
	def DockOff(self, *args):
		if self.DockCheck():
			cmds.dockControl(GeneralWindowSettings.dockName, edit = True, floating = True, height = GeneralWindowSettings.windowHeight)
			print("{0} undocked".format(GeneralWindow.title))
		else:
			cmds.warning("Dock Controls wasn't found")
	def DockToSide(self, areaSide, *args):
		if self.DockCheck():
			cmds.dockControl(GeneralWindowSettings.dockName, edit = True, floating = False, area = areaSide)
		else:
			cmds.dockControl(GeneralWindowSettings.dockName, label = GeneralWindow.title, content = GeneralWindowSettings.windowName, area = areaSide, allowedArea = GeneralWindowSettings.dockAllowedAreas) # , backgroundColor = Colors.lightBlue10
		print("{0} docked {1}".format(GeneralWindow.title, areaSide))

	# EXECUTION
	def WindowCreate(self, *args):
		self.CreateUI()
		self.FramesCollapse(True)
	def RUN_DOCKED(self, *args):
		self.DockDelete()
		self.WindowCreate()
		self.DockToSide(GeneralWindowSettings.dockStartArea)

		MayaSettings.HelpPopupActivate()
		MayaSettings.CachedPlaybackDeactivate()

