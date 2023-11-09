# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

import maya.cmds as cmds
from utils import Colors

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
	def __init__(self, label = "label", value = False, command = "pass", menuReset = True, enabled = True, ccResetAll = "pass"):
		self.value = value
		self.checkbox = cmds.checkBox(label = label, value = value, changeCommand = command, enable = enabled)
		
		cmds.popupMenu()
		
		if (menuReset):
			cmds.menuItem(label = "reset current", command = self.Reset)
			cmds.menuItem(label = "reset all", command = ccResetAll)
	
	def Get(self, *args):
		return cmds.checkBox(self.checkbox, query = True, value = True)
	
	def Set(self, value = None, *args):
		cmds.checkBox(self.checkbox, edit = True, value = value)
	
	def Reset(self, *args):
		cmds.checkBox(self.checkbox, edit = True, value = self.value)

class Slider: # TODO
	def __init__(self, label="", attribute="", startName="", nameAdd=True, value=0, minMax=[0, 1, 0, 1], parent="", command="pass", precision=3, widthWindow = 10, widthMarker = 10, columnWidth3 = (5, 5, 5), menuReset=True, menuScan=True, ccResetAll="pass", ccScanAll="pass"):
		self.attribute = attribute
		self.startName = startName
		self.addSelectedName = nameAdd
		self.value = value
		self.command = command
		self.precision = precision
		self.markerColorDefault = Colors.blackWhite50
		self.markerColorChanged = Colors.blue50
		self.valueCached = 0;
		
		cmds.flowLayout(parent = parent)
		
		self.slider = cmds.floatSliderGrp(
			label = " " + label,
			value = self.value,
			changeCommand = self.command,
			dragCommand = self.command,
			fieldMinValue = minMax[0],
			fieldMaxValue = minMax[1],
			minValue = minMax[2],
			maxValue = minMax[3],
			field = True,
			precision = self.precision,
			width = widthWindow - widthMarker,
			columnAlign = (1, "left"),
			columnWidth3 = columnWidth3,
			enableKeyboardFocus = True,
			)
		
		cmds.popupMenu(parent = self.slider)
		
		if (menuReset):
			cmds.menuItem(label = "reset current", command = self.Reset)
			cmds.menuItem(label = "reset all", command = ccResetAll)
		
		if (menuScan):
			cmds.menuItem(divider = True)
			cmds.menuItem(label = "scan current", command = self.Scan)
			cmds.menuItem(label = "scan all", command = ccScanAll)
		
		self._marker = cmds.button(label = "", enable = 0, w = widthMarker, backgroundColor = self.markerColorDefault)
	
	def Get(self, *args):
		return cmds.floatSliderGrp(self.slider, query = True, value = True)
	
	def Set(self, value = None, *args): # FIXME
		# if (value == None): _value = cmds.floatSliderGrp(self.slider, query = True, value = True)
		# else:
		# 	_value = value
		# 	cmds.floatSliderGrp(self.slider, edit = True, value = _value)
		# 	self.command()
		
		# # Marker update
		# if (_value != self.value):
		# 	cmds.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
		# else:
		# 	cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
		
		# # Check selected
		# _selectedName = _OVERLAPPY.selected
		# if (_selectedName == ""):
		# 	return
		
		# # Add suffix or not
		# _selectedName = _OVERLAPPY.ConvertText(_selectedName)
		# if (self.addSelectedName):
		# 	_selectedName = self.startName + _selectedName
		# else:
		# 	_selectedName = self.startName
		
		# # Set attribute
		# try:
		# 	cmds.setAttr(_selectedName + self.attribute, _value)
		# except:
		# 	# print("Can't set value")
		# 	pass
		pass
	
	def Reset(self, *args):
		cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
		cmds.floatSliderGrp(self.slider, edit = True, value = self.value)
		self.command()
	
	def Scan(self, *args): # FIXME
		# _firstName = _OVERLAPPY.selected
		# if (_firstName == ""):
		# 	return
		# _firstName = _OVERLAPPY.ConvertText(_firstName)
		# if (self.addSelectedName):
		# 	_firstName = self.startName + _firstName
		# else:
		# 	_firstName = self.startName
		
		# # Get attribute
		# try:
		# 	# print(firstName + self._attribute)
		# 	_value = cmds.getAttr(_firstName + self.attribute)
		# 	cmds.floatSliderGrp(self.slider, edit = True, value = _value)
		# except:
		# 	# print("Can't get value")
		# 	return
		
		# # Marker update
		# if (round(_value, 3) != self.value):
		# 	cmds.button(self._marker, edit = True, backgroundColor = self.markerColorChanged)
		# else:
		# 	cmds.button(self._marker, edit = True, backgroundColor = self.markerColorDefault)
		pass
	
	def GetCached(self, *args):
		return self.valueCached
	
	def SetCached(self, *args):
		self.valueCached = cmds.floatSliderGrp(self.slider, query = True, value = True)
	
	def ResetCached(self, *args):
		self.valueCached = 0