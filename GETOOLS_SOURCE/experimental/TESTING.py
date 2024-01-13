import maya.cmds as cmds

nameWindow = "TEST_window"
windowWidth = 300
windowHeight = 100
margin = 5
windowWidthMargin = windowWidth - margin*2


# Create a new window
if cmds.window(nameWindow, exists = True):
	cmds.deleteUI(nameWindow)

cmds.window(nameWindow, title = "Label", maximizeButton = False, sizeable = True, widthHeight = (windowWidth, windowHeight))
layout0 = cmds.columnLayout(adjustableColumn = True, width = windowWidth)


# FRAME 1
cmds.frameLayout(parent = layout0, label = "FRAME 1", collapsable = True, marginWidth = margin, marginHeight = margin)
countOffsets = 3
cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = windowWidthMargin / countOffsets)
cmds.button(label = "test")
cmds.button(label = "test")
cmds.button(label = "test")
cmds.button(label = "test")
cmds.button(label = "test")



cmds.showWindow(nameWindow)
