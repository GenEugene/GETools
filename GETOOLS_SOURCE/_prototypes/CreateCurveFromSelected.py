import maya.cmds as cmds

selected = cmds.ls(sl = True)
positions = []

for item in selected:
	position = cmds.xform(item, query = True, translation = True, worldSpace = True)
	positions.append(position)

name = "myCurve"
degree = 4
points = positions

cmds.curve(name = name, degree = degree, point = points)