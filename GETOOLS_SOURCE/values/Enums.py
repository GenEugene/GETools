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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene

class Types:
	transform = "transform"
	joint = "joint"
	locator = "locator"
	constraint = "constraint"
	animLayer = "animLayer"

	shape = "Shape"

	reference = "reference"
	skinCluster = "skinCluster"
	motionTrail = "motionTrail"

class Attributes:
	translateShort = ("tx", "ty", "tz")
	translateLong = ("translateX", "translateY", "translateZ")

	rotateShort = ("rx", "ry", "rz")
	rotateLong = ("rotateX", "rotateY", "rotateZ")

	scaleShort = ("sx", "sy", "sz")
	scaleLong = ("scaleX", "scaleY", "scaleZ")

	visibility = "visibility"

	scaleLocal = ("localScaleX", "localScaleY", "localScaleZ")

	rotateOrder = "rotateOrder"
	startFrame = "startFrame"
	drawStyle = "drawStyle"
	segmentScaleCompensate = "segmentScaleCompensate"

class Constraints:
	parentConstraint = "parentConstraint"
	pointConstraint = "pointConstraint"
	orientConstraint = "orientConstraint"
	scaleConstraint = "scaleConstraint"
	aimConstraint = "aimConstraint"
	list = (parentConstraint, pointConstraint, orientConstraint, scaleConstraint, aimConstraint)

class Infinity:
	infinityConstant = "constant"
	infinityLinear = "linear"
	infinityCycle = "cycle"
	infinityCycleRelative = "cycleRelative"
	infinityOscillate = "oscillate"

class MotionTrail:
	handle = "Handle"
	trailDrawMode = "trailDrawMode"
	template = "template"
	snapshotShape = "snapshotShape"
	pts = "pts"

class Particle:
	"Shape.radius"
	"Shape.conserve"
	"Shape.drag"
	"Shape.damp"
	"Shape.goalSmoothness"
	"Shape.goalWeight[0]"
	".timeScale"

class Other:
	string = "string"
	# PasteKey options
	"replace"
	"replaceCompletely"

	# NAMES
	layerBase = "BaseAnimation"
	python = "Python"
	left = "left"
	right = "right"

	#
	"Shape"
	".overrideEnabled"
	".overrideDisplayType"

