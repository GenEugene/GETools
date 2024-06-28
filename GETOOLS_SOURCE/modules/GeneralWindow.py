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
from functools import partial

from ..modules import CenterOfMass
from ..modules import Overlappy
from ..modules import Rigging
from ..modules import Settings
from ..modules import Tools

from ..utils import Blendshapes
from ..utils import Colors
from ..utils import Install
from ..utils import Layers
from ..utils import MayaSettings
from ..utils import MotionTrail
from ..utils import Scene
from ..utils import Selector
from ..utils import Toggles

from ..values import Icons

class GeneralWindow:
	version = "v1.0.5"
	name = "GETools"
	title = name + " " + version

	def __init__(self):
		self.directory = ""
		self.frameTools = None
		self.frameRigging = None
		self.frameOverlappy = None
		self.frameCenterOfMass = None
		self.frameExperimental = None
	def CreateUI(self):
		if cmds.window(Settings.windowName, exists = True):
			cmds.deleteUI(Settings.windowName)
		cmds.window(Settings.windowName, title = GeneralWindow.title, maximizeButton = False, sizeable = True, widthHeight = (Settings.windowWidth, Settings.windowHeight))
		
		# layoutRoot = cmds.columnLayout(adjustableColumn = True, width = Settings.windowWidth)
		layoutRoot = cmds.menuBarLayout(width = Settings.windowWidth)
		self.LayoutMenuBar(layoutRoot)
		
		# self.LayoutTitle(layoutRoot) # TODO title

		layoutScroll = cmds.scrollLayout(parent = layoutRoot, width = Settings.windowWidth)
		self.LayoutTools(layoutScroll)
		self.LayoutRigging(layoutScroll)
		self.LayoutOverlappy(layoutScroll)
		self.LayoutCenterOfMass(layoutScroll)
		self.LayoutExperimental(layoutScroll)

	# UI LAYOUTS
	def LayoutMenuBar(self, parentLayout):
		cmds.columnLayout("layoutMenuBar", parent = parentLayout, adjustableColumn = True, width = Settings.windowWidthScroll)
		cmds.menuBarLayout()

		cmds.menu(label = "File")
		cmds.menuItem(label = "Reload Scene (force)", command = Scene.Reload, image = Icons.reset)
		cmds.menuItem(label = "Exit Maya (force)", command = Scene.ExitMaya, image = Icons.off)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Restart GETools", command = partial(self.RUN_DOCKED, "", True), image = Icons.reset)
		cmds.menuItem(label = "Close GETools", command = self.DockDelete, image = Icons.off)
		
		# cmds.menu(label = "Edit", tearOff = True)
		# cmds.menuItem(label = "Save Settings")
		# cmds.menuItem(label = "Load Settings")
		# cmds.menuItem(label = "Reset Settings")

		cmds.menu(label = "Display", tearOff = True)
		cmds.menuItem(label = "Collapse All", command = partial(self.FramesCollapse, True), image = Icons.visibleOff)
		cmds.menuItem(label = "Expand All", command = partial(self.FramesCollapse, False), image = Icons.visibleOn)
		cmds.menuItem(dividerLabel = "Docking", divider = True)
		cmds.menuItem(label = "Dock Left", command = partial(self.DockToSide, Settings.dockAllowedAreas[0]), image = Icons.arrowLeft)
		cmds.menuItem(label = "Dock Right", command = partial(self.DockToSide, Settings.dockAllowedAreas[1]), image = Icons.arrowRight)
		cmds.menuItem(label = "Undock", command = self.DockOff, image = Icons.arrowDown)

		def ColorsPalette(*args):
			colorCalibration = Colors.ColorsPalette()
			colorCalibration.CreateUI()
		def PrintChannelBoxAttributes(*args):
			print(Selector.GetChannelBoxAttributes())
		cmds.menu(label = "Utils", tearOff = True)
		cmds.menuItem(label = "Select Hiererchy", command = Selector.SelectHierarchy)
		# cmds.menuItem(label = "Create Reset Button", command = Install.CreateResetButton)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Print selected objects to console", command = Selector.PrintSelected, image = Icons.text)
		cmds.menuItem(label = "Print channel box selected attributes", command = PrintChannelBoxAttributes, image = Icons.text)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Open Colors Palette", command = ColorsPalette, image = Icons.color)
		cmds.menuItem(dividerLabel = "Blendshapes", divider = True)
		cmds.menuItem(label = "Print Blendshapes Base Nodes", command = Blendshapes.GetBlendshapeNodesFromSelected, image = Icons.text)
		cmds.menuItem(label = "Print Blendshapes Names", command = Blendshapes.GetBlendshapeWeightsFromSelected, image = Icons.text)
		
		cmds.menu(label = "Toggle", tearOff = True)
		cmds.menuItem(label = "Joints", command = Toggles.ToggleJoints, image = Icons.joint)

		self.LayoutMenuInstall()

		cmds.menu(label = "Help", tearOff = True) # , helpMenu = True
		def LinkVersionHistory(self): cmds.showHelp("https://github.com/GenEugene/GETools/blob/master/changelog.txt", absolute = True)
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/GETools", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://gumroad.com/l/iCNa", absolute = True)
		def LinkGithubWiki(self): cmds.showHelp("https://github.com/GenEugene/GETools/wiki", absolute = True)
		def LinkYoutubeTutorial(self): cmds.showHelp("", absolute = True) # TODO add new youtube link with tutorial
		def LinkLinkedin(self): cmds.showHelp("https://www.linkedin.com/in/geneugene", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True)
		def LinkDiscord(self): cmds.showHelp("https://discord.gg/heMxJhTqCz", absolute = True)
		def LinkShareIdeas(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/ideas", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/report-a-problem", absolute = True)
		
		cmds.menuItem(label = "About GETools", enable = False, image = self.directory + Icons.get) # TODO add window with information
		cmds.menuItem(label = "Version History", command = LinkVersionHistory)
		cmds.menuItem(dividerLabel = "Links", divider = True)
		cmds.menuItem(label = "GitHub", command = LinkGithub, image = Icons.home)
		cmds.menuItem(label = "Gumroad", command = LinkGumroad)
		cmds.menuItem(dividerLabel = "HOW TO USE", divider = True)
		cmds.menuItem(label = "Documentation", command = LinkGithubWiki, image = Icons.help)
		cmds.menuItem(label = "Tutorial Video", enable = False, command = LinkYoutubeTutorial, image = Icons.playblast)
		cmds.menuItem(dividerLabel = "Contacts", divider = True)
		cmds.menuItem(label = "Linkedin", command = LinkLinkedin)
		cmds.menuItem(label = "YouTube", command = LinkYoutube)
		cmds.menuItem(label = "Discord", command = LinkDiscord)
		cmds.menuItem(dividerLabel = "Support", divider = True)
		cmds.menuItem(label = "Share your Ideas", command = LinkShareIdeas, image = Icons.light)
		cmds.menuItem(label = "Report a Problem", command = LinkReport, image = Icons.warning)

		# DEV ZONE
		def LayerCreate(*args):
			Layers.Create("testLayer")
		def LayerCreateForSelected(*args):
			selected = Selector.MultipleObjects()
			if (selected == None):
				return
			Layers.CreateForSelected(selected)
		def LayerDelete(*args):
			Layers.Delete("testLayer")
		def LayerGetSelected(*args):
			Layers.GetSelected()
		def LayerMove(*args):
			selected = Layers.GetSelected()
			if (selected == None or len(selected) < 2):
				cmds.warning("Need to select at least 2 layers")
				return
			Layers.MoveChildrenToParent(selected[:-1], selected[-1]) # FIXME main problem is layers have no selection order, they just listed from top to bottom

		# cmds.menu(label = "---", enable = False)
		# cmds.menu(label = "DEV", tearOff = True)
		# cmds.menuItem(dividerLabel = "Layers", divider = True)
		# cmds.menuItem(label = "Layer Create", command = LayerCreate)
		# cmds.menuItem(label = "Layer Create For Selected", command = LayerCreateForSelected)
		# cmds.menuItem(label = "Layer Delete", command = LayerDelete)
		# cmds.menuItem(label = "Layer Get Selected", command = LayerGetSelected)
		# cmds.menuItem(label = "Layer Move", command = LayerMove)
		pass
	def LayoutMenuInstall(self):
		cmds.menu(label = "To Shelf", tearOff = True)
		###
		cmds.menuItem(subMenu = True, label = "General", tearOff = True, image = Icons.fileOpen)
		cmds.menuItem(dividerLabel = "File", divider = True)
		cmds.menuItem(label = "Reload Scene (force)", command = partial(Install.ToShelf_ReloadScene, self.directory))
		cmds.menuItem(label = "Exit Maya (force)", command = partial(Install.ToShelf_ExitMaya, self.directory))
		cmds.menuItem(dividerLabel = "Utils", divider = True)
		cmds.menuItem(label = "Select Hiererchy", command = partial(Install.ToShelf_SelectHierarchy, self.directory))
		# cmds.menuItem(label = "Create Reset Button", command = partial(Install.ToShelf_CreateResetButton, self.directory), image = Icons.reset)
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOGGLE", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Size", tearOff = True)
		cmds.menuItem(label = "Joints", command = partial(Install.ToShelf_ToggleJoints, self.directory), image = Icons.joint)
		# cmds.menuItem(label = "Meshes", command = partial(Install.ToShelf_ToggleJoints, self.directory))
		# cmds.menuItem(label = "Nurbs", command = partial(Install.ToShelf_ToggleJoints, self.directory))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Locators", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Size", tearOff = True)
		cmds.menuItem(label = "50%", command = partial(Install.ToShelf_LocatorsSizeScale50, self.directory))
		cmds.menuItem(label = "90%", command = partial(Install.ToShelf_LocatorsSizeScale90, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "110%", command = partial(Install.ToShelf_LocatorsSizeScale110, self.directory))
		cmds.menuItem(label = "200%", command = partial(Install.ToShelf_LocatorsSizeScale200, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Create", tearOff = True, image = Icons.locator)
		cmds.menuItem(label = "Locator", command = partial(Install.ToShelf_LocatorCreate, self.directory))
		cmds.menuItem(label = "Match", command = partial(Install.ToShelf_LocatorsMatch, self.directory))
		cmds.menuItem(label = "Parent", command = partial(Install.ToShelf_LocatorsParent, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Pin", tearOff = True, image = Icons.pin)
		cmds.menuItem(label = "Pin", command = partial(Install.ToShelf_LocatorsPin, self.directory))
		cmds.menuItem(label = "Without reverse constraint", command = partial(Install.ToShelf_LocatorsPinWithoutReverse, self.directory))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_LocatorsPinPos, self.directory))
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_LocatorsPinRot, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Relative", tearOff = True, image = Icons.pinInvert)
		cmds.menuItem(label = "Relative", command = partial(Install.ToShelf_LocatorsRelative, self.directory))
		cmds.menuItem(label = "Skip last object reverse constraint", command = partial(Install.ToShelf_LocatorsRelativeSkipLast, self.directory))
		cmds.menuItem(label = "Without reverse constraint", command = partial(Install.ToShelf_LocatorsRelativeWithoutReverse, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Aim", tearOff = True, image = Icons.pin)
		minus = "-"
		plus = "+"
		axisX = "X"
		axisY = "Y"
		axisZ = "Z"
		axisXMinus = minus + axisX
		axisYMinus = minus + axisY
		axisZMinus = minus + axisZ
		axisXPlus = plus + axisX
		axisYPlus = plus + axisY
		axisZPlus = plus + axisZ
		cmds.menuItem(dividerLabel = "All", divider = True)
		cmds.menuItem(label = axisXMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXMinus, False, (-1, 0, 0)))
		cmds.menuItem(label = axisXPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXPlus, False, (1, 0, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisYMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYMinus, False, (0, -1, 0)))
		cmds.menuItem(label = axisYPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYPlus, False, (0, 1, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisZMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZMinus, False, (0, 0, -1)))
		cmds.menuItem(label = axisZPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZPlus, False, (0, 0, 1)))
		cmds.menuItem(dividerLabel = "Rotation", divider = True)
		cmds.menuItem(label = axisXMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXMinus, True, (-1, 0, 0)))
		cmds.menuItem(label = axisXPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisXPlus, True, (1, 0, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisYMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYMinus, True, (0, -1, 0)))
		cmds.menuItem(label = axisYPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisYPlus, True, (0, 1, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisZMinus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZMinus, True, (0, 0, -1)))
		cmds.menuItem(label = axisZPlus, command = partial(Install.ToShelf_LocatorsAim, self.directory, axisZPlus, True, (0, 0, 1)))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Baking", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Bake", tearOff = True)
		cmds.menuItem(label = "Classic", command = partial(Install.ToShelf_BakeClassic, self.directory))
		cmds.menuItem(label = "Classic Cut Out", command = partial(Install.ToShelf_BakeClassicCutOut, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Custom", command = partial(Install.ToShelf_BakeCustom, self.directory))
		cmds.menuItem(label = "Custom Cut Out", command = partial(Install.ToShelf_BakeCustomCutOut, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "By Last", tearOff = True)
		cmds.menuItem(label = "By Last", command = partial(Install.ToShelf_BakeByLast, self.directory, True, True))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_BakeByLast, self.directory, True, False))
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_BakeByLast, self.directory, False, True))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "World", tearOff = True, image = Icons.world)
		cmds.menuItem(label = "World", command = partial(Install.ToShelf_BakeByWorld, self.directory, True, True))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_BakeByWorld, self.directory, True, False))
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_BakeByWorld, self.directory, False, True))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Animation", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Delete", tearOff = True, image = Icons.delete)
		cmds.menuItem(label = "Animation", command = partial(Install.ToShelf_DeleteKeys, self.directory))
		cmds.menuItem(label = "Nonkeyable", command = partial(Install.ToShelf_DeleteNonkeyable, self.directory))
		cmds.menuItem(label = "Static", command = partial(Install.ToShelf_DeleteStatic, self.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(label = "Euler Filter", command = partial(Install.ToShelf_EulerFilter, self.directory), image = Icons.filter)
		#
		cmds.menuItem(subMenu = True, label = "Infinity", tearOff = True)
		cmds.menuItem(label = "Constant", command = partial(Install.ToShelf_SetInfinity, self.directory, 1))
		cmds.menuItem(label = "Linear", command = partial(Install.ToShelf_SetInfinity, self.directory, 2))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Cycle", command = partial(Install.ToShelf_SetInfinity, self.directory, 3))
		cmds.menuItem(label = "Offset", command = partial(Install.ToShelf_SetInfinity, self.directory, 4))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Oscillate", command = partial(Install.ToShelf_SetInfinity, self.directory, 5))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Offset", tearOff = True)
		cmds.menuItem(label = "-3", command = partial(Install.ToShelf_AnimOffset, self.directory, -1, 3))
		cmds.menuItem(label = "-2", command = partial(Install.ToShelf_AnimOffset, self.directory, -1, 2))
		cmds.menuItem(label = "-1", command = partial(Install.ToShelf_AnimOffset, self.directory, -1, 1))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "+1", command = partial(Install.ToShelf_AnimOffset, self.directory, 1, 1))
		cmds.menuItem(label = "+2", command = partial(Install.ToShelf_AnimOffset, self.directory, 1, 2))
		cmds.menuItem(label = "+3", command = partial(Install.ToShelf_AnimOffset, self.directory, 1, 3))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Timeline", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Timeline", tearOff = True)
		cmds.menuItem(label = "Min Out", command = partial(Install.ToShelf_SetTimelineMinOut, self.directory))
		cmds.menuItem(label = "Min In", command = partial(Install.ToShelf_SetTimelineMinIn, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Max In", command = partial(Install.ToShelf_SetTimelineMaxIn, self.directory))
		cmds.menuItem(label = "Max Out", command = partial(Install.ToShelf_SetTimelineMaxOut, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Expand Out", command = partial(Install.ToShelf_SetTimelineExpandOut, self.directory))
		cmds.menuItem(label = "Expand In", command = partial(Install.ToShelf_SetTimelineExpandIn, self.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Selected Range", command = partial(Install.ToShelf_SetTimelineSet, self.directory))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "RIGGING - Constraints", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Constraints", tearOff = True, image = Icons.constraint)
		cmds.menuItem(label = "Parent", command = partial(Install.ToShelf_Constraint, self.directory, False, True, False, False, False))
		cmds.menuItem(label = "Point", command = partial(Install.ToShelf_Constraint, self.directory, False, False, True, False, False))
		cmds.menuItem(label = "Orient", command = partial(Install.ToShelf_Constraint, self.directory, False, False, False, True, False))
		cmds.menuItem(label = "Scale", command = partial(Install.ToShelf_Constraint, self.directory, False, False, False, False, True))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Parent with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, True, False, False, False))
		cmds.menuItem(label = "Point with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, False, True, False, False))
		cmds.menuItem(label = "Orient with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, False, False, True, False))
		cmds.menuItem(label = "Scale with maintain", command = partial(Install.ToShelf_Constraint, self.directory, True, False, False, False, True))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Connections", tearOff = True, image = Icons.constraint)
		cmds.menuItem(label = "Disconnect", command = partial(Install.ToShelf_DisconnectTargets, self.directory))
		cmds.menuItem(label = "Delete Constraints", command = partial(Install.ToShelf_DeleteConstraints, self.directory))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "RIGGING - Utils", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Rotate Order", tearOff = True)
		cmds.menuItem(label = "Show", command = partial(Install.ToShelf_RotateOrder, self.directory, True), image = Icons.visibleOn)
		cmds.menuItem(label = "Hide", command = partial(Install.ToShelf_RotateOrder, self.directory, False), image = Icons.visibleOff)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Segment Scale Compensate", tearOff = True, image = Icons.joint)
		cmds.menuItem(label = "On", command = partial(Install.ToShelf_SegmentScaleCompensate, self.directory, True), image = Icons.on)
		cmds.menuItem(label = "Off", command = partial(Install.ToShelf_SegmentScaleCompensate, self.directory, False), image = Icons.off)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Joint Draw Style", tearOff = True, image = Icons.joint)
		cmds.menuItem(label = "Bone", command = partial(Install.ToShelf_JointDrawStyle, self.directory, 0), image = Icons.visibleOn)
		cmds.menuItem(label = "Hidden", command = partial(Install.ToShelf_JointDrawStyle, self.directory, 2), image = Icons.visibleOff)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(label = "Copy Skin Weights From Last Selected", command = partial(Install.ToShelf_CopySkin, self.directory), image = Icons.copy)
		
		cmds.menuItem(dividerLabel = "RIGGING - Blendshapes", divider = True)
		###
		# cmds.menuItem(subMenu = True, label = "Rotate Order", tearOff = True)
		cmds.menuItem(label = "Wraps Create", command = partial(Install.ToShelf_WrapsCreate, self.directory), image = Icons.wrap)
		# cmds.menuItem(label = "Wraps Convert", command = partial(Install.ToShelf_WrapsCreate, self.directory), image = Icons.wrap) # TODO
		cmds.menuItem(label = "Reconstruct", command = partial(Install.ToShelf_BlendshapesReconstruct, self.directory), image = Icons.blendshape)
		cmds.menuItem(label = "Zero Weights", command = partial(Install.ToShelf_BlendshapesZeroWeights, self.directory), image = Icons.blendshape)
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "EXPERIMENTAL", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Motion Trail", tearOff = True)
		cmds.menuItem(label = "Create", command = partial(Install.ToShelf_MotionTrailCreate, self.directory))
		cmds.menuItem(label = "Select", command = partial(Install.ToShelf_MotionTrailSelect, self.directory))
		cmds.menuItem(label = "Delete", command = partial(Install.ToShelf_MotionTrailDelete, self.directory))
		cmds.setParent('..', menu = True)
		#

	def LayoutTitle(self, parentLayout): # TODO figure out how to use resizeable images
		cmds.columnLayout("layoutTitle", parent = parentLayout, adjustableColumn = False)
		size = 30
		cmds.iconTextButton(label = "GETOOLS", style = "iconAndTextHorizontal", image = self.directory + Icons.get, width = size, height = size)
		# cmds.image(image = self.directory + Icons.get, width = size, height = size)

	def LayoutTools(self, parentLayout):
		self.frameTools = cmds.frameLayout("layoutTools", parent = parentLayout, label = "1. " + Tools.Tools.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		Tools.Tools().UICreate(self.frameTools)
	def LayoutRigging(self, parentLayout):
		self.frameRigging = cmds.frameLayout("layoutRigging", parent = parentLayout, label = "2. " + Rigging.Rigging.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		Rigging.Rigging().UICreate(self.frameRigging)
	def LayoutOverlappy(self, parentLayout):
		self.frameOverlappy = cmds.frameLayout("layoutOverlappy", parent = parentLayout, label = "3. " + Overlappy.Overlappy.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		Overlappy.Overlappy().UICreate(self.frameOverlappy)
	def LayoutCenterOfMass(self, parentLayout):
		self.frameCenterOfMass = cmds.frameLayout("layoutCenterOfMass", parent = parentLayout, label = "4. " + CenterOfMass.CenterOfMass.title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		CenterOfMass.CenterOfMass().UICreate(self.frameCenterOfMass)
	def LayoutExperimental(self, parentLayout):
		self.frameExperimental = cmds.frameLayout("layoutExperimental", parent = parentLayout, label = "5. " + "EXPERIMENTAL", collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = Settings.margin, marginHeight = Settings.margin)
		cmds.popupMenu()
		cmds.menuItem(label = "Right-Click test")
		
		countOffsets = 3
		cmds.gridLayout(numberOfColumns = countOffsets, cellWidth = Settings.windowWidthMargin / countOffsets, cellHeight = Settings.lineHeight)

		cmds.button(label = "Trails Create", command = MotionTrail.Create, backgroundColor = Colors.orange10)
		cmds.button(label = "Trails Select", command = MotionTrail.Select, backgroundColor = Colors.orange50)
		cmds.button(label = "Trails Delete", command = MotionTrail.Delete, backgroundColor = Colors.orange100)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Select", command = MotionTrail.Select)
		# cmds.menuItem(label = "Delete", command = MotionTrail.Delete)
		pass

	# WINDOW
	def WindowCheck(self, *args):
		return cmds.window(Settings.windowName, exists = True)
	def WindowShow(self, *args):
		if self.WindowCheck():
			cmds.showWindow(Settings.windowName)
			print("Window showed")
		else:
			print("No Window")
	def WindowHide(self, *args):
		if self.WindowCheck():
			cmds.window(Settings.windowName, edit = True, visible = False)
			print("Window hidden")
		else:
			print("No Window")
	def WindowDelete(self, *args):
		if self.WindowCheck():
			cmds.deleteUI(Settings.windowName)
			print("Window deleted")
		else:
			print("No Window")
	def FramesCollapse(self, value, *args): # TODO collapse function for sub frames
		if (self.frameTools != None):
			cmds.frameLayout(self.frameTools, edit = True, collapse = value)
		if (self.frameRigging != None):
			cmds.frameLayout(self.frameRigging, edit = True, collapse = value)
		if (self.frameOverlappy != None):
			cmds.frameLayout(self.frameOverlappy, edit = True, collapse = value)
		if (self.frameCenterOfMass != None):
			cmds.frameLayout(self.frameCenterOfMass, edit = True, collapse = value)
		if (self.frameExperimental != None):
			cmds.frameLayout(self.frameExperimental, edit = True, collapse = value)

	# DOCKING
	def DockCheckVisible(self, *args):
		return cmds.dockControl(Settings.dockName, query = True, visible = True)
	def DockCheck(self, *args):
		return cmds.dockControl(Settings.dockName, query = True, exists = True)
	def DockDelete(self, *args):
		if self.DockCheck():
			cmds.deleteUI(Settings.dockName, control = True)
			# print("Dock Control deleted")
		# else:
		# 	print("No Dock")
		pass
	def DockOff(self, *args):
		if self.DockCheck():
			cmds.dockControl(Settings.dockName, edit = True, floating = True, height = Settings.windowHeight)
			print("{0} undocked".format(GeneralWindow.title))
		else:
			cmds.warning("Dock Controls wasn't found")
	def DockToSide(self, areaSide, *args):
		if self.DockCheck():
			cmds.dockControl(Settings.dockName, edit = True, floating = False, area = areaSide)
		else:
			cmds.dockControl(Settings.dockName, label = GeneralWindow.title, content = Settings.windowName, area = areaSide, allowedArea = Settings.dockAllowedAreas) # , backgroundColor = Colors.lightBlue10
		print("{0} docked to {1}".format(GeneralWindow.title, areaSide))

	# EXECUTION
	def WindowCreate(self, *args):
		self.CreateUI()
		self.FramesCollapse(True)
	def RUN_DOCKED(self, path="", forced=False, *args):
		self.directory = path

		if (not forced and self.DockCheck()): # for script toggling. Comment these 3 lines if you need to deactivate toggling
			if (self.DockCheckVisible()):
				self.DockDelete()
				print("{0} closed".format(GeneralWindow.title))
				return

		self.DockDelete()
		self.WindowCreate()
		self.DockToSide(Settings.dockStartArea)

		MayaSettings.HelpPopupActivate()
		MayaSettings.CachedPlaybackDeactivate()

