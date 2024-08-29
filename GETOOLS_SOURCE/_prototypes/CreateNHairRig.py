import maya.mel as mel
import maya.cmds as cmds

def DraftFunction(): # HACK remove after rig will be finished
	before_objects = cmds.ls()
	mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0" };')
	after_objects = cmds.ls()
	new_objects = list(set(after_objects) - set(before_objects))
	for item in new_objects:
		print(item)

def CreateRig(): # TODO
	targetCurve = "testCurve"
	targetNucleus = "ovlpNucleusttt_RS2_pCube1"
	nameHairSystem = "getools_HairSystem"
	nameFollicle = "getools_Follicle"
	nameOutputCurve = "getools_OutputCurve"

	hairSystemTransformNode = cmds.createNode("transform", name = nameHairSystem, skipSelect = True)
	hairSystemShapeNode = cmds.createNode("hairSystem", name = nameHairSystem + "Shape", parent = hairSystemTransformNode, skipSelect = True)
	follicleTransformNode = cmds.createNode("transform", name = nameFollicle, skipSelect = True)
	follicleShapeNode = cmds.createNode("follicle", name = nameFollicle + "Shape", parent = follicleTransformNode, skipSelect = True)
	outputCurveTransformNode = cmds.createNode("transform", name = nameOutputCurve, skipSelect = True)
	outputCurveShapeNode = cmds.createNode("nurbsCurve", name = nameOutputCurve + "Shape", parent = outputCurveTransformNode, skipSelect = True)

	cmds.connectAttr("time1.outTime", hairSystemShapeNode + ".currentTime")
	cmds.connectAttr(follicleShapeNode + ".outHair", hairSystemShapeNode + ".inputHair[0]")
	cmds.connectAttr(follicleShapeNode + ".outCurve", outputCurveShapeNode + ".create")
	cmds.connectAttr(hairSystemShapeNode + ".outputHair[0]", follicleShapeNode + ".currentPosition")
	cmds.connectAttr(targetCurve + ".worldMatrix[0]", follicleShapeNode + ".startPositionMatrix")
	cmds.connectAttr(targetCurve + "Shape" + ".local", follicleShapeNode + ".startPosition")
	cmds.connectAttr(targetNucleus + ".startFrame", hairSystemShapeNode + ".startFrame")
	cmds.connectAttr(targetNucleus + ".outputObjects[0]", hairSystemShapeNode + ".nextState")
	cmds.connectAttr(hairSystemShapeNode + ".currentState", targetNucleus + ".inputActive[1]")
	cmds.connectAttr(hairSystemShapeNode + ".startState", targetNucleus + ".inputActiveStart[1]")

	cmds.setAttr(hairSystemShapeNode + ".active", True)
	cmds.setAttr(hairSystemShapeNode + ".solverDisplay", 1)
	cmds.setAttr(hairSystemShapeNode + ".collideWidthOffset", 50)

	# setAttr "getools_HairSystemShape.collide" 1;
	# setAttr "getools_HairSystemShape.selfCollide" 0;
	# setAttr "getools_HairSystemShape.bounce" 0;
	# setAttr "getools_HairSystemShape.friction" 0.5;
	# setAttr "getools_HairSystemShape.stickiness" 0;

	# setAttr "getools_HairSystemShape.stretchResistance" 10;
	# setAttr "getools_HairSystemShape.compressionResistance" 10;
	# setAttr "getools_HairSystemShape.bendResistance" 1;
	# setAttr "getools_HairSystemShape.twistResistance" 0;
	# setAttr "getools_HairSystemShape.extraBendLinks" 0;
	# setAttr "getools_HairSystemShape.restLengthScale" 1;

	# setAttr "getools_HairSystemShape.stiffnessScale[1].stiffnessScale_FloatValue" 0.2;

	# setAttr "getools_FollicleShape.pointLock" 1; # 1, 2, 3
	# setAttr "getools_FollicleShape.degree" 1; # 1, 2, 3

	# setAttr "nRigidShape1.isDynamic" 1;



