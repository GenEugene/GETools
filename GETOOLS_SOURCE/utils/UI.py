# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds

from GETOOLS_SOURCE.utils import Colors
from GETOOLS_SOURCE.modules import Settings

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

class FloatFieldButtons: # TODO test
	def __init__(self,
			# parent = None,
			value = 10,
			precision = 3,
			enabled = True,
			annotation = "",
			command = "pass",
			menuReset = True,
			width = 20,
			height = 10,
			commandUp = "pass",
			commandDown = "pass",
			backgroundColor = Colors.blackWhite70,
			):
		
		buttonsWidth = width / 2
		cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (buttonsWidth, buttonsWidth), columnAttach = [(1, 'both', 0), (2, 'both', 0)] )

		self.floatLocatorSize = FloatField(value = value, precision = precision, annotation = annotation, enabled = enabled, command = command, menuReset = menuReset)

		ButtonLeftRight(width = buttonsWidth * 0.9, height = height, annotation = annotation, commandLeft = commandUp, commandRight = commandDown, backgroundColor = backgroundColor) # TODO

		cmds.setParent('..')
		cmds.setParent('..')

class ButtonLeftRight:
	def __init__(self,
			# parent = None, # TODO
			width = 20,
			height = 10,
			annotation = "",
			commandLeft = "pass",
			commandRight = "pass",
			backgroundColor = Colors.blackWhite70,
			):
		
		buttonsWidth = width / 2
		cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (buttonsWidth, buttonsWidth), columnAttach = [(1, 'both', 0), (2, 'both', 0)] )
		cmds.button(label = "<", height = height, command = commandLeft, annotation = annotation, backgroundColor = backgroundColor)
		cmds.button(label = ">", height = height, command = commandRight, annotation = annotation, backgroundColor = backgroundColor)
		cmds.setParent('..')

class FloatField:
	def __init__(self,
			value = 10,
			precision = 3,
			enabled = True,
			annotation = "",
			command = "pass",
			menuReset = True,
			minValue = float("-inf"),
			maxValue = float("inf"),
			):
		
		self.valueDefault = value
		self.floatField = cmds.floatField(value = value, precision = precision, changeCommand = command, enable = enabled, annotation = annotation, minValue = minValue, maxValue = maxValue)

		if (menuReset):
			cmds.popupMenu()
			cmds.menuItem(label = "reset", command = self.Reset)
	
	def Get(self, *args):
		return cmds.floatField(self.floatField, query = True, value = True)
	
	def Set(self, value = 0, *args):
		cmds.floatField(self.floatField, edit = True, value = value)
	
	def Reset(self, *args):
		cmds.floatField(self.floatField, edit = True, value = self.valueDefault)

class Checkbox:
	def __init__(self,
			# parent = None, # TODO
			label = "label",
			value = False,
			enable = True,
			annotation = "",
			command = "pass",
			# commandResetAll = "",
			menuReset = True,
			):
		
		self.valueDefault = value
		self.checkbox = cmds.checkBox(label = label, value = value, changeCommand = command, enable = enable, annotation = annotation)

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
			command = "pass",
			menuReset = True,
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
		
		windowName = Settings.windowName
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
		
		if (self.command != "pass"):
			self.command()
	
	def Reset(self, *args):
		cmds.button(self.marker, edit = True, backgroundColor = self.markerColorDefault)
		cmds.floatSliderGrp(self.slider, edit = True, value = self.valueDefault)
		if (self.command != "pass"):
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