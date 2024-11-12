import maya.cmds as cmds

### Names
nameLocatorOriginal = "locOriginal"
nameLocatorProjected = "locProjected"


### TODO Get objects
selectedMesh = "pPlane1"
selectedMeshShape = cmds.listRelatives(selectedMesh, shapes = True, fullPath = False)[0]


### Create locators
locatorOriginal = cmds.spaceLocator(name = nameLocatorOriginal)[0]
locatorProjected = cmds.spaceLocator(name = nameLocatorProjected)[0]

### Create closestPointOnMesh node
closestPointOnMeshNode = cmds.createNode("closestPointOnMesh")

### Connect locators to closestPointOnMesh node
cmds.connectAttr(selectedMeshShape + ".worldMesh[0]", closestPointOnMeshNode + ".inMesh")
cmds.connectAttr(selectedMeshShape + ".worldMatrix[0]", closestPointOnMeshNode + ".inputMatrix")
cmds.connectAttr(locatorOriginal + ".translate", closestPointOnMeshNode + ".inPosition")
cmds.connectAttr(closestPointOnMeshNode + ".position", locatorProjected + ".translate")

### Create inside/outside logic
# floatConstantNode = cmds.createNode("floatConstant")
# floatMathNode = cmds.createNode("floatMath")
# floatLogicNode = cmds.createNode("floatLogic")
# colorConditionNode = cmds.createNode("colorCondition")

