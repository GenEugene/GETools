# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

blackWhite0 = (0, 0, 0)
blackWhite10 = (0.1, 0.1, 0.1)
blackWhite20 = (0.2, 0.2, 0.2)
blackWhite30 = (0.3, 0.3, 0.3)
blackWhite40 = (0.4, 0.4, 0.4)
blackWhite50 = (0.5, 0.5, 0.5)
blackWhite60 = (0.6, 0.6, 0.6)
blackWhite70 = (0.7, 0.7, 0.7)
blackWhite80 = (0.8, 0.8, 0.8)
blackWhite90 = (0.9, 0.9, 0.9)
blackWhite100 = (1, 1, 1)

red10 = (1, 0.6, 0.55)
red50 = (1, 0.45, 0.4)
red100 = (1, 0.2, 0.1)

orange10 = (1, 0.82, 0.5)
orange50 = (1, 0.7, 0.35)
orange100 = (1, 0.55, 0)

yellow10 = (1, 1, 0.6)
yellow50 = (1, 1, 0.4)
yellow100 = (1, 1, 0)

green10 = (0.7, 1, 0.7)
green50 = (0.45, 1, 0.45)
green100 = (0.1, 1, 0.1)

lightBlue10 = (0.6, 1, 1)
lightBlue50 = (0.4, 1, 1)
lightBlue100 = (0.0, 1, 1)

blue10 = (0.55, 0.8, 1)
blue50 = (0.4, 0.65, 1)
blue100 = (0.2, 0.5, 1)

purple10 = (0.75, 0.7, 1)
purple50 = (0.75, 0.5, 1)
purple100 = (0.75, 0.3, 1)


import maya.cmds as cmds

class ColorsPalette:
	def __init__(self):
		self.window_name = "windowColorCalibration"
		self.titleText = "Colors Palette"
		self.windowWidth = 330
		self.windowHeight = 10
		self.lineHeight = 20
	
	def CreateUI(self):
		# WINDOW
		if cmds.window(self.window_name, exists = True):
			cmds.deleteUI(self.window_name)
		cmds.window(self.window_name, title = self.titleText, maximizeButton = False, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		cmds.window(self.window_name, edit = True, resizeToFitChildren = True)
		layoutMain = cmds.columnLayout(adjustableColumn = False, width = self.windowWidth)

		# TODO add color console print on button press
		buttonsBlackWhite = 11
		cmds.gridLayout(parent = layoutMain, numberOfColumns = buttonsBlackWhite, cellWidth = self.windowWidth / buttonsBlackWhite)
		#
		cmds.button(label = "0", backgroundColor = blackWhite0)
		cmds.button(label = "10", backgroundColor = blackWhite10)
		cmds.button(label = "20", backgroundColor = blackWhite20)
		cmds.button(label = "30", backgroundColor = blackWhite30)
		cmds.button(label = "40", backgroundColor = blackWhite40)
		cmds.button(label = "50", backgroundColor = blackWhite50)
		cmds.button(label = "60", backgroundColor = blackWhite60)
		cmds.button(label = "70", backgroundColor = blackWhite70)
		cmds.button(label = "80", backgroundColor = blackWhite80)
		cmds.button(label = "90", backgroundColor = blackWhite90)
		cmds.button(label = "100", backgroundColor = blackWhite100)

		buttonsColors = 3
		cmds.gridLayout(parent = layoutMain, numberOfColumns = buttonsColors, cellWidth = self.windowWidth / buttonsColors)
		#
		cmds.button(label = "red 10", backgroundColor = red10)
		cmds.button(label = "red 50", backgroundColor = red50)
		cmds.button(label = "red 100", backgroundColor = red100)
		#
		cmds.button(label = "orange 10", backgroundColor = orange10)
		cmds.button(label = "orange 50", backgroundColor = orange50)
		cmds.button(label = "orange 100", backgroundColor = orange100)
		#
		cmds.button(label = "yellow 10", backgroundColor = yellow10)
		cmds.button(label = "yellow 50", backgroundColor = yellow50)
		cmds.button(label = "yellow 100", backgroundColor = yellow100)
		#
		cmds.button(label = "green 10", backgroundColor = green10)
		cmds.button(label = "green 50", backgroundColor = green50)
		cmds.button(label = "green 100", backgroundColor = green100)
		#
		cmds.button(label = "light blue 10", backgroundColor = lightBlue10)
		cmds.button(label = "light blue 50", backgroundColor = lightBlue50)
		cmds.button(label = "light blue 100", backgroundColor = lightBlue100)
		#
		cmds.button(label = "blue 10", backgroundColor = blue10)
		cmds.button(label = "blue 50", backgroundColor = blue50)
		cmds.button(label = "blue 100", backgroundColor = blue100)
		#
		cmds.button(label = "purple 10", backgroundColor = purple10)
		cmds.button(label = "purple 50", backgroundColor = purple50)
		cmds.button(label = "purple 100", backgroundColor = purple100)

		# RUN WINDOW
		cmds.showWindow(self.window_name)

