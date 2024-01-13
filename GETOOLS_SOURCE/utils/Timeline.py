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

def GetTimeMinMax(inner=True):
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

def SetTime(mode=0, *args):
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

