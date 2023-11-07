import maya.cmds as cmds

def Create(self, *args):
	_selected = cmds.ls(selection = True) # Get selected objects
	if (len(_selected) == 0):
		cmds.warning("You must select at least 1 object")
		return
	_name = "MotionTrail_1"
	_step = 1
	_start = cmds.playbackOptions(query = True, minTime = True)
	_end = cmds.playbackOptions(query = True, maxTime = True)
	cmds.snapshot(name = _name, motionTrail = True, increment = _step, startTime = _start, endTime = _end)
	_trails = cmds.ls(type = "motionTrail")
	for item in _trails:
		cmds.setAttr(item + "Handle" + "Shape.trailDrawMode", 1)
		cmds.setAttr(item + "Handle" + "Shape.template", 1)

def Select(self, *args):
	_trails = cmds.ls(type = "motionTrail")
	if (len(_trails) == 0): return
	cmds.select(clear = True)
	for item in _trails:
		cmds.select(item + "Handle", add = True)

def Delete(self, *args):
	_trails = cmds.ls(type = "motionTrail")
	if (len(_trails) == 0): return
	for item in _trails:
		cmds.delete(item + "Handle")