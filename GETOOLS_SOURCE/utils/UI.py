# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from utils import Colors
from modules import GeneralWindow

class Window: # TODO
	def __init__(self, titleText = "My Window Name", windowWidth = 150, windowHeight = 50, nameWindow = "myWindowDefault"):
		self.titleText = titleText
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.nameWindow = nameWindow
		self.layoutMain = None

	def CreateWindow(self):
		if cmds.window(self.nameWindow, exists = True):
			cmds.deleteUI(self.nameWindow)
		cmds.window(self.nameWindow, title = self.titleText, widthHeight = (self.windowWidth, self.windowHeight))
		# cmds.window(self.nameWindow, title = self.titleText, minimizeButton = True, maximizeButton = True, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		# cmds.window(self.nameWindow, edit = True, resizeToFitChildren = True)
		self.layoutMain = cmds.columnLayout(adjustableColumn = True, width = self.windowWidth)
	
	def RunWindow(self):
		cmds.showWindow(self.nameWindow)

class Checkbox:
	def __init__(self,
			label = "label",
			value = False,
			menuReset = True,
			enabled = True,
			annotation = "",
			command = "pass",
			# commandResetAll = "",
			):
		
		self.valueDefault = value
		self.checkbox = cmds.checkBox(label = label, value = value, changeCommand = command, enable = enabled, annotation = annotation)

		if (menuReset):
			cmds.popupMenu()
			cmds.menuItem(label = "reset", command = self.Reset)
			# cmds.menuItem(label = "reset all", command = commandResetAll)
	
	def Get(self, *args):
		return cmds.checkBox(self.checkbox, query = True, value = True)
	
	def Set(self, value = None, *args):
		cmds.checkBox(self.checkbox, edit = True, value = value)
	
	def Reset(self, *args):
		cmds.checkBox(self.checkbox, edit = True, value = self.valueDefault)

class Slider:
	def __init__(self,
			parent = None,
			label = "label",
			annotation = "",
			value = 0,
			minMax = [0, 1, 0, 1],
			precision = 3,
			widthWindow = 50,
			widthMarker = 10,
			columnWidth3 = (5, 5, 5),
			menuReset = True,
			command = "pass",
			):
		
		self.valueDefault = value
		self.valueCached = 0;
		self.command = command
		self.precision = precision
		self.markerColorDefault = Colors.blackWhite50
		self.markerColorChanged = Colors.blue50
		
		self.layoutFlow = cmds.flowLayout(parent = parent)
		self.marker = cmds.button("sliderButtonMarker", parent = self.layoutFlow, label = "", command = self.Reset, width = widthMarker, backgroundColor = self.markerColorDefault, annotation = "Reset value")
		self.slider = cmds.floatSliderGrp(
			"slider",
			parent = self.layoutFlow,
			label = " " + label,
			annotation = annotation,
			value = self.valueDefault,
			fieldMinValue = minMax[0],
			fieldMaxValue = minMax[1],
			minValue = minMax[2],
			maxValue = minMax[3],
			precision = self.precision,
			width = widthWindow - widthMarker,
			columnAlign = (1, "left"),
			columnWidth3 = columnWidth3,
			enableKeyboardFocus = True,
			changeCommand = self.Set,
			dragCommand = self.Set,
			field = True,
			)
		
		windowName = GeneralWindow.GeneralWindowSettings.windowName
		self.slider = self.slider.replace(windowName + "|", "") # fix for docked window only. Don't know how to avoid issue
		
		if (menuReset):
			cmds.popupMenu(parent = self.slider)
			cmds.menuItem(label = "reset", command = self.Reset)
	
	def Get(self, *args):
		return cmds.floatSliderGrp(self.slider, query = True, value = True)
	
	def Set(self, value = None, *args):
		if (value == None):
			_value = cmds.floatSliderGrp(self.slider, query = True, value = True)
		else:
			_value = value
			cmds.floatSliderGrp(self.slider, edit = True, value = _value)
			# self.command()
		
		# Marker update
		if (_value != self.valueDefault):
			cmds.button(self.marker, edit = True, backgroundColor = self.markerColorChanged)
		else:
			cmds.button(self.marker, edit = True, backgroundColor = self.markerColorDefault)
		
		self.command()
	
	def Reset(self, *args):
		cmds.button(self.marker, edit = True, backgroundColor = self.markerColorDefault)
		cmds.floatSliderGrp(self.slider, edit = True, value = self.valueDefault)
		self.command()
	
	# def Scan(self, *args): # TODO rework or remove
	# 	_firstName = _OVERLAPPY.selected
	# 	if (_firstName == ""):
	# 		return
	# 	_firstName = Text.ConvertSymbols(_firstName)
	# 	if (self.addSelectedName):
	# 		_firstName = self.startName + _firstName
	# 	else:
	# 		_firstName = self.startName
	# 	# Get attribute
	# 	try:
	# 		# print(firstName + self._attribute)
	# 		_value = cmds.getAttr(_firstName + self.attribute)
	# 		cmds.floatSliderGrp(self.slider, edit = True, value = _value)
	# 	except:
	# 		# print("Can't get value")
	# 		return
	# 	# Marker update
	# 	if (round(_value, 3) != self.valueDefault):
	# 		cmds.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
	# 	else:
	# 		cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
	
	def GetCached(self, *args):
		return self.valueCached
	
	def SetCached(self, *args):
		self.valueCached = cmds.floatSliderGrp(self.slider, query = True, value = True)
	
	def ResetCached(self, *args):
		self.valueCached = 0