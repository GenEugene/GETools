# GETOOLS is under the terms of the MIT License
# Copyright (c) 2018-2024 Eugene Gataulin (GenEugene). All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene https://discord.gg/heMxJhTqCz
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds
import math

from ..utils import Text


def CreatePolygonWithLocators(countPoints=3, radius=10, rotation=0):
	if countPoints < 3:
		cmds.warning("Number of points must be 3 or more to create a polygon")
		return None
	
	nameGroup = "grpPolygon"
	namePolygon = "customPolygon"
	nameLocator = "locator_"
	nameCluster = "cluster_"
	
	### Create main group as a container for all new objects
	mainGroup = cmds.group(name = Text.SetUniqueFromText(nameGroup), empty = True)
	cmds.setAttr(mainGroup + ".tx", lock = True)
	cmds.setAttr(mainGroup + ".ty", lock = True)
	cmds.setAttr(mainGroup + ".tz", lock = True)
	cmds.setAttr(mainGroup + ".rx", lock = True)
	cmds.setAttr(mainGroup + ".ry", lock = True)
	cmds.setAttr(mainGroup + ".rz", lock = True)
	cmds.setAttr(mainGroup + ".sx", lock = True)
	cmds.setAttr(mainGroup + ".sy", lock = True)
	cmds.setAttr(mainGroup + ".sz", lock = True)

	### Calculate vertex positions based on the number of points and radius
	angleStep = 360 / countPoints
	vertices = []
	for i in range(countPoints):
		angleRadian = math.radians(i * angleStep + rotation)
		x = math.cos(angleRadian) * radius
		z = math.sin(angleRadian) * radius
		vertices.append((x, 0, z))
	
	### Create the polygon
	poly = cmds.polyCreateFacet(point = vertices, name = Text.SetUniqueFromText(namePolygon))[0]
	
	### Invert normals so the polygon faces upwards
	cmds.polyNormal(poly, normalMode = 0)  # normalMode = 0 inverts normals

	### Create locators for each vertex and attach them via clusters
	locators = []
	handles = []
	for i, vertex in enumerate(vertices):
		### Create locator and position it at the vertex's initial position
		locator = cmds.spaceLocator(name = Text.SetUniqueFromText("{0}{1}".format(nameLocator, i + 1)))[0]
		locators.append(locator)
		cmds.xform(locator, worldSpace = True, translation = vertex)
		
		### Create a cluster for the current vertex
		cluster, handle = cmds.cluster("{0}.vtx[{1}]".format(poly, i), name = Text.SetUniqueFromText("{0}{1}".format(nameCluster, i + 1)))
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

	return mainGroup, poly, locators, handles

def CreateLocatorProjectedToMesh(mesh, createInsideOutsideLogic=False, *args):
	### Names
	nameLocatorOriginal = "locOriginal"
	nameLocatorProjected = "locProjected"

	### Get shape of mesh
	meshShape = cmds.listRelatives(mesh, shapes = True, fullPath = False)[0]

	### Create locators
	locatorOriginal = cmds.spaceLocator(name = nameLocatorOriginal)[0]
	locatorProjected = cmds.spaceLocator(name = nameLocatorProjected)[0]

	### Create closestPointOnMesh node
	closestPointOnMeshNode = cmds.createNode("closestPointOnMesh")

	### Connect locators to closestPointOnMesh node
	cmds.connectAttr(meshShape + ".worldMesh[0]", closestPointOnMeshNode + ".inMesh")
	cmds.connectAttr(meshShape + ".worldMatrix[0]", closestPointOnMeshNode + ".inputMatrix")
	cmds.connectAttr(locatorOriginal + ".translate", closestPointOnMeshNode + ".inPosition")
	cmds.connectAttr(closestPointOnMeshNode + ".position", locatorProjected + ".translate")

	if createInsideOutsideLogic:
		### Create inside/outside logic
		# floatConstantNode = cmds.createNode("floatConstant")
		# floatMathNode = cmds.createNode("floatMath")
		# floatLogicNode = cmds.createNode("floatLogic")
		# colorConditionNode = cmds.createNode("colorCondition")
		print("TODO: Create Inside Outside Logic")

