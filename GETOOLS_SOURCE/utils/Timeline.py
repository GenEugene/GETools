# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
import maya.mel as mel

class TimeRangeHandler:
	def __init__(self):
		self.values = [0, 0, 0, 0, 0] # current, minOuter, minInner, maxInner, maxOuter
	
	def Scan(self, *args):
		self.values[0] = cmds.currentTime(query = True)
		self.values[1] = cmds.playbackOptions(query = True, animationStartTime = True)
		self.values[2] = cmds.playbackOptions(query = True, min = True)
		self.values[3] = cmds.playbackOptions(query = True, max = True)
		self.values[4] = cmds.playbackOptions(query = True, animationEndTime = True)
	
	def SetCurrent(self, value, *args):
		cmds.currentTime(value)
	
	def SetCurrentCached(self, *args):
		cmds.currentTime(self.values[0])
	
	def SetMin(self, value, *args):
		cmds.playbackOptions(edit = True, min = value)
	
	def Reset(self): # , *args
		cmds.playbackOptions(edit = True, animationStartTime = self.values[1], min = self.values[2], max = self.values[3], animationEndTime = self.values[4])
		cmds.currentTime(self.values[2])


# Utilities
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
	return (min, max)

def FetchTimeline():
	return mel.eval('$tmpVar=$gPlayBackSlider')
def CheckHighlighting():
	return cmds.timeControl(FetchTimeline(), query = True, rangeVisible = True)
def GetSelectedTimeRange():
	return cmds.timeControl(FetchTimeline(), query = True, rangeArray = True)

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
		minMaxInner = GetTimeMinMax(True)
		cmds.playbackOptions(animationStartTime = minMaxInner[0], animationEndTime = minMaxInner[1])
	elif (mode == 7):
		selectedTime = GetSelectedTimeRange()
		endTime = selectedTime[1] - 1
		cmds.playbackOptions(min = selectedTime[0], max = endTime)