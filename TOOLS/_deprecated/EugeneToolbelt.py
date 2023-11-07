### DEPRECATED ###

import maya.cmds as cmds
# from utils import Colors
from utils import Icons
from experimental import ScriptExecutor

### TODO how to avoid this way?
# iconPathGET = "C:\MyFiles\Personal\Repositories\MayaToolbelt\Scripts\MyScripts\Tools\icons\GET.png"
# iconPathTools = "C:\MyFiles\Personal\Repositories\MayaToolbelt\Scripts\MyScripts\Tools\icons\Tools.png"
# iconPathCenterOfMass = "C:\MyFiles\Personal\Repositories\MayaToolbelt\Scripts\MyScripts\Tools\icons\CenterOfMass.png"
# iconPathOverlappy = "C:\MyFiles\Personal\Repositories\MayaToolbelt\Scripts\MyScripts\Tools\icons\Overlappy.png"
###

class EugeneToolbelt:
	def __init__(self):
		### SETUP
		self.version = "v0.0.1"
		self.titleText = "Eugene Toolbelt"
		self.windowWidth = 170
		self.windowHeight = 10
		# self.lineHeight = 20
		# self.minMaxWeight = (0, 100)
		# self.marginWidthHeight = 5
		self.iconSize = 60
		### WINDOW
		self.nameWindow = "windowEugeneToolbelt"
		### CHECKBOXES
		# self.checkboxLocatorHideParent = None

	def CreateUI(self):
		# WINDOW
		if cmds.window(self.nameWindow, exists = True):
			cmds.deleteUI(self.nameWindow)
		cmds.window(self.nameWindow, title = self.titleText + " " + self.version, minimizeButton = False, maximizeButton = False, sizeable = False, widthHeight = (self.windowWidth, self.windowHeight))
		cmds.window(self.nameWindow, edit = True, resizeToFitChildren = True) # , widthHeight = (self.windowWidth, self.windowHeight)
		layoutMain = cmds.columnLayout(adjustableColumn = False, width = self.windowWidth) # , h = self.windowHeight
		# uiResize = self.ResizeUI
		# cmds.separator(style = "none") # "none", "single", "double", "singleDash", "doubleDash", "in" and "out".


		# BUTTONS
		#
		cmds.gridLayout(parent = layoutMain, numberOfColumns = 5, cellWidthHeight = (self.iconSize, self.iconSize))
		textAddToShelf = "Add to current shelf"
		#
		cmds.iconTextButton(style = "iconOnly", image = Icons.tools, command = ScriptExecutor.ToolsRun)
		cmds.popupMenu()
		cmds.menuItem(label = textAddToShelf, command = ScriptExecutor.ToolsAddToShelf)
		#
		cmds.iconTextButton(style = "iconOnly", image = Icons.centerOfMass, command = ScriptExecutor.CenterOfMassRun)
		cmds.popupMenu()
		# cmds.menuItem(dividerLabel = "Created objects", divider = True)
		cmds.menuItem(label = textAddToShelf, command = ScriptExecutor.CenterOfMassAddToShelf)
		#
		cmds.iconTextButton(style = "iconOnly", image = Icons.overlappy, command = ScriptExecutor.OverlappyRun, enable = False)
		cmds.popupMenu()
		cmds.menuItem(label = textAddToShelf, command = ScriptExecutor.OverlappyAddToShelf)
		

		# RUN WINDOW
		cmds.showWindow(self.nameWindow)
		self.ResizeUI()
	def ResizeUI(self, *args):
		cmds.window(self.nameWindow, edit = True, height = 1, resizeToFitChildren = True)
	

	# EXECUTION
	def RUN(self, *args):
		EugeneToolbelt().CreateUI()


# EugeneToolbelt().RUN()