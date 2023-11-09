import maya.cmds as cmds
# from math import pow, sqrt
from functools import partial
from utils import Colors
from utils import Scene
from utils import MotionTrail
from modules import CenterOfMass as com
from modules import Tools as tls

class GeneralWindow:
	def __init__(self):
		### WINDOW
		self.version = "v0.0.2"
		self.titleText = "GETools"
		self.windowHeight = 100
		self.windowWidth = 320
		self.windowWidthScrollSpace = 16
		# self.lineHeight = 20
		self.margin = 5
		self.nameWindow = "windowGETools"

		### DOCK
		self.dockName = "dockGETools"
		self.dockAllowedAreas = ["left", "right"]
		self.dockStartArea = self.dockAllowedAreas[0]

		### PRECOMPILED
		self.labelText = self.titleText + " " + self.version
		self.windowWidthScroll = self.windowWidth - self.windowWidthScrollSpace
		self.windowWidthMargin = self.windowWidthScroll - self.margin * 2

		### STORED VALUES
		self.frameTools = None
		self.frameOverlappy = None
		self.frameCenterOfMass = None
		self.frameExperimental = None
	def CreateUI(self):
		# CREATE WINDOW
		if cmds.window(self.nameWindow, exists = True):
			cmds.deleteUI(self.nameWindow)
		cmds.window(self.nameWindow, title = self.labelText, maximizeButton = False, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		# layout0 = cmds.columnLayout(adjustableColumn = True, width = self.windowWidth)
		layout0 = cmds.scrollLayout(width = self.windowWidth) # , horizontalScrollBarThickness = 16, verticalScrollBarThickness = 16

		self.LayoutMenu(layout0)
		###
		self.LayoutTools(layout0)
		self.LayoutOverlappy(layout0)
		self.LayoutCenterOfMass(layout0)
		self.LayoutExperimental(layout0)

		self.FrameCollapse(True)

	# UI LAYOUTS
	def LayoutMenu(self, parentLayout):
		layoutMenu = cmds.columnLayout(parent = parentLayout, adjustableColumn = True, width = self.windowWidthScroll)
		cmds.menuBarLayout(parent = layoutMenu)
		
		cmds.menu(label = "File")
		def SceneReload(self): Scene.Reload()
		def ExitMaya(self): Scene.ExitMaya()
		cmds.menuItem(label = "Reload Scene (force)", command = SceneReload)
		cmds.menuItem(label = "Exit Maya (force)", command = ExitMaya)
		

		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Save Settings")
		cmds.menuItem(label = "Load Settings")
		cmds.menuItem(label = "Reset Settings")


		cmds.menu(label = "Display")
		cmds.menuItem(label = "Collapse All", command = partial(self.FrameCollapse, True))
		cmds.menuItem(label = "Expand All", command = partial(self.FrameCollapse, False))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Dock Left", command = partial(self.DockSide, self.dockAllowedAreas[0]))
		cmds.menuItem(label = "Dock Right", command = partial(self.DockSide, self.dockAllowedAreas[1]))
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
		cmds.menuItem(label = "Report a Problem...", command = LinkReport)
	def LayoutTools(self, parentLayout):
		self.frameTools = cmds.frameLayout(parent = parentLayout, label = "TOOLS", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		tls.Tools().UILayout(self.frameTools)
	def LayoutOverlappy(self, parentLayout): # TODO
		# self.frameTools = cmds.frameLayout(parent = parentLayout, label = "TOOLS", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		# tls.Tools().UILayout(self.frameTools)

		self.frameOverlappy = cmds.frameLayout(parent = parentLayout, label = "OVERLAPPY", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		countOffsets = 3
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidthMargin / countOffsets)
		cmds.button(label = "test", backgroundColor = Colors.orange10)
		cmds.button(label = "test", backgroundColor = Colors.orange50)
		cmds.button(label = "test", backgroundColor = Colors.orange100)
	def LayoutCenterOfMass(self, parentLayout):
		self.frameCenterOfMass = cmds.frameLayout(parent = parentLayout, label = "CENTER OF MASS", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		com.CenterOfMass().UILayout(self.frameCenterOfMass)
	def LayoutExperimental(self, parentLayout):
		self.frameExperimental = cmds.frameLayout(parent = parentLayout, label = "EXPERIMENTAL", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		countOffsets = 1
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidthMargin / countOffsets)

		cmds.button(label = "Motion Trail", command = MotionTrail.Create, backgroundColor = Colors.orange10)
		cmds.popupMenu()
		cmds.menuItem(label = "Select", command = MotionTrail.Select)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Delete", command = MotionTrail.Delete)

	# DOCKING
	def DockCleanup(self):
		dockExists = cmds.dockControl(self.dockName, query = True, exists = True)
		if dockExists:
			cmds.deleteUI(self.dockName, control = True)
			return True
		else:
			return False
	def DockOff(self, *args): # TODO undick window without creation recreation
		dockExists = cmds.dockControl(self.dockName, query = True, exists = True)
		if dockExists:
			cmds.deleteUI(self.dockName, control = True)
			self.CreateUI()
			cmds.showWindow(self.nameWindow)
			print("{0} undocked".format(self.titleText))
		else:
			cmds.warning("Window is not docked")
	def DockSide(self, areaSide, *args):
		dockExists = cmds.dockControl(self.dockName, query = True, exists = True)
		if dockExists:
			cmds.dockControl(self.dockName, edit = True, floating = False, area = areaSide)
		else:
			cmds.dockControl(self.dockName, label = self.labelText, area = areaSide, content = self.nameWindow, allowedArea = self.dockAllowedAreas)
		print("{0} docked {1}".format(self.titleText, areaSide))
	
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
		self.DockSide(self.dockStartArea)

