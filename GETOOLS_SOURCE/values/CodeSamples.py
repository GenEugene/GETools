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
# Logic in this module is not optimal enough, need manually change path names, methods and parameters.


def GeneralWindow(): # brackets added when method used
	import GETOOLS_SOURCE.modules.GeneralWindow as gtwindow
	gtwindow.GeneralWindow().RUN_DOCKED


# FILE
def SceneReload():
	import GETOOLS_SOURCE.utils.Scene as scene
	scene.Reload()

def ExitMaya():
	import GETOOLS_SOURCE.utils.Scene as scene
	scene.ExitMaya()


# UTILS
def SelectHierarchy():
	import GETOOLS_SOURCE.utils.Selector as selector
	selector.SelectHierarchy()

def CreateResetButton():
	import GETOOLS_SOURCE.utils.Install as install
	install.CreateResetButton()


# TOGGLES
def ToggleCameras():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleCameras()

def ToggleControlVertices():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleControlVertices()

def ToggleDeformers():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleDeformers()

def ToggleDimensions():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleDimensions()

def ToggleDynamicConstraints():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleDynamicConstraints()

def ToggleDynamics():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleDynamics()

def ToggleFluids():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleFluids()

def ToggleFollicles():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleFollicles()

def ToggleGrid():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleGrid()

def ToggleHairSystems():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleHairSystems()

def ToggleHandles():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleHandles()

def ToggleHulls():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleHulls()

def ToggleIkHandles():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleIkHandles()

def ToggleJoints():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleJoints()

def ToggleLights():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleLights()

def ToggleLocators():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleLocators()

def ToggleManipulators():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleManipulators()

def ToggleNCloths():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleNCloths()

def ToggleNParticles():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleNParticles()

def ToggleNRigids():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleNRigids()

def ToggleNurbsCurves():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleNurbsCurves()

def ToggleNurbsSurfaces():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleNurbsSurfaces()

def TogglePivots():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.TogglePivots()

def TogglePlanes():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.TogglePlanes()

def TogglePolymeshes():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.TogglePolymeshes()

def ToggleShadows():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleShadows()

def ToggleStrokes():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleStrokes()

def ToggleSubdivSurfaces():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleSubdivSurfaces()

def ToggleTextures():
	import GETOOLS_SOURCE.utils.Toggles as toggles
	toggles.ToggleTextures()


# LOCATORS
def LocatorsSizeScale(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.SelectedLocatorsSizeScale

def LocatorsSizeSet():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.SelectedLocatorsSizeSet()

def LocatorCreate():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.Create()

def LocatorsMatch():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelected(constraint = False)

def LocatorsParent():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelected(constraint = True)

def LocatorsPin():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = True)

def LocatorsPinWithoutReverse():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelected(constraint = True, bake = True)

def LocatorsPinPos():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = False)

def LocatorsPinRot():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = False, constrainRotate = True)

def LocatorsRelative():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True, skipLastReverse = False)

def LocatorsRelativeSkipLast():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True)

def LocatorsRelativeWithoutReverse():
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateAndBakeAsChildrenFromLastSelected()

def LocatorsAim(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Locators as locators
	locators.CreateOnSelectedAim


# BAKINNG
def BakeClassic(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as baker
    baker.BakeSelected

def BakeCustom(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as baker
    baker.BakeSelected

def BakeByLast(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as baker
    baker.BakeSelectedByLastObject

def BakeByWorld(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as baker
    baker.BakeSelectedByWorld


# ANIMATION
def AnimOffsetSelected(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Animation as animation
	animation.OffsetSelected

def DeleteKeys():
	import GETOOLS_SOURCE.utils.Animation as animation
	animation.DeleteKeys(True)

def DeleteNonkeyable():
	import GETOOLS_SOURCE.utils.Animation as animation
	animation.DeleteKeysNonkeyable()

def DeleteStatic():
	import GETOOLS_SOURCE.utils.Animation as animation
	animation.DeleteStaticCurves()

def EulerFilterOnSelected():
	import GETOOLS_SOURCE.utils.Animation as animation
	animation.EulerFilterOnSelected()

def SetInfinity(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Animation as animation
	animation.SetInfinity

def SetTimeline(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Timeline as timeline
	timeline.SetTime


# RIGGING
def Constraint(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Constraints as constraints
	constraints.ConstrainSelectedToLastObject

def DeleteConstraints():
	import GETOOLS_SOURCE.utils.Constraints as constraints
	constraints.DeleteConstraintsOnSelected()

def DisconnectTargets():
	import GETOOLS_SOURCE.utils.Constraints as constraints
	constraints.DisconnectTargetsFromConstraintOnSelected()

def RotateOrder(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Other as other
	other.RotateOrderVisibility

def SegmentScaleCompensate(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Other as other
	other.SegmentScaleCompensate

def JointDrawStyle(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Other as other
	other.JointDrawStyle

def CopySkin():
	import GETOOLS_SOURCE.utils.Skinning as skinning
	skinning.CopySkinWeightsFromLastMesh()

def SelectSkinnedMeshesOrJoints():
	import GETOOLS_SOURCE.utils.Skinning as skinning
	skinning.SelectSkinnedMeshesOrJoints()

def WrapsCreate():
	import GETOOLS_SOURCE.utils.Deformers as deformers
	deformers.WrapsCreateOnSelected()

def WrapsConvert(): # TODO
	import GETOOLS_SOURCE.utils.Deformers as deformers
	deformers.WrapsConvertFromSelected()

def BlendshapesReconstruct():
	import GETOOLS_SOURCE.utils.Deformers as deformers
	deformers.BlendshapesReconstruction()

def BlendshapesExtractShapes():
	import GETOOLS_SOURCE.utils.Blendshapes as blendshapes
	blendshapes.ExtractShapesFromSelected()

def BlendshapesZeroWeights():
	import GETOOLS_SOURCE.utils.Blendshapes as blendshapes
	blendshapes.ZeroBlendshapeWeightsOnSelected()


# EXPERIMENTAL
def MotionTrailCreate():
	import GETOOLS_SOURCE.utils.MotionTrail as mtrail
	mtrail.Create()

def MotionTrailSelect():
	import GETOOLS_SOURCE.utils.MotionTrail as mtrail
	mtrail.Select()

def MotionTrailDelete():
	import GETOOLS_SOURCE.utils.MotionTrail as mtrail
	mtrail.Delete()

