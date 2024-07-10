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
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

blackWhite00 = (0, 0, 0)
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
from functools import partial

class ColorsPalette:
	def __init__(self):
		self.window_name = "windowColorCalibration"
		self.titleText = "Colors Palette"
		self.windowWidth = 330
		self.windowHeight = 10
		self.lineHeight = 20
	
	def CreateUI(self):
		if cmds.window(self.window_name, exists = True):
			cmds.deleteUI(self.window_name)
		cmds.window(self.window_name, title = self.titleText, maximizeButton = False, sizeable = True, widthHeight = (self.windowWidth, self.windowHeight))
		cmds.window(self.window_name, edit = True, resizeToFitChildren = True)
		layoutMain = cmds.columnLayout(adjustableColumn = False, width = self.windowWidth)

		def ButtonPrint(label, color):
			def PrintColor(label, color, *args):
				print("{0}: {1}".format(label, color))
			cmds.button(label = label, command = partial(PrintColor, label, color), backgroundColor = color)

		buttonsBlackWhite = 11
		cmds.gridLayout(parent = layoutMain, numberOfColumns = buttonsBlackWhite, cellWidth = self.windowWidth / buttonsBlackWhite)
		#
		ButtonPrint(label = "0", color = blackWhite00)
		ButtonPrint(label = "10", color = blackWhite10)
		ButtonPrint(label = "20", color = blackWhite20)
		ButtonPrint(label = "30", color = blackWhite30)
		ButtonPrint(label = "40", color = blackWhite40)
		ButtonPrint(label = "50", color = blackWhite50)
		ButtonPrint(label = "60", color = blackWhite60)
		ButtonPrint(label = "70", color = blackWhite70)
		ButtonPrint(label = "80", color = blackWhite80)
		ButtonPrint(label = "90", color = blackWhite90)
		ButtonPrint(label = "100", color = blackWhite100)

		buttonsColors = 3
		cmds.gridLayout(parent = layoutMain, numberOfColumns = buttonsColors, cellWidth = self.windowWidth / buttonsColors)
		#
		ButtonPrint(label = "red 10", color = red10)
		ButtonPrint(label = "red 50", color = red50)
		ButtonPrint(label = "red 100", color = red100)
		#
		ButtonPrint(label = "orange 10", color = orange10)
		ButtonPrint(label = "orange 50", color = orange50)
		ButtonPrint(label = "orange 100", color = orange100)
		#
		ButtonPrint(label = "yellow 10", color = yellow10)
		ButtonPrint(label = "yellow 50", color = yellow50)
		ButtonPrint(label = "yellow 100", color = yellow100)
		#
		ButtonPrint(label = "green 10", color = green10)
		ButtonPrint(label = "green 50", color = green50)
		ButtonPrint(label = "green 100", color = green100)
		#
		ButtonPrint(label = "light blue 10", color = lightBlue10)
		ButtonPrint(label = "light blue 50", color = lightBlue50)
		ButtonPrint(label = "light blue 100", color = lightBlue100)
		#
		ButtonPrint(label = "blue 10", color = blue10)
		ButtonPrint(label = "blue 50", color = blue50)
		ButtonPrint(label = "blue 100", color = blue100)
		#
		ButtonPrint(label = "purple 10", color = purple10)
		ButtonPrint(label = "purple 50", color = purple50)
		ButtonPrint(label = "purple 100", color = purple100)

		# RUN WINDOW
		cmds.showWindow(self.window_name)

