import maya.cmds as cmds
# from math import pow, sqrt
# from functools import partial
from utils import Colors
from utils import Scene

class GeneralWindow:
	def __init__(self):
		### SETUP
		self.version = "v0.0.2"
		self.titleText = "GETools"
		self.windowWidth = 300
		self.windowHeight = 100
		# self.lineHeight = 20
		# self.minMaxWeight = (0, 100)
		self.margin = 5
		self.windowWidthMargin = self.windowWidth - self.margin * 2
		### WINDOW
		self.nameWindow = "windowGETools"
		### DOCK
		self.dockLabel = "GETOOLS"
		self.dockName = "dockGETools"
		self.dockAllowedAreas = ["right", "left"]
		self.dockStartArea = "left"

	def CreateUI(self):
		# WINDOW
		if cmds.window(self.nameWindow, exists = True):
			cmds.deleteUI(self.nameWindow)
		cmds.window(self.nameWindow, title = self.titleText + " " + self.version, maximizeButton = False, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		# cmds.window(self.window_name, edit = True, resizeToFitChildren = True) # , widthHeight = (self.windowWidth, self.windowHeight)
		layout0 = cmds.columnLayout(adjustableColumn = True, width = self.windowWidth)


		# HEAD MENU
		cmds.menuBarLayout()
		
		cmds.menu(label = "File")
		cmds.menuItem(label = "Reload Scene (force)", command = self.SceneReload)
		cmds.menuItem(label = "Exit Maya (force)", command = self.ExitMaya)
		
		cmds.menu(label = "Edit")
		cmds.menuItem(label = "Save Settings")
		cmds.menuItem(label = "Load Settings")
		cmds.menuItem(label = "Reset Settings")

		cmds.menu(label = "Display")
		cmds.menuItem(label = "Expand All") # , command = partial(self.LayoutsCollapseLogic, False)
		cmds.menuItem(label = "Collapse All") # , command = partial(self.LayoutsCollapseLogic, True)

		cmds.menu(label = "DEV")
		# cmds.menuItem(label = "Dev Tools toggle", checkBox = False) # , command = self.LayoutDevToolsToggle
		cmds.menuItem(label = "Reload Script") # , command = self.Restart

		cmds.menu(label = "Help")
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/GETools", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://app.gumroad.com/geneugene", absolute = True) # TODO add new gumroad link
		def LinkYoutubeTutorial(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True) # TODO add new youtube link with tutorial
		def LinkLinkedin(self): cmds.showHelp("https://www.linkedin.com/in/geneugene", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True)
		def LinkDiscord(self): cmds.showHelp("https://discord.gg/heMxJhTqCz", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/Overlappy/discussions/categories/report-a-problem", absolute = True) # TODO create this page on GETools github https://github.com/GenEugene/GETools/issues
		cmds.menuItem(label = "About GETools", enable = False) # TODO add window with information
		cmds.menuItem(dividerLabel = "Links", divider = True)
		cmds.menuItem(label = "GitHub", command = LinkGithub)
		cmds.menuItem(label = "Gumroad", command = LinkGumroad)
		cmds.menuItem(label = "Tutorial Video", command = LinkYoutubeTutorial)
		cmds.menuItem(dividerLabel = "Contacts", divider = True)
		cmds.menuItem(label = "Linkedin", command = LinkLinkedin)
		cmds.menuItem(label = "YouTube", command = LinkYoutube)
		cmds.menuItem(label = "Discord", command = LinkDiscord)
		cmds.menuItem(dividerLabel = "Support", divider = True)
		cmds.menuItem(label = "Report a Problem...", command = LinkReport)


		# FRAME 1
		cmds.frameLayout(parent = layout0, label = "FRAME 1", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		countOffsets = 3
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidthMargin / countOffsets)
		cmds.button(label = "test", backgroundColor = Colors.green10)
		cmds.button(label = "test", backgroundColor = Colors.green50)
		cmds.button(label = "test", backgroundColor = Colors.green100)
		

		# FRAME 2
		cmds.frameLayout(parent = layout0, label = "FRAME 2", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		countOffsets = 2
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidthMargin / countOffsets)
		cmds.button(label = "test", backgroundColor = Colors.orange10)
		cmds.button(label = "test", backgroundColor = Colors.orange50)
		

		# FRAME 3
		cmds.frameLayout(parent = layout0, label = "FRAME 3", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		countOffsets = 3
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidthMargin / countOffsets)
		cmds.button(label = "test", backgroundColor = Colors.blue10)
		cmds.button(label = "test", backgroundColor = Colors.blue50)
		cmds.button(label = "test", backgroundColor = Colors.blue100)
		

		# DOCK CONTROL
		# cmds.showWindow(self.nameWindow)
		dockExists = cmds.dockControl(self.dockName, query = True, exists = True)
		if dockExists:
			cmds.deleteUI(self.dockName, control = True)
		else:
			cmds.dockControl(self.dockName, label = self.dockLabel, area = self.dockStartArea, content = self.nameWindow, allowedArea = self.dockAllowedAreas) # moveable = True, floating = True


	def SceneReload(self, *args): Scene.Reload()
	def ExitMaya(self, *args): Scene.ExitMaya()


	# EXECUTION
	def RUN(self, *args):
		GeneralWindow().CreateUI()

