import maya.cmds as cmds

nameWindow = "qweqwe"
windowWidth = 300
windowHeight = 100
margin = 5
dockName = None


# Create a new window
if cmds.window(nameWindow, exists = True):
	cmds.deleteUI(nameWindow)

cmds.window(nameWindow, title = "Label", maximizeButton = False, sizeable = True, widthHeight = (windowWidth, windowHeight))
layout0 = cmds.columnLayout(adjustableColumn = True, width = windowWidth)


# FRAME 1
cmds.frameLayout(parent = layout0, label = "FRAME 1", collapsable = True, marginWidth = margin, marginHeight = margin)
# countOffsets = 3
# cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = windowWidth / countOffsets)
cmds.button(label = "test")
cmds.button(label = "test")
cmds.button(label = "test")

# Show the window
# cmds.showWindow(nameWindow)


dockExists = cmds.dockControl("GETOOLS", query = True, exists = True)
if dockExists:
    print("Dock control 'GETOOLS' already exists.")
else:
    print("No dock control with the label 'GETOOLS' found.")




allowedAreas = ['right', 'left']
dockName = cmds.dockControl(label = "GETOOLS", area = 'left', content = nameWindow, allowedArea = allowedAreas, moveable = True)

print(dockName)


