import maya.cmds as cmds
# from utils import Colors
# from utils import UI
# from utils import Constraints
# from utils import Baker
# from utils import Locators

class GeneralWindow:
	def __init__(self):
		### SETUP
		self.version = "v0.0.1"
		self.titleText = "General Window"
		self.windowWidth = 300
		self.windowHeight = 10
		self.lineHeight = 20
		self.minMaxWeight = (0, 100)
		self.marginWidthHeight = 5
		### WINDOW
		self.window_name = "windowGeneral"

	def CreateUI(self):
		# WINDOW
		if cmds.window(self.window_name, exists = True):
			cmds.deleteUI(self.window_name)
		cmds.window(self.window_name, title = self.titleText + " " + self.version, maximizeButton = True, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		# cmds.window(self.window_name, edit = True, resizeToFitChildren = True) # , widthHeight = (self.windowWidth, self.windowHeight)
		layoutMain = cmds.columnLayout(adjustableColumn = False, width = self.windowWidth) # , h = self.windowHeight
		# uiResize = self.ResizeUI



		# FRAMES 1
		# cmds.frameLayout(parent = layoutMain, label = "FRAME 1", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		# #
		# countOffsets = 1
		# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		# cmds.button(label = "test 1") # backgroundColor = Colors.green10
		
		# cmds.frameLayout(parent = layoutMain, label = "FRAME 2", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		# #
		# countOffsets = 2
		# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		# cmds.button(label = "test 1") # backgroundColor = Colors.green10
		# cmds.button(label = "test 2") # backgroundColor = Colors.green10
		
		# cmds.frameLayout(parent = layoutMain, label = "FRAME 3", collapseCommand = uiResize, expandCommand = uiResize, collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.marginWidthHeight, marginHeight = self.marginWidthHeight)
		# #
		# countOffsets = 3
		# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		# cmds.button(label = "test 1") # backgroundColor = Colors.green10
		# cmds.button(label = "test 2") # backgroundColor = Colors.green10
		# cmds.button(label = "test 3") # backgroundColor = Colors.green10
		


		# RUN WINDOW
		cmds.showWindow(self.window_name)
		# self.ResizeUI()
	# def ResizeUI(self, *args):
	# 	cmds.window(self.window_name, edit = True, height = 1, resizeToFitChildren = True)


	
	# EXECUTION
	def RUN(self, *args):
		GeneralWindow().CreateUI()


# GeneralWindow().RUN()