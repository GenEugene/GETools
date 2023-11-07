import maya.cmds as cmds
from utils import Colors
# from utils import UI
# from utils import Constraints
# from utils import Baker
# from utils import Locators

class GeneralWindow:
	def __init__(self):
		### SETUP
		self.version = "v0.0.0"
		self.titleText = "GETools"
		self.windowWidth = 300
		self.windowHeight = 100
		# self.lineHeight = 20
		# self.minMaxWeight = (0, 100)
		self.margin = 5
		### WINDOW
		self.nameWindow = "windowGeneral"
		### DOCK
		self.dockName = None
		self.allowedAreas = ['right', 'left']

	def CreateUI(self):
		# WINDOW
		if cmds.window(self.nameWindow, exists = True):
			cmds.deleteUI(self.nameWindow)
		cmds.window(self.nameWindow, title = self.titleText + " " + self.version, maximizeButton = False, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		# cmds.window(self.window_name, edit = True, resizeToFitChildren = True) # , widthHeight = (self.windowWidth, self.windowHeight)
		layout0 = cmds.columnLayout(adjustableColumn = True, width = self.windowWidth)


		# FRAME 1
		cmds.frameLayout(parent = layout0, label = "FRAME 1", collapsable = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		# countOffsets = 3
		# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		cmds.button(label = "test", backgroundColor = Colors.green10)
		cmds.button(label = "test", backgroundColor = Colors.green50)
		cmds.button(label = "test", backgroundColor = Colors.green100)
		
		# FRAME 2
		# cmds.frameLayout(parent = layout0, label = "FRAME 2", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		# countOffsets = 3
		# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		# cmds.button(label = "test 1", backgroundColor = Colors.green10)
		# cmds.button(label = "test 2", backgroundColor = Colors.green50)
		
		# FRAME 3
		# cmds.frameLayout(parent = layout0, label = "FRAME 3", collapsable = True, borderVisible = True, backgroundColor = Colors.blackWhite10, marginWidth = self.margin, marginHeight = self.margin)
		# countOffsets = 3
		# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = self.windowWidth / countOffsets)
		# cmds.button(label = "test 1", backgroundColor = Colors.green10)
		# cmds.button(label = "test 2", backgroundColor = Colors.green50)
		# cmds.button(label = "test 3", backgroundColor = Colors.green100)
		
		cmds.showWindow(self.nameWindow)

		# if self.dockName:
		# 	dockExists = cmds.dockControl(self.dockName, query = True, exists = True)
		# 	if dockExists:
		# 		cmds.deleteUI(self.dockName, control=True)
		# 		print("Dock control 'GETOOLS' already exists.")
		# 	else:
		# 		print("No dock control with the label 'GETOOLS' found.")

		# self.dockName = cmds.dockControl(label = "GETOOLS", area = 'left', content = self.nameWindow, allowedArea = self.allowedAreas) # moveable = True
		# print(self.dockName)


	# EXECUTION
	def RUN(self, *args):
		GeneralWindow().CreateUI()


# GeneralWindow().RUN()




# import maya.cmds as cmds

# nameWindow = "qweqwe"
# windowWidth = 300
# windowHeight = 100
# margin = 5
# dockName = None


# # Create a new window
# if cmds.window(nameWindow, exists = True):
# 	cmds.deleteUI(nameWindow)

# cmds.window(nameWindow, title = "Label", maximizeButton = False, sizeable = True, widthHeight = (windowWidth, windowHeight))
# layout0 = cmds.columnLayout(adjustableColumn = True, width = windowWidth)


# # FRAME 1
# cmds.frameLayout(parent = layout0, label = "FRAME 1", collapsable = True, marginWidth = margin, marginHeight = margin)
# # countOffsets = 3
# # cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = windowWidth / countOffsets)
# cmds.button(label = "test")
# cmds.button(label = "test")
# cmds.button(label = "test")

# # Show the window
# # cmds.showWindow(nameWindow)


# dockExists = cmds.dockControl("GETOOLS", query = True, exists = True)
# if dockExists:
#     print("Dock control 'GETOOLS' already exists.")
# else:
#     print("No dock control with the label 'GETOOLS' found.")


# allowedAreas = ['right', 'left']
# dockName = cmds.dockControl(label = "GETOOLS", area = 'left', content = nameWindow, allowedArea = allowedAreas, moveable = True)
# print(dockName)