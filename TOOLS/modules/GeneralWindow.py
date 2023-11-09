# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from functools import partial
from utils import Colors
from utils import Scene
from utils import MotionTrail
from modules import Tools as tls
from modules import Overlappy as ovlp
from modules import CenterOfMass as com

class GeneralWindowSettings:
	windowName = "windowGETools"
	dockName = "dockGETools"
	dockAllowedAreas = ["left", "right"]
	dockStartArea = dockAllowedAreas[0]
	
	windowHeight = 100
	windowWidth = 320
	windowWidthScrollSpace = 16
	# lineHeight = 20
	margin = 5

	windowWidthScroll = windowWidth - windowWidthScrollSpace
	windowWidthMargin = windowWidthScroll - margin * 2

class GeneralWindow:
	version = "v0.0.3"
	title = "GETools" + " " + version

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
		self.LayoutMenu(layoutRoot)
		
		layoutScroll = cmds.scrollLayout(parent = layoutRoot, width = GeneralWindowSettings.windowWidth)
		self.LayoutTools(layoutScroll)
		self.LayoutOverlappy(layoutScroll)
		self.LayoutCenterOfMass(layoutScroll)
		self.LayoutExperimental(layoutScroll)

		self.FrameCollapse(True)

	# UI LAYOUTS
	def LayoutMenu(self, parentLayout):
		layoutMenu = cmds.columnLayout(parent = parentLayout, adjustableColumn = True, width = GeneralWindowSettings.windowWidthScroll)
		cmds.menuBarLayout(parent = layoutMenu)
		
		cmds.menu(label = "File")
		def SceneReload(self): Scene.Reload()
		def ExitMaya(self): Scene.ExitMaya()
		cmds.menuItem(label = "Reload Scene (force)", command = SceneReload)
		cmds.menuItem(label = "Exit Maya (force)", command = ExitMaya)
		

		# cmds.menu(label = "Edit")
		# cmds.menuItem(label = "Save Settings")
		# cmds.menuItem(label = "Load Settings")
		# cmds.menuItem(label = "Reset Settings")


		cmds.menu(label = "Display")
		cmds.menuItem(label = "Collapse All", command = partial(self.FrameCollapse, True))
		cmds.menuItem(label = "Expand All", command = partial(self.FrameCollapse, False))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Dock Left", command = partial(self.DockSide, GeneralWindowSettings.dockAllowedAreas[0]))
		cmds.menuItem(label = "Dock Right", command = partial(self.DockSide, GeneralWindowSettings.dockAllowedAreas[1]))
		cmds.menuItem(label = "Undock", command = self.DockOff)


		# cmds.menu(label = "DEV")
		# cmds.menuItem(label = "Dev Tools toggle", checkBox = False) # , command = self.LayoutDevToolsToggle
		# cmds.menuItem(label = "Reload Script") # , command = self.Restart


		cmds.menu(label = "Help")
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/GETools", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://app.gumroad.com/geneugene", absolute = True) # TODO add new gumroad link
		def LinkYoutubeTutorial(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True) # TODO add new youtube link with tutorial
		def LinkLinkedin(self): cmds.showHelp("https://www.linkedin.com/in/geneugene", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True)
		def LinkDiscord(self): cmds.showHelp("https://discord.gg/heMxJhTqCz", absolute = True)
		def LinkShareIdeas(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/ideas", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/report-a-problem", absolute = True)
		cmds.menuItem(label = "About GETools", enable = False) # TODO add window with information
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
	def LayoutTools(self, parentLayout):
		self.frameTools = cmds.frameLayout(parent = parentLayout, label = tls.Tools.title, collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		tls.Tools().UILayout(self.frameTools)
	def LayoutOverlappy(self, parentLayout):
		self.frameOverlappy = cmds.frameLayout(parent = parentLayout, label = ovlp.Overlappy.title, collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		ovlp.Overlappy().UILayout(self.frameOverlappy)
	def LayoutCenterOfMass(self, parentLayout):
		self.frameCenterOfMass = cmds.frameLayout(parent = parentLayout, label = com.CenterOfMass.title, collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		com.CenterOfMass().UILayout(self.frameCenterOfMass)
	def LayoutExperimental(self, parentLayout):
		self.frameExperimental = cmds.frameLayout(parent = parentLayout, label = "EXPERIMENTAL", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = GeneralWindowSettings.margin, marginHeight = GeneralWindowSettings.margin)
		countOffsets = 1
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = GeneralWindowSettings.windowWidthMargin / countOffsets)

		cmds.button(label = "Motion Trail", command = MotionTrail.Create, backgroundColor = Colors.orange10)
		cmds.popupMenu()
		cmds.menuItem(label = "Select", command = MotionTrail.Select)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Delete", command = MotionTrail.Delete)

	# DOCKING
	def DockCleanup(self):
		dockExists = cmds.dockControl(GeneralWindowSettings.dockName, query = True, exists = True)
		if dockExists:
			cmds.deleteUI(GeneralWindowSettings.dockName, control = True)
			return True
		else:
			return False
	def DockOff(self, *args): # TODO undick window without creation recreation
		dockExists = cmds.dockControl(GeneralWindowSettings.dockName, query = True, exists = True)
		if dockExists:
			cmds.deleteUI(GeneralWindowSettings.dockName, control = True)
			self.CreateUI()
			cmds.showWindow(GeneralWindowSettings.windowName)
			print("{0} undocked".format(GeneralWindow.title))
		else:
			cmds.warning("Window is not docked")
	def DockSide(self, areaSide, *args):
		dockExists = cmds.dockControl(GeneralWindowSettings.dockName, query = True, exists = True)
		if dockExists:
			cmds.dockControl(GeneralWindowSettings.dockName, edit = True, floating = False, area = areaSide)
		else:
			cmds.dockControl(GeneralWindowSettings.dockName, label = GeneralWindow.title, area = areaSide, content = GeneralWindowSettings.windowName, allowedArea = GeneralWindowSettings.dockAllowedAreas)
		print("{0} docked {1}".format(GeneralWindow.title, areaSide))
	
	# FRAME COLLAPSE
	def FrameCollapse(self, value, *args):
		cmds.frameLayout(self.frameTools, edit = True, collapse = value)
		cmds.frameLayout(self.frameOverlappy, edit = True, collapse = value)
		cmds.frameLayout(self.frameCenterOfMass, edit = True, collapse = value)
		cmds.frameLayout(self.frameExperimental, edit = True, collapse = value)
		# TODO collapse function for sub frames

	# EXECUTION
	def RUN(self, *args):
		if (self.DockCleanup()):
			print("GETools window closed")
			return
		self.CreateUI()
		self.DockSide(GeneralWindowSettings.dockStartArea)

