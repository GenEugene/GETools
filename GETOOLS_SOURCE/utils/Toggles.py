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

import maya.cmds as cmds

from ..values import Enums

def Toggle(parameter):
	currentPanel = cmds.getPanel(withFocus = True)
	checkModelEditor = cmds.modelEditor(currentPanel, exists = True)

	if (not checkModelEditor):
		cmds.warning("No Model Editor in panel \"{0}\"".format(currentPanel))
		return

	check = cmds.modelEditor(currentPanel, query = True, **{parameter: True})
	cmds.modelEditor(currentPanel, edit = True, **{parameter: not check})
	print("Panel \"{0}\", {1} {2}".format(currentPanel, parameter, not check))

# def ToggleAllObjects(*args): Toggle(Enums.ModelEditor.allObjects)
def ToggleCameras(*args): Toggle(Enums.ModelEditor.cameras)
def ToggleControlVertices(*args): Toggle(Enums.ModelEditor.controlVertices)
def ToggleDeformers(*args): Toggle(Enums.ModelEditor.deformers)
def ToggleDimensions(*args): Toggle(Enums.ModelEditor.dimensions)
def ToggleDynamicConstraints(*args): Toggle(Enums.ModelEditor.dynamicConstraints)
def ToggleDynamics(*args): Toggle(Enums.ModelEditor.dynamics)
def ToggleFluids(*args): Toggle(Enums.ModelEditor.fluids)
def ToggleFollicles(*args): Toggle(Enums.ModelEditor.follicles)
def ToggleGrid(*args): Toggle(Enums.ModelEditor.grid)
def ToggleHairSystems(*args): Toggle(Enums.ModelEditor.hairSystems)
def ToggleHandles(*args): Toggle(Enums.ModelEditor.handles)
def ToggleHulls(*args): Toggle(Enums.ModelEditor.hulls)
def ToggleIkHandles(*args): Toggle(Enums.ModelEditor.ikHandles)
def ToggleJoints(*args): Toggle(Enums.ModelEditor.joints)
def ToggleLights(*args): Toggle(Enums.ModelEditor.lights)
def ToggleLocators(*args): Toggle(Enums.ModelEditor.locators)
def ToggleManipulators(*args): Toggle(Enums.ModelEditor.manipulators)
def ToggleNCloths(*args): Toggle(Enums.ModelEditor.nCloths)
def ToggleNParticles(*args): Toggle(Enums.ModelEditor.nParticles)
def ToggleNRigids(*args): Toggle(Enums.ModelEditor.nRigids)
def ToggleNurbsCurves(*args): Toggle(Enums.ModelEditor.nurbsCurves)
def ToggleNurbsSurfaces(*args): Toggle(Enums.ModelEditor.nurbsSurfaces)
def TogglePivots(*args): Toggle(Enums.ModelEditor.pivots)
def TogglePlanes(*args): Toggle(Enums.ModelEditor.planes)
def TogglePolymeshes(*args): Toggle(Enums.ModelEditor.polymeshes)
def ToggleShadows(*args): Toggle(Enums.ModelEditor.shadows)
def ToggleStrokes(*args): Toggle(Enums.ModelEditor.strokes)
def ToggleSubdivSurfaces(*args): Toggle(Enums.ModelEditor.subdivSurfaces)
def ToggleTextures(*args): Toggle(Enums.ModelEditor.textures)

