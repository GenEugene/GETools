import maya.cmds as cmds

cmds.confirmDialog(
	title = "Zero offset detected",
	message = "For ROTATION BAKING need to use particle offset with non zero values.\nIf offset is zero the particle will remain on the same position as original object, so no rotation will be generated.\n",
	messageAlign = "left",
	icon = "warning",

	button = ["Continue anyway","Cancel"],
	annotation = ["bla", "qwe"],

	defaultButton = "Cancel",
	cancelButton = "Cancel",

	dismissString = "Dismissed"
	)


# Maya 2022+
cmds.framelessDialog(
	title = "Zero offset detected",
	message = "For ROTATION BAKING need to use particle offset with non zero values.\nIf offset is zero the particle will remain on the same position as original object, so no rotation will be generated.\n",
	path = "OVERLAPPY\Particle Offset\MoveX-Y-Z",
	button = ["Bake with zero offset", "Cancel"],
	primary = ["OK"]
	)

