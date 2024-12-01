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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import maya.cmds as cmds
from functools import partial

from .. import Settings
from ..modules import Options
from ..modules import Tools
from ..modules import Rigging
from ..modules import Overlappy
from ..modules import CenterOfMass
from ..modules import Experimental
from ..utils import Annotation
from ..utils import Blendshapes
from ..utils import Colors
from ..utils import Install
from ..utils import MayaSettings
from ..utils import MotionTrail
from ..utils import Parent
from ..utils import Print
from ..utils import Scene
from ..utils import Selector
from ..utils import Shelf
from ..utils import Skinning
from ..utils import Toggles
from ..utils import UI
from ..values import Icons


class GeneralWindow:
	_version = "v1.5.1"
	_name = "GETools"
	_title = _name + " " + _version

	def __init__(self):
		self.optionsPlugin = Options.PluginVariables()
		self.optionsPlugin.titleGeneral = GeneralWindow._title

		self.frameTools = None
		self.frameRigging = None
		self.frameOverlappy = None
		self.frameCenterOfMass = None
		self.frameMotionTrail = None
		self.frameExperimental = None
	def CreateUI(self):
		if cmds.window(Settings.windowName, exists = True):
			cmds.deleteUI(Settings.windowName)
		generalWindow = cmds.window(Settings.windowName, title = GeneralWindow._title, maximizeButton = False, sizeable = True, width = Settings.windowWidth, height = Settings.windowHeight)
		
		layoutRoot = cmds.menuBarLayout(parent = generalWindow)
		self.LayoutMenuBar(parentLayout = layoutRoot)

		layoutScroll = cmds.scrollLayout(parent = generalWindow)

		self.LayoutTools(parentLayout = layoutScroll)
		self.LayoutRigging(parentLayout = layoutScroll)
		self.LayoutOverlappy(parentLayout = layoutScroll)
		self.LayoutCenterOfMass(parentLayout = layoutScroll)
		self.LayoutMotionTrail(parentLayout = layoutScroll)
		self.LayoutExperimental(parentLayout = layoutScroll)

	### UI LAYOUTS
	def LayoutMenuBar(self, parentLayout):
		cmds.columnLayout("layoutMenuBar", parent = parentLayout, adjustableColumn = True, width = Settings.windowWidth)
		cmds.menuBarLayout()

		cmds.menu(label = "File")
		cmds.menuItem(label = "Reload Scene (force)", command = Scene.Reload, image = Icons.reset)
		cmds.menuItem(label = "Exit Maya (force)", command = Scene.ExitMaya, image = Icons.off)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Restart GETools", command = partial(self.RUN_DOCKED, self.optionsPlugin.directory, True), image = Icons.reset)
		cmds.menuItem(label = "Close GETools", command = self.DockDelete, image = Icons.off)
		
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
		cmds.menu(label = "Utils", tearOff = True)
		cmds.menuItem(label = "Select Hiererchy", command = Selector.SelectHierarchy, image = Icons.selectByHierarchy)
		cmds.menuItem(label = "Select Hiererchy Transforms", command = Selector.SelectHierarchyTransforms, image = Icons.selectByHierarchy)
		cmds.menuItem(label = "Select Skinned Meshes Or Joints", command = Skinning.SelectSkinnedMeshesOrJoints)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Save Pose To Shelf", command = Install.CreatePoseButton)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Parent Shapes", command = Parent.ParentShape)
		cmds.menuItem(label = "Annotate Selected", command = Annotation.AnnotateSelected)
		cmds.menuItem(dividerLabel = "Prints", divider = True)
		cmds.menuItem(label = "Print Selected Objects To Console", command = Print.PrintSelected, image = Icons.text)
		cmds.menuItem(label = "Print Animatable Attributes", command = partial(Print.PrintAttributesAnimatableOnSelected, False), image = Icons.text)
		# cmds.menuItem(label = "Print Animatable Attributes With Shapes", command = partial(Print.PrintAttributesAnimatableOnSelected, True), image = Icons.text) # FIXME
		cmds.menuItem(label = "Print Channel Box Selected Attributes", command = Print.PrintAttributesSelectedFromChannelBox, image = Icons.text)
		cmds.menuItem(dividerLabel = "Blendshapes", divider = True)
		cmds.menuItem(label = "Print Blendshapes Base Nodes", command = Blendshapes.GetBlendshapeNodesFromSelected, image = Icons.text)
		cmds.menuItem(label = "Print Blendshapes Names", command = Blendshapes.GetBlendshapeWeightsFromSelected, image = Icons.text)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Open Colors Palette", command = ColorsPalette, image = Icons.color)
		
		cmds.menu(label = "Toggle", tearOff = True)
		# cmds.menuItem(label = "All Objects", command = Toggles.ToggleAllObjects)
		cmds.menuItem(label = "Cameras", command = Toggles.ToggleCameras, image = Icons.camera)
		cmds.menuItem(label = "Control Vertices", command = Toggles.ToggleControlVertices, image = Icons.vertex)
		cmds.menuItem(label = "Deformers", command = Toggles.ToggleDeformers)
		cmds.menuItem(label = "Dimensions", command = Toggles.ToggleDimensions)
		cmds.menuItem(label = "Dynamic Constraints", command = Toggles.ToggleDynamicConstraints, image = Icons.dynamicConstraint)
		cmds.menuItem(label = "Dynamics", command = Toggles.ToggleDynamics)
		cmds.menuItem(label = "Fluids", command = Toggles.ToggleFluids)
		cmds.menuItem(label = "Follicles", command = Toggles.ToggleFollicles, image = Icons.follicle)
		cmds.menuItem(label = "Grid", command = Toggles.ToggleGrid, image = Icons.grid)
		cmds.menuItem(label = "Hair Systems", command = Toggles.ToggleHairSystems, image = Icons.hairSystem)
		cmds.menuItem(label = "Handles", command = Toggles.ToggleHandles)
		cmds.menuItem(label = "Hulls", command = Toggles.ToggleHulls)
		cmds.menuItem(label = "IK Handles", command = Toggles.ToggleIkHandles, image = Icons.ikHandle)
		cmds.menuItem(label = "Joints", command = Toggles.ToggleJoints, image = Icons.joint)
		cmds.menuItem(label = "Lights", command = Toggles.ToggleLights, image = Icons.light)
		cmds.menuItem(label = "Locators", command = Toggles.ToggleLocators, image = Icons.locator)
		cmds.menuItem(label = "Manipulators", command = Toggles.ToggleManipulators, image = Icons.manipulator)
		cmds.menuItem(label = "NCloths", command = Toggles.ToggleNCloths, image = Icons.nCloth)
		cmds.menuItem(label = "NParticles", command = Toggles.ToggleNParticles, image = Icons.particle)
		cmds.menuItem(label = "NRigids", command = Toggles.ToggleNRigids, image = Icons.nRigid)
		cmds.menuItem(label = "Nurbs Curves", command = Toggles.ToggleNurbsCurves, image = Icons.nurbsCurve)
		cmds.menuItem(label = "Nurbs Surfaces", command = Toggles.ToggleNurbsSurfaces, image = Icons.nurbsSurface)
		cmds.menuItem(label = "Pivots", command = Toggles.TogglePivots)
		cmds.menuItem(label = "Planes", command = Toggles.TogglePlanes, image = Icons.plane)
		cmds.menuItem(label = "Poly Meshes", command = Toggles.TogglePolymeshes, image = Icons.polyMesh)
		cmds.menuItem(label = "Shadows", command = Toggles.ToggleShadows, image = Icons.shadows)
		cmds.menuItem(label = "Strokes", command = Toggles.ToggleStrokes, image = Icons.stroke)
		cmds.menuItem(label = "Subdiv Surfaces", command = Toggles.ToggleSubdivSurfaces)
		cmds.menuItem(label = "Textures", command = Toggles.ToggleTextures, image = Icons.image)

		self.LayoutMenuOptions()

		cmds.menu(label = "Help", tearOff = True) # , helpMenu = True
		def LinkVersionHistory(self): cmds.showHelp("https://github.com/GenEugene/GETools/blob/master/changelog.txt", absolute = True)
		def LinkGithub(self): cmds.showHelp("https://github.com/GenEugene/GETools", absolute = True)
		def LinkGumroad(self): cmds.showHelp("https://gumroad.com/l/iCNa", absolute = True)
		def LinkGithubWiki(self): cmds.showHelp("https://github.com/GenEugene/GETools/wiki", absolute = True)
		def LinkYoutubeVideos(self): cmds.showHelp("https://youtube.com/playlist?list=PLhwndaM4LAxhbl95yz9WVie1iYflTFy6S&si=UOoK-mdk4Rm5bVyp", absolute = True)
		def LinkLinkedin(self): cmds.showHelp("https://www.linkedin.com/in/geneugene", absolute = True)
		def LinkYoutube(self): cmds.showHelp("https://youtube.com/@EugeneGataulin", absolute = True)
		def LinkDiscord(self): cmds.showHelp("https://discord.gg/heMxJhTqCz", absolute = True)
		def LinkShareIdeas(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/ideas", absolute = True)
		def LinkReport(self): cmds.showHelp("https://github.com/GenEugene/GETools/discussions/categories/report-a-problem", absolute = True)
		
		# cmds.menuItem(label = "About GETools", enable = False, image = self.options.directory + Icons.get1[0]) # TODO add window with information
		cmds.menuItem(label = "Version History", command = LinkVersionHistory)
		cmds.menuItem(dividerLabel = "Links", divider = True)
		cmds.menuItem(label = "GitHub", command = LinkGithub, image = Icons.home)
		cmds.menuItem(label = "Gumroad", command = LinkGumroad)
		cmds.menuItem(dividerLabel = "HOW TO USE", divider = True)
		cmds.menuItem(label = "Documentation", command = LinkGithubWiki, image = Icons.help)
		cmds.menuItem(label = "Videos Playlist", command = LinkYoutubeVideos, image = Icons.playblast)
		cmds.menuItem(dividerLabel = "Contacts", divider = True)
		cmds.menuItem(label = "Discord", command = LinkDiscord)
		cmds.menuItem(label = "Linkedin", command = LinkLinkedin)
		cmds.menuItem(label = "YouTube", command = LinkYoutube)
		cmds.menuItem(dividerLabel = "Support", divider = True)
		cmds.menuItem(label = "Share Your Ideas", command = LinkShareIdeas, image = Icons.light)
		cmds.menuItem(label = "Report a Problem", command = LinkReport, image = Icons.warning)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Change Icon", command = partial(Shelf.ToggleButtonIcons, self.optionsPlugin.directory))
	def LayoutMenuOptions(self):
		cmds.menu(label = "Options", tearOff = True)

		self.optionsPlugin.menuCheckboxEulerFilter = UI.MenuCheckbox(label = "Euler Filter After Baking", value = Settings.checkboxEulerFilter, valueDefault = Settings.checkboxEulerFilter)

		cmds.menuItem(dividerLabel = "Install", divider = True)

		# Install
		cmds.menuItem(subMenu = True, label = "Install Buttons To Current Shelf", tearOff = True, image = Icons.fileOpen)
		cmds.menuItem(subMenu = True, label = "File", tearOff = True, image = Icons.fileOpen)
		cmds.menuItem(label = "Reload Scene (force)", command = partial(Install.ToShelf_ReloadScene, self.optionsPlugin.directory), image = Icons.reset)
		cmds.menuItem(label = "Exit Maya (force)", command = partial(Install.ToShelf_ExitMaya, self.optionsPlugin.directory), image = Icons.off)
		cmds.setParent('..', menu = True)

		cmds.menuItem(subMenu = True, label = "Utils", tearOff = True)
		cmds.menuItem(label = "Select Hiererchy", command = partial(Install.ToShelf_SelectHierarchy, self.optionsPlugin.directory), image = Icons.selectByHierarchy)
		cmds.menuItem(label = "Select Hiererchy Transforms", command = partial(Install.ToShelf_SelectHierarchyTransforms, self.optionsPlugin.directory), image = Icons.selectByHierarchy)
		cmds.menuItem(label = "Select Skinned Meshes Or Joints", command = partial(Install.ToShelf_SelectSkinnedMeshesOrJoints, self.optionsPlugin.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Save Pose To Shelf", command = partial(Install.ToShelf_SavePoseToShelf, self.optionsPlugin.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Parent Shapes", command = partial(Install.ToShelf_ParentShapes, self.optionsPlugin.directory))
		cmds.menuItem(label = "Annotate Selected", command = partial(Install.ToShelf_AnnotateSelected, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(subMenu = True, label = "Toggle", tearOff = True)
		# cmds.menuItem(label = "All Objects", command = partial(Install.ToShelf_ToggleAllObjects, self.options.directory))
		cmds.menuItem(label = "Cameras", command = partial(Install.ToShelf_ToggleCameras, self.optionsPlugin.directory), image = Icons.camera)
		cmds.menuItem(label = "Control Vertices", command = partial(Install.ToShelf_ToggleControlVertices, self.optionsPlugin.directory), image = Icons.vertex)
		cmds.menuItem(label = "Deformers", command = partial(Install.ToShelf_ToggleDeformers, self.optionsPlugin.directory))
		cmds.menuItem(label = "Dimensions", command = partial(Install.ToShelf_ToggleDimensions, self.optionsPlugin.directory))
		cmds.menuItem(label = "Dynamic Constraints", command = partial(Install.ToShelf_ToggleDynamicConstraints, self.optionsPlugin.directory), image = Icons.dynamicConstraint)
		cmds.menuItem(label = "Dynamics", command = partial(Install.ToShelf_ToggleDynamics, self.optionsPlugin.directory))
		cmds.menuItem(label = "Fluids", command = partial(Install.ToShelf_ToggleFluids, self.optionsPlugin.directory))
		cmds.menuItem(label = "Follicles", command = partial(Install.ToShelf_ToggleFollicles, self.optionsPlugin.directory), image = Icons.follicle)
		cmds.menuItem(label = "Grid", command = partial(Install.ToShelf_ToggleGrid, self.optionsPlugin.directory), image = Icons.grid)
		cmds.menuItem(label = "Hair Systems", command = partial(Install.ToShelf_ToggleHairSystems, self.optionsPlugin.directory), image = Icons.hairSystem)
		cmds.menuItem(label = "Handles", command = partial(Install.ToShelf_ToggleHandles, self.optionsPlugin.directory))
		cmds.menuItem(label = "Hulls", command = partial(Install.ToShelf_ToggleHulls, self.optionsPlugin.directory))
		cmds.menuItem(label = "IK Handles", command = partial(Install.ToShelf_ToggleIkHandles, self.optionsPlugin.directory), image = Icons.ikHandle)
		cmds.menuItem(label = "Joints", command = partial(Install.ToShelf_ToggleJoints, self.optionsPlugin.directory), image = Icons.joint)
		cmds.menuItem(label = "Lights", command = partial(Install.ToShelf_ToggleLights, self.optionsPlugin.directory), image = Icons.light)
		cmds.menuItem(label = "Locators", command = partial(Install.ToShelf_ToggleLocators, self.optionsPlugin.directory), image = Icons.locator)
		cmds.menuItem(label = "Manipulators", command = partial(Install.ToShelf_ToggleManipulators, self.optionsPlugin.directory), image = Icons.manipulator)
		cmds.menuItem(label = "NCloths", command = partial(Install.ToShelf_ToggleNCloths, self.optionsPlugin.directory), image = Icons.nCloth)
		cmds.menuItem(label = "NParticles", command = partial(Install.ToShelf_ToggleNParticles, self.optionsPlugin.directory), image = Icons.particle)
		cmds.menuItem(label = "NRigids", command = partial(Install.ToShelf_ToggleNRigids, self.optionsPlugin.directory), image = Icons.nRigid)
		cmds.menuItem(label = "Nurbs Curves", command = partial(Install.ToShelf_ToggleNurbsCurves, self.optionsPlugin.directory), image = Icons.nurbsCurve)
		cmds.menuItem(label = "Nurbs Surfaces", command = partial(Install.ToShelf_ToggleNurbsSurfaces, self.optionsPlugin.directory), image = Icons.nurbsSurface)
		cmds.menuItem(label = "Pivots", command = partial(Install.ToShelf_TogglePivots, self.optionsPlugin.directory))
		cmds.menuItem(label = "Planes", command = partial(Install.ToShelf_TogglePlanes, self.optionsPlugin.directory), image = Icons.plane)
		cmds.menuItem(label = "Poly Meshes", command = partial(Install.ToShelf_TogglePolymeshes, self.optionsPlugin.directory), image = Icons.polyMesh)
		cmds.menuItem(label = "Shadows", command = partial(Install.ToShelf_ToggleShadows, self.optionsPlugin.directory), image = Icons.shadows)
		cmds.menuItem(label = "Strokes", command = partial(Install.ToShelf_ToggleStrokes, self.optionsPlugin.directory), image = Icons.stroke)
		cmds.menuItem(label = "Subdiv Surfaces", command = partial(Install.ToShelf_ToggleSubdivSurfaces, self.optionsPlugin.directory))
		cmds.menuItem(label = "Textures", command = partial(Install.ToShelf_ToggleTextures, self.optionsPlugin.directory), image = Icons.image)
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Locators", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Size", tearOff = True, image = Icons.scale)
		cmds.menuItem(label = "50%", command = partial(Install.ToShelf_LocatorsSizeScale50, self.optionsPlugin.directory), image = Icons.minus)
		cmds.menuItem(label = "90%", command = partial(Install.ToShelf_LocatorsSizeScale90, self.optionsPlugin.directory), image = Icons.minus)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "110%", command = partial(Install.ToShelf_LocatorsSizeScale110, self.optionsPlugin.directory), image = Icons.plus)
		cmds.menuItem(label = "200%", command = partial(Install.ToShelf_LocatorsSizeScale200, self.optionsPlugin.directory), image = Icons.plus)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Create", tearOff = True, image = Icons.locator)
		cmds.menuItem(label = "Locator", command = partial(Install.ToShelf_LocatorCreate, self.optionsPlugin.directory))
		cmds.menuItem(label = "Match", command = partial(Install.ToShelf_LocatorsMatch, self.optionsPlugin.directory))
		cmds.menuItem(label = "Parent", command = partial(Install.ToShelf_LocatorsParent, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Pin", tearOff = True, image = Icons.pin)
		cmds.menuItem(label = "Pin", command = partial(Install.ToShelf_LocatorsPin, self.optionsPlugin.directory))
		cmds.menuItem(label = "Without Reverse Constraint", command = partial(Install.ToShelf_LocatorsPinWithoutReverse, self.optionsPlugin.directory))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_LocatorsPinPos, self.optionsPlugin.directory), image = Icons.move)
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_LocatorsPinRot, self.optionsPlugin.directory), image = Icons.rotate)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Relative", tearOff = True, image = Icons.pinInvert)
		cmds.menuItem(label = "Relative", command = partial(Install.ToShelf_LocatorsRelative, self.optionsPlugin.directory))
		cmds.menuItem(label = "Skip Last Object Reverse Constraint", command = partial(Install.ToShelf_LocatorsRelativeSkipLast, self.optionsPlugin.directory))
		cmds.menuItem(label = "Without Reverse Constraint", command = partial(Install.ToShelf_LocatorsRelativeWithoutReverse, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Chain Distribution", tearOff = True, image = Icons.pinInvert)
		cmds.menuItem(label = "Default Mode", command = partial(Install.ToShelf_LocatorsChainDistribution1, self.optionsPlugin.directory))
		cmds.menuItem(label = "Alternative Mode", command = partial(Install.ToShelf_LocatorsChainDistribution2, self.optionsPlugin.directory))
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
		cmds.menuItem(label = axisXMinus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisXMinus, False, (-1, 0, 0)))
		cmds.menuItem(label = axisXPlus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisXPlus, False, (1, 0, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisYMinus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisYMinus, False, (0, -1, 0)))
		cmds.menuItem(label = axisYPlus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisYPlus, False, (0, 1, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisZMinus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisZMinus, False, (0, 0, -1)))
		cmds.menuItem(label = axisZPlus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisZPlus, False, (0, 0, 1)))
		cmds.menuItem(dividerLabel = "Rotation", divider = True)
		cmds.menuItem(label = axisXMinus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisXMinus, True, (-1, 0, 0)))
		cmds.menuItem(label = axisXPlus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisXPlus, True, (1, 0, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisYMinus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisYMinus, True, (0, -1, 0)))
		cmds.menuItem(label = axisYPlus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisYPlus, True, (0, 1, 0)))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = axisZMinus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisZMinus, True, (0, 0, -1)))
		cmds.menuItem(label = axisZPlus, command = partial(Install.ToShelf_LocatorsAim, self.optionsPlugin.directory, axisZPlus, True, (0, 0, 1)))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Baking", divider = True)
		cmds.menuItem(subMenu = True, label = "Bake", tearOff = True, image = Icons.bake)
		cmds.menuItem(label = "Classic", command = partial(Install.ToShelf_BakeClassic, self.optionsPlugin.directory))
		cmds.menuItem(label = "Classic Cut Out", command = partial(Install.ToShelf_BakeClassicCutOut, self.optionsPlugin.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Custom", command = partial(Install.ToShelf_BakeCustom, self.optionsPlugin.directory))
		cmds.menuItem(label = "Custom Cut Out", command = partial(Install.ToShelf_BakeCustomCutOut, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "By Last", tearOff = True, image = Icons.bake)
		cmds.menuItem(label = "By Last", command = partial(Install.ToShelf_BakeByLast, self.optionsPlugin.directory, True, True))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_BakeByLast, self.optionsPlugin.directory, True, False), image = Icons.move)
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_BakeByLast, self.optionsPlugin.directory, False, True), image = Icons.rotate)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "World", tearOff = True, image = Icons.world)
		cmds.menuItem(label = "World", command = partial(Install.ToShelf_BakeByWorld, self.optionsPlugin.directory, True, True))
		cmds.menuItem(label = "POS", command = partial(Install.ToShelf_BakeByWorld, self.optionsPlugin.directory, True, False), image = Icons.move)
		cmds.menuItem(label = "ROT", command = partial(Install.ToShelf_BakeByWorld, self.optionsPlugin.directory, False, True), image = Icons.rotate)
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Animation", divider = True)
		###
		cmds.menuItem(subMenu = True, label = "Delete", tearOff = True, image = Icons.delete)
		cmds.menuItem(label = "Animation", command = partial(Install.ToShelf_DeleteKeys, self.optionsPlugin.directory))
		cmds.menuItem(label = "Nonkeyable", command = partial(Install.ToShelf_DeleteNonkeyable, self.optionsPlugin.directory))
		cmds.menuItem(label = "Static", command = partial(Install.ToShelf_DeleteStatic, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(label = "Euler Filter", command = partial(Install.ToShelf_EulerFilterOnSelected, self.optionsPlugin.directory), image = Icons.filterActive)
		#
		cmds.menuItem(subMenu = True, label = "Infinity", tearOff = True, image = Icons.infinity)
		cmds.menuItem(label = "Constant", command = partial(Install.ToShelf_SetInfinity, self.optionsPlugin.directory, 1))
		cmds.menuItem(label = "Linear", command = partial(Install.ToShelf_SetInfinity, self.optionsPlugin.directory, 2))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Cycle", command = partial(Install.ToShelf_SetInfinity, self.optionsPlugin.directory, 3), image = Icons.cycle)
		cmds.menuItem(label = "Offset", command = partial(Install.ToShelf_SetInfinity, self.optionsPlugin.directory, 4), image = Icons.cycle)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Oscillate", command = partial(Install.ToShelf_SetInfinity, self.optionsPlugin.directory, 5))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Offset", tearOff = True, image = Icons.arrowsOutHorizontal)
		cmds.menuItem(label = "-3", command = partial(Install.ToShelf_AnimOffsetSelected, self.optionsPlugin.directory, -1, 3), image = Icons.minus)
		cmds.menuItem(label = "-2", command = partial(Install.ToShelf_AnimOffsetSelected, self.optionsPlugin.directory, -1, 2), image = Icons.minus)
		cmds.menuItem(label = "-1", command = partial(Install.ToShelf_AnimOffsetSelected, self.optionsPlugin.directory, -1, 1), image = Icons.minus)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "+1", command = partial(Install.ToShelf_AnimOffsetSelected, self.optionsPlugin.directory, 1, 1), image = Icons.plus)
		cmds.menuItem(label = "+2", command = partial(Install.ToShelf_AnimOffsetSelected, self.optionsPlugin.directory, 1, 2), image = Icons.plus)
		cmds.menuItem(label = "+3", command = partial(Install.ToShelf_AnimOffsetSelected, self.optionsPlugin.directory, 1, 3), image = Icons.plus)
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "TOOLS - Timeline", divider = True)
		cmds.menuItem(subMenu = True, label = "Timeline", tearOff = True)
		cmds.menuItem(label = "Min Out", command = partial(Install.ToShelf_SetTimelineMinOut, self.optionsPlugin.directory))
		cmds.menuItem(label = "Min In", command = partial(Install.ToShelf_SetTimelineMinIn, self.optionsPlugin.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Max In", command = partial(Install.ToShelf_SetTimelineMaxIn, self.optionsPlugin.directory))
		cmds.menuItem(label = "Max Out", command = partial(Install.ToShelf_SetTimelineMaxOut, self.optionsPlugin.directory))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Focus Out", command = partial(Install.ToShelf_SetTimelineFocusOut, self.optionsPlugin.directory), image = Icons.arrowsOut)
		cmds.menuItem(label = "Focus In", command = partial(Install.ToShelf_SetTimelineFocusIn, self.optionsPlugin.directory), image = Icons.arrowsIn)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Selected Range", command = partial(Install.ToShelf_SetTimelineSet, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "RIGGING - Constraints", divider = True)
		cmds.menuItem(subMenu = True, label = "Constraints", tearOff = True, image = Icons.constraint)
		cmds.menuItem(label = "Parent", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, False, True, False, False, False))
		cmds.menuItem(label = "Point", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, False, False, True, False, False))
		cmds.menuItem(label = "Orient", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, False, False, False, True, False))
		cmds.menuItem(label = "Scale", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, False, False, False, False, True))
		cmds.menuItem(divider = True)
		cmds.menuItem(label = "Parent With Maintain", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, True, True, False, False, False))
		cmds.menuItem(label = "Point With Maintain", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, True, False, True, False, False))
		cmds.menuItem(label = "Orient With Maintain", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, True, False, False, True, False))
		cmds.menuItem(label = "Scale With Maintain", command = partial(Install.ToShelf_Constraint, self.optionsPlugin.directory, True, False, False, False, True))
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Connections", tearOff = True, image = Icons.constraint)
		cmds.menuItem(label = "Disconnect", command = partial(Install.ToShelf_DisconnectTargets, self.optionsPlugin.directory))
		cmds.menuItem(label = "Delete Constraints", command = partial(Install.ToShelf_DeleteConstraints, self.optionsPlugin.directory))
		cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "RIGGING - Utils", divider = True)
		cmds.menuItem(subMenu = True, label = "Rotate Order", tearOff = True)
		cmds.menuItem(label = "Show", command = partial(Install.ToShelf_RotateOrder, self.optionsPlugin.directory, True), image = Icons.visibleOn)
		cmds.menuItem(label = "Hide", command = partial(Install.ToShelf_RotateOrder, self.optionsPlugin.directory, False), image = Icons.visibleOff)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Segment Scale Compensate", tearOff = True, image = Icons.joint)
		cmds.menuItem(label = "On", command = partial(Install.ToShelf_SegmentScaleCompensate, self.optionsPlugin.directory, True), image = Icons.on)
		cmds.menuItem(label = "Off", command = partial(Install.ToShelf_SegmentScaleCompensate, self.optionsPlugin.directory, False), image = Icons.off)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(subMenu = True, label = "Joint Draw Style", tearOff = True, image = Icons.joint)
		cmds.menuItem(label = "Bone", command = partial(Install.ToShelf_JointDrawStyle, self.optionsPlugin.directory, 0), image = Icons.visibleOn)
		cmds.menuItem(label = "Hidden", command = partial(Install.ToShelf_JointDrawStyle, self.optionsPlugin.directory, 2), image = Icons.visibleOff)
		cmds.setParent('..', menu = True)
		#
		cmds.menuItem(label = "Copy Skin Weights From Last Selected", command = partial(Install.ToShelf_CopySkin, self.optionsPlugin.directory), image = Icons.copySkinWeights)
		
		cmds.menuItem(dividerLabel = "RIGGING - Blendshapes", divider = True)
		# cmds.menuItem(subMenu = True, label = "Rotate Order", tearOff = True)
		cmds.menuItem(label = "Wraps Create", command = partial(Install.ToShelf_WrapsCreate, self.optionsPlugin.directory), image = Icons.wrap)
		# cmds.menuItem(label = "Wraps Convert", command = partial(Install.ToShelf_WrapsCreate, self.options.directory), image = Icons.wrap) # TODO
		cmds.menuItem(label = "Reconstruct", command = partial(Install.ToShelf_BlendshapesReconstruct, self.optionsPlugin.directory), image = Icons.blendshape)
		cmds.menuItem(label = "Extract Shapes", command = partial(Install.ToShelf_BlendshapesExtractShapes, self.optionsPlugin.directory), image = Icons.polyMesh)
		cmds.menuItem(label = "Zero Weights", command = partial(Install.ToShelf_BlendshapesZeroWeights, self.optionsPlugin.directory), image = Icons.zero)
		# cmds.setParent('..', menu = True)
		
		cmds.menuItem(dividerLabel = "RIGGING - Curves", divider = True)
		cmds.menuItem(label = "Create Curve From Selected Objects", command = partial(Install.ToShelf_CreateCurveFromSelectedObjects, self.optionsPlugin.directory), image = Icons.nurbsCurve)
		cmds.menuItem(label = "Create Curve From Trajectory", command = partial(Install.ToShelf_CreateCurveFromTrajectory, self.optionsPlugin.directory), image = Icons.nurbsCurve)
		
		cmds.menuItem(dividerLabel = "MOTION TRAIL", divider = True)
		cmds.menuItem(subMenu = True, label = "Motion Trail", tearOff = True, image = Icons.motionTrail)
		cmds.menuItem(label = "Create", command = partial(Install.ToShelf_MotionTrailCreate, self.optionsPlugin.directory), image = Icons.plus)
		cmds.menuItem(label = "Select", command = partial(Install.ToShelf_MotionTrailSelect, self.optionsPlugin.directory), image = Icons.cursor)
		cmds.menuItem(label = "Delete", command = partial(Install.ToShelf_MotionTrailDelete, self.optionsPlugin.directory), image = Icons.minus)
		cmds.setParent('..', menu = True)
	
	def LayoutTools(self, parentLayout):
		self.frameTools = cmds.frameLayout("layoutTools", parent = parentLayout, label = "1. " + Tools.Tools._title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = 0, marginHeight = 0)
		Tools.Tools(self.optionsPlugin).UICreate(self.frameTools)
	def LayoutRigging(self, parentLayout):
		self.frameRigging = cmds.frameLayout("layoutRigging", parent = parentLayout, label = "2. " + Rigging.Rigging._title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = 0, marginHeight = 0)
		Rigging.Rigging(self.optionsPlugin).UICreate(self.frameRigging)
	def LayoutOverlappy(self, parentLayout):
		self.frameOverlappy = cmds.frameLayout("layoutOverlappy", parent = parentLayout, label = "3. " + Overlappy.Overlappy._title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = 0, marginHeight = 0)
		Overlappy.Overlappy(self.optionsPlugin).UICreate(self.frameOverlappy)
	def LayoutCenterOfMass(self, parentLayout):
		self.frameCenterOfMass = cmds.frameLayout("layoutCenterOfMass", parent = parentLayout, label = "4. " + CenterOfMass.CenterOfMass._title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = 0, marginHeight = 0)
		CenterOfMass.CenterOfMass(self.optionsPlugin).UICreate(self.frameCenterOfMass)
	def LayoutMotionTrail(self, parentLayout):
		versionMT = "v1.0" # TODO move to Motion Trail class when possible
		nameMT = "MOTION TRAIL"
		titleMT = nameMT + " " + versionMT
				
		self.frameMotionTrail = cmds.frameLayout("layoutMotionTrail", parent = parentLayout, label = "5. " + titleMT, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = 0, marginHeight = 0, width = Settings.windowWidth)
		
		countOffsets = 3
		cmds.gridLayout(parent = self.frameMotionTrail, numberOfColumns = countOffsets, cellWidth = Settings.windowWidth / countOffsets, cellHeight = Settings.lineHeight)
		cmds.button(label = "Create", command = MotionTrail.Create, backgroundColor = Colors.orange10)
		cmds.button(label = "Select All", command = MotionTrail.Select, backgroundColor = Colors.orange50)
		cmds.button(label = "Delete All", command = MotionTrail.Delete, backgroundColor = Colors.orange100)
		# cmds.popupMenu()
		# cmds.menuItem(label = "Select", command = MotionTrail.Select)
		# cmds.menuItem(label = "Delete", command = MotionTrail.Delete)
	def LayoutExperimental(self, parentLayout):
		self.frameExperimental = cmds.frameLayout("layoutExperimental", parent = parentLayout, label = Experimental.Experimental._title, collapsable = True, backgroundColor = Settings.frames1Color, marginWidth = 0, marginHeight = 0)
		Experimental.Experimental(self.optionsPlugin).UICreate(self.frameExperimental)
	
	### WINDOW
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
		if self.frameTools is not None:
			cmds.frameLayout(self.frameTools, edit = True, collapse = value)
		if self.frameRigging is not None:
			cmds.frameLayout(self.frameRigging, edit = True, collapse = value)
		if self.frameOverlappy is not None:
			cmds.frameLayout(self.frameOverlappy, edit = True, collapse = value)
		if self.frameCenterOfMass is not None:
			cmds.frameLayout(self.frameCenterOfMass, edit = True, collapse = value)
		if self.frameMotionTrail is not None:
			cmds.frameLayout(self.frameMotionTrail, edit = True, collapse = value)
		if self.frameExperimental is not None:
			cmds.frameLayout(self.frameExperimental, edit = True, collapse = value)

	### DOCKING
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
			print("{0} undocked".format(GeneralWindow._title))
		else:
			cmds.warning("Dock Controls wasn't found")
	def DockToSide(self, areaSide, *args):
		if self.DockCheck():
			cmds.dockControl(Settings.dockName, edit = True, floating = False, area = areaSide)
		else:
			cmds.dockControl(Settings.dockName, label = GeneralWindow._title, content = Settings.windowName, area = areaSide, allowedArea = Settings.dockAllowedAreas) # , backgroundColor = Colors.lightBlue10
		print("{0} docked to {1}".format(GeneralWindow._title, areaSide))

	### EXECUTION
	def WindowCreate(self, *args):
		self.CreateUI()
		self.FramesCollapse(True)
	def RUN_DOCKED(self, path="", forced=False, *args):
		self.optionsPlugin.directory = path

		if (not forced and self.DockCheck()): # for script toggling. Comment these 3 lines if you need to deactivate toggling
			if (self.DockCheckVisible()):
				self.DockDelete()
				print("{0} closed".format(GeneralWindow._title))
				return

		self.DockDelete()
		self.WindowCreate()
		self.DockToSide(Settings.dockStartArea)

		MayaSettings.HelpPopupActivate()
		MayaSettings.CachedPlaybackDeactivate()

