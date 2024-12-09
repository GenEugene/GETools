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

def CreateLocatorProjectedToMesh(mesh, createInsideOutsideLogic=False, createHeightLogic=False, *args):
	### Variables
	_nameLocatorOriginal = "locOriginal"
	_nameLocatorProjected = "locProjected"
	_nameLambertMaterialProjection = "matGEToolsProjection"
	_borderOffset = 0.01

	### Get shape of mesh
	meshShape = cmds.listRelatives(mesh, shapes = True, fullPath = False)[0]

	### Create locators
	locatorOriginal = cmds.spaceLocator(name = Text.SetUniqueFromText(_nameLocatorOriginal))[0]
	locatorProjected = cmds.spaceLocator(name = Text.SetUniqueFromText(_nameLocatorProjected))[0]

	### Create closestPointOnMesh node
	closestPointOnMeshNode = cmds.createNode("closestPointOnMesh")

	### Connect locators to closestPointOnMesh node
	cmds.connectAttr(meshShape + ".worldMesh[0]", closestPointOnMeshNode + ".inMesh")
	cmds.connectAttr(meshShape + ".worldMatrix[0]", closestPointOnMeshNode + ".inputMatrix")
	cmds.connectAttr(locatorOriginal + ".translate", closestPointOnMeshNode + ".inPosition")
	cmds.connectAttr(closestPointOnMeshNode + ".position", locatorProjected + ".translate")

	if createInsideOutsideLogic:
		### Create inside/outside logic
		floatConstantNode = cmds.createNode("floatConstant")
		cmds.setAttr(floatConstantNode + ".inFloat", _borderOffset)

		### Create nodes for X branch
		floatMathNodeX1 = cmds.createNode("floatMath")
		floatLogicNodeX1 = cmds.createNode("floatLogic")
		floatMathNodeX2 = cmds.createNode("floatMath")
		floatLogicNodeX2 = cmds.createNode("floatLogic")
		floatLogicNodeX = cmds.createNode("floatLogic")

		cmds.setAttr(floatMathNodeX1 + ".operation", 0)
		cmds.setAttr(floatLogicNodeX1 + ".operation", 3)
		cmds.setAttr(floatMathNodeX2 + ".operation", 1)
		cmds.setAttr(floatLogicNodeX2 + ".operation", 2)
		cmds.setAttr(floatLogicNodeX + ".operation", 0)

		cmds.connectAttr(closestPointOnMeshNode + ".inPositionX", floatMathNodeX1 + ".floatA")
		cmds.connectAttr(floatConstantNode + ".outFloat", floatMathNodeX1 + ".floatB")
		cmds.connectAttr(floatMathNodeX1 + ".outFloat", floatLogicNodeX1 + ".floatA")
		cmds.connectAttr(closestPointOnMeshNode + ".positionX", floatLogicNodeX1 + ".floatB")

		cmds.connectAttr(closestPointOnMeshNode + ".inPositionX", floatMathNodeX2 + ".floatA")
		cmds.connectAttr(floatConstantNode + ".outFloat", floatMathNodeX2 + ".floatB")
		cmds.connectAttr(floatMathNodeX2 + ".outFloat", floatLogicNodeX2 + ".floatA")
		cmds.connectAttr(closestPointOnMeshNode + ".positionX", floatLogicNodeX2 + ".floatB")

		cmds.connectAttr(floatLogicNodeX1 + ".outBool", floatLogicNodeX + ".floatA")
		cmds.connectAttr(floatLogicNodeX2 + ".outBool", floatLogicNodeX + ".floatB")

		### Create nodes for Z branch
		floatMathNodeZ1 = cmds.createNode("floatMath")
		floatLogicNodeZ1 = cmds.createNode("floatLogic")
		floatMathNodeZ2 = cmds.createNode("floatMath")
		floatLogicNodeZ2 = cmds.createNode("floatLogic")
		floatLogicNodeZ = cmds.createNode("floatLogic")

		cmds.setAttr(floatMathNodeZ1 + ".operation", 0)
		cmds.setAttr(floatLogicNodeZ1 + ".operation", 3)
		cmds.setAttr(floatMathNodeZ2 + ".operation", 1)
		cmds.setAttr(floatLogicNodeZ2 + ".operation", 2)
		cmds.setAttr(floatLogicNodeZ + ".operation", 0)

		cmds.connectAttr(closestPointOnMeshNode + ".inPositionZ", floatMathNodeZ1 + ".floatA")
		cmds.connectAttr(floatConstantNode + ".outFloat", floatMathNodeZ1 + ".floatB")
		cmds.connectAttr(floatMathNodeZ1 + ".outFloat", floatLogicNodeZ1 + ".floatA")
		cmds.connectAttr(closestPointOnMeshNode + ".positionZ", floatLogicNodeZ1 + ".floatB")

		cmds.connectAttr(closestPointOnMeshNode + ".inPositionZ", floatMathNodeZ2 + ".floatA")
		cmds.connectAttr(floatConstantNode + ".outFloat", floatMathNodeZ2 + ".floatB")
		cmds.connectAttr(floatMathNodeZ2 + ".outFloat", floatLogicNodeZ2 + ".floatA")
		cmds.connectAttr(closestPointOnMeshNode + ".positionZ", floatLogicNodeZ2 + ".floatB")

		cmds.connectAttr(floatLogicNodeZ1 + ".outBool", floatLogicNodeZ + ".floatA")
		cmds.connectAttr(floatLogicNodeZ2 + ".outBool", floatLogicNodeZ + ".floatB")


		### Create nodes for combined X and Z
		floatMathNodeCombined = cmds.createNode("floatMath")
		floatLogicCombinedNode = cmds.createNode("floatLogic")
		colorConditionNode = cmds.createNode("colorCondition")

		cmds.connectAttr(floatLogicNodeX + ".outBool", floatMathNodeCombined + ".floatA")
		cmds.connectAttr(floatLogicNodeZ + ".outBool", floatMathNodeCombined + ".floatB")

		cmds.setAttr(floatLogicCombinedNode + ".operation", 3)

		cmds.connectAttr(floatMathNodeCombined + ".outFloat", floatLogicCombinedNode + ".floatA")
		cmds.connectAttr(floatLogicCombinedNode + ".outBool", colorConditionNode + ".condition")

		cmds.setAttr(colorConditionNode + ".colorA", 0, 1, 0, type = "double3")
		cmds.setAttr(colorConditionNode + ".colorB", 1, 0, 0, type = "double3")
		cmds.setAttr(mesh + ".useOutlinerColor", True)
		cmds.connectAttr(colorConditionNode + ".outColor", mesh + ".outlinerColor")

		# Create Lambert and shading group
		material = cmds.shadingNode("lambert", asShader = True, name = Text.SetUniqueFromText(_nameLambertMaterialProjection))
		shadingGroup = cmds.sets(renderable = True, noSurfaceShader = True, empty = True, name = Text.SetUniqueFromText(material + "SG"))
		cmds.connectAttr(material + ".outColor", shadingGroup + ".surfaceShader", force = True)
		cmds.sets(mesh, edit = True, forceElement = shadingGroup)
		cmds.connectAttr(colorConditionNode + ".outColor", material + ".color")
	
	if createHeightLogic:
		# nodeDistanceDimension = cmds.createNode("distanceDimShape")
		# cmds.distanceDimension(startPoint = (0, 2, 2), endPoint = (1, 5, 6))
		print("TODO: createHeightLogic")

