# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

class Types:
	transform = "transform"
	joint = "joint"
	constraint = "constraint"
	animLayer = "animLayer"

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

	localScaleX = "localScaleX"
	localScaleY = "localScaleY"
	localScaleZ = "localScaleZ"

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

