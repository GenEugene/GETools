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

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.mel as mel
import maya.cmds as cmds

from ..utils import Selector


_prefix = "getools_"
_nameHairSystem = _prefix + "HairSystem"
_nameFollicle = _prefix + "Follicle"
_nameOutputCurve = _prefix + "OutputCurve"


def CreateNHairOnCurve(curve, nucleus): # TODO
	if (curve == None or nucleus == None):
		cmds.warning("No curve or nucleus node")
		return

	# Create hair rig nodes
	hairSystemTransformNode = cmds.createNode("transform", name = _nameHairSystem, skipSelect = True)
	hairSystemShapeNode = cmds.createNode("hairSystem", name = _nameHairSystem + "Shape", parent = hairSystemTransformNode, skipSelect = True)
	follicleTransformNode = cmds.createNode("transform", name = _nameFollicle, skipSelect = True)
	follicleShapeNode = cmds.createNode("follicle", name = _nameFollicle + "Shape", parent = follicleTransformNode, skipSelect = True)
	outputCurveTransformNode = cmds.createNode("transform", name = _nameOutputCurve, skipSelect = True)
	outputCurveShapeNode = cmds.createNode("nurbsCurve", name = _nameOutputCurve + "Shape", parent = outputCurveTransformNode, skipSelect = True)

	# Connect hair rig attributes
	cmds.connectAttr("time1.outTime", hairSystemShapeNode + ".currentTime")
	cmds.connectAttr(follicleShapeNode + ".outHair", hairSystemShapeNode + ".inputHair[0]")
	cmds.connectAttr(follicleShapeNode + ".outCurve", outputCurveShapeNode + ".create")
	cmds.connectAttr(hairSystemShapeNode + ".outputHair[0]", follicleShapeNode + ".currentPosition")
	cmds.connectAttr(curve + ".worldMatrix[0]", follicleShapeNode + ".startPositionMatrix")
	cmds.connectAttr(curve + "Shape" + ".local", follicleShapeNode + ".startPosition")
	cmds.connectAttr(nucleus + ".startFrame", hairSystemShapeNode + ".startFrame")
	cmds.connectAttr(nucleus + ".outputObjects[0]", hairSystemShapeNode + ".nextState")
	cmds.connectAttr(hairSystemShapeNode + ".currentState", nucleus + ".inputActive[1]")
	cmds.connectAttr(hairSystemShapeNode + ".startState", nucleus + ".inputActiveStart[1]")

	# Hair System nucleus activation
	cmds.setAttr(hairSystemShapeNode + ".active", True)

	# Collisions
	# setAttr "getools_HairSystemShape.collide" 1;
	# setAttr "getools_HairSystemShape.selfCollide" 0;
	cmds.setAttr(hairSystemShapeNode + ".collideWidthOffset", 50)
	cmds.setAttr(hairSystemShapeNode + ".solverDisplay", 1)
	# setAttr "getools_HairSystemShape.bounce" 0;
	# setAttr "getools_HairSystemShape.friction" 0.5;
	# setAttr "getools_HairSystemShape.stickiness" 0;

	# Dynamic Properties
	# setAttr "getools_HairSystemShape.stretchResistance" 10;
	# setAttr "getools_HairSystemShape.compressionResistance" 10;
	# setAttr "getools_HairSystemShape.bendResistance" 1;
	# setAttr "getools_HairSystemShape.twistResistance" 0;
	# setAttr "getools_HairSystemShape.extraBendLinks" 0;
	# setAttr "getools_HairSystemShape.restLengthScale" 1;

	# Stiffness Scale
	# setAttr "getools_HairSystemShape.stiffnessScale[1].stiffnessScale_FloatValue" 0.2;

	# Attraction
	# setAttr "getools_HairSystemShape.startCurveAttract" 0;
	# setAttr "getools_HairSystemShape.attractionDamp" 0;

	# Forces
	# setAttr "getools_HairSystemShape.mass" 1;
	# setAttr "getools_HairSystemShape.drag" 0.05;
	# setAttr "getools_HairSystemShape.tangentialDrag" 0.1;
	# setAttr "getools_HairSystemShape.motionDrag" 0;
	# setAttr "getools_HairSystemShape.damp" 0;
	# setAttr "getools_HairSystemShape.stretchDamp" 0.1;
	# setAttr "getools_HairSystemShape.dynamicsWeight" 1;

	# Follicle Attributes
	# setAttr "getools_FollicleShape.pointLock" 1; # 1, 2, 3
	# setAttr "getools_FollicleShape.degree" 1; # 1, 2, 3

	# Colliders Activation
	# setAttr "nRigidShape1.isDynamic" 1;

	return (hairSystemTransformNode, hairSystemShapeNode), (follicleTransformNode, follicleShapeNode), (outputCurveTransformNode, outputCurveShapeNode)

def CreateNHairOnSelected(nucleus, *args): # TODO
	# Check selected objects
	selectedList = Selector.MultipleObjects(2)
	if (selectedList == None):
		return
	
	curve = None
	
	result = CreateNHairOnCurve(curve, nucleus)

	print(result)


