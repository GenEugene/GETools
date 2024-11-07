import maya.cmds as cmds
import math


nameGroup = "grpPolygon"
namePolygon = "CustomPolygon"
nameLocator = "locator_"
nameCluster = "cluster_"


def CreatePolygonWithLocators(numPoints=3, radius=10):
	if numPoints < 3:
		cmds.error("Number of points must be 3 or more to create a polygon")
	
	### Create main group as a container for all new objects
	mainGroup = cmds.group(name = nameGroup, empty = True)

	### Calculate vertex positions based on the number of points and radius
	angleStep = 360 / numPoints
	vertices = []
	for i in range(numPoints):
		angle_rad = math.radians(i * angleStep)
		x = math.cos(angle_rad) * radius
		z = math.sin(angle_rad) * radius
		vertices.append((x, 0, z))
	
	### Create the polygon
	poly = cmds.polyCreateFacet(point = vertices, name = namePolygon)[0]
	
	### Invert normals so the polygon faces upwards
	cmds.polyNormal(poly, normalMode = 0)  # normalMode = 0 inverts normals

	### Create locators for each vertex and attach them via clusters
	locators = []
	handles = []
	for i, vertex in enumerate(vertices):
		### Create locator and position it at the vertex's initial position
		locator = cmds.spaceLocator(name = "{0}{1}".format(nameLocator, i + 1))[0]
		locators.append(locator)
		cmds.xform(locator, worldSpace = True, translation = vertex)
		
		### Create a cluster for the current vertex
		cluster, handle = cmds.cluster("{0}.vtx[{1}]".format(poly, i), name = "{0}{1}".format(nameCluster, i + 1))
		handles.append(handle)
		cmds.setAttr(handle + ".visibility", 0)

		### Attach the cluster to the locator
		cmds.pointConstraint(locator, handle, maintainOffset = False)
	
	### Parent to group
	cmds.parent(poly, mainGroup)
	cmds.parent(locators, mainGroup)
	cmds.parent(handles, mainGroup)

	### Select polygon
	cmds.select(poly, replace = True)

	return poly


CreatePolygonWithLocators(4)

