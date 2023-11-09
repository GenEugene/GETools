import maya.cmds as cmds
import maya.mel as mel

def SetTimeCurrent(value):
	cmds.currentTime(value, edit = True, update = True)

def GetTimeCurrent():
	return cmds.currentTime(query = True)

def GetTimeMinMax(inner = True):
	if inner:
		min = cmds.playbackOptions(query = True, min = True)
		max = cmds.playbackOptions(query = True, max = True)
	else:
		min = cmds.playbackOptions(query = True, animationStartTime = True)
		max = cmds.playbackOptions(query = True, animationEndTime = True)
	return min, max

def GetSelectedTimeRange():
	timeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
	return cmds.timeControl(timeSlider, query = True, rangeArray = True)

def SetTime(mode = 0, *args):
	if (mode == 1):
		cmds.playbackOptions(min = GetTimeCurrent())
	elif (mode == 2):
		cmds.playbackOptions(max = GetTimeCurrent())
	elif (mode == 3):
		cmds.playbackOptions(animationStartTime = GetTimeCurrent())
	elif (mode == 4):
		cmds.playbackOptions(animationEndTime = GetTimeCurrent())
	elif (mode == 5):
		minMaxOuter = GetTimeMinMax(False)
		cmds.playbackOptions(min = minMaxOuter[0], max = minMaxOuter[1])
	elif (mode == 6):
		minMaxInner = GetTimeMinMax()
		cmds.playbackOptions(animationStartTime = minMaxInner[0], animationEndTime = minMaxInner[1])
	elif (mode == 7):
		selectedTime = GetSelectedTimeRange()
		endTime = selectedTime[1] - 1
		cmds.playbackOptions(min = selectedTime[0], max = endTime)