import maya.cmds as cmds

def CurveFromTrajectory():
	# Variables
	step = 1
	degree = 3
	# Names
	mtName = "newMotionTrail"
	mtFinalName = mtName + "Handle"
	curveName = "testCurve"


	# Get time start/end
	start = cmds.playbackOptions(q=1, min=1)
	end = cmds.playbackOptions(q=1, max=1)
	# Create motion trail
	cmds.snapshot(n = mtName, mt=1, i=step, st = start, et = end)

	# Get points from motion trail
	cmds.select(mtFinalName, r=1)
	selected = cmds.ls(sl=1, dag=1, et="snapshotShape")
	pts = cmds.getAttr(selected[0] + ".pts")
	size = len(pts)
	for i in range(size):
		pts[i] = pts[i][0:3]
		#print "{0}: {1}".format(i, pts[i])

	# Create curve
	newCurve = cmds.curve(n = curveName, d = degree, p = pts)

	# End
	cmds.delete(mtFinalName)
	cmds.select(cl=1)