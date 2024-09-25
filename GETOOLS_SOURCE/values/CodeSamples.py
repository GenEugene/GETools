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
	import GETOOLS_SOURCE.utils.Scene as Scene
	Scene.Reload()

def ExitMaya():
	import GETOOLS_SOURCE.utils.Scene as Scene
	Scene.ExitMaya()


# UTILS
def SelectHierarchy():
	import GETOOLS_SOURCE.utils.Selector as Selector
	Selector.SelectHierarchy()

def SelectHierarchyTransforms():
	import GETOOLS_SOURCE.utils.Selector as Selector
	Selector.SelectHierarchyTransforms()

def SavePoseToShelf():
	import GETOOLS_SOURCE.utils.Install as Install
	Install.CreatePoseButton()

def ParentShapes():
	import GETOOLS_SOURCE.utils.Parent as Parent
	Parent.ParentShape()

def AnnotateSelected():
	import GETOOLS_SOURCE.utils.Annotation as Annotation
	Annotation.AnnotateSelected()


# TOGGLES
def ToggleCameras():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleCameras()

def ToggleControlVertices():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleControlVertices()

def ToggleDeformers():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleDeformers()

def ToggleDimensions():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleDimensions()

def ToggleDynamicConstraints():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleDynamicConstraints()

def ToggleDynamics():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleDynamics()

def ToggleFluids():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleFluids()

def ToggleFollicles():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleFollicles()

def ToggleGrid():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleGrid()

def ToggleHairSystems():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleHairSystems()

def ToggleHandles():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleHandles()

def ToggleHulls():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleHulls()

def ToggleIkHandles():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleIkHandles()

def ToggleJoints():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleJoints()

def ToggleLights():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleLights()

def ToggleLocators():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleLocators()

def ToggleManipulators():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleManipulators()

def ToggleNCloths():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleNCloths()

def ToggleNParticles():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleNParticles()

def ToggleNRigids():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleNRigids()

def ToggleNurbsCurves():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleNurbsCurves()

def ToggleNurbsSurfaces():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleNurbsSurfaces()

def TogglePivots():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.TogglePivots()

def TogglePlanes():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.TogglePlanes()

def TogglePolymeshes():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.TogglePolymeshes()

def ToggleShadows():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleShadows()

def ToggleStrokes():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleStrokes()

def ToggleSubdivSurfaces():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleSubdivSurfaces()

def ToggleTextures():
	import GETOOLS_SOURCE.utils.Toggles as Toggles
	Toggles.ToggleTextures()


# LOCATORS
def LocatorsSizeScale(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.SelectedLocatorsSizeScale

def LocatorsSizeSet():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.SelectedLocatorsSizeSet()

def LocatorCreate():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.Create()

def LocatorsMatch():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelected(constraint = False)

def LocatorsParent():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelected(constraint = True)

def LocatorsPin():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = True)

def LocatorsPinWithoutReverse():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelected(constraint = True, bake = True)

def LocatorsPinPos():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = True, constrainRotate = False)

def LocatorsPinRot():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelected(constraint = True, bake = True, constrainReverse = True, constrainTranslate = False, constrainRotate = True)

def LocatorsRelative():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True, skipLastReverse = False)

def LocatorsRelativeSkipLast():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateAndBakeAsChildrenFromLastSelected(constraintReverse = True)

def LocatorsRelativeWithoutReverse():
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateAndBakeAsChildrenFromLastSelected()

def LocatorsAim(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Locators as Locators
	Locators.CreateOnSelectedAim


# BAKINNG
def BakeClassic(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as Baker
    Baker.BakeSelected

def BakeCustom(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as Baker
    Baker.BakeSelected

def BakeByLast(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as Baker
    Baker.BakeSelectedByLastObject

def BakeByWorld(): # brackets added when method used
    import GETOOLS_SOURCE.utils.Baker as Baker
    Baker.BakeSelectedByWorld


# ANIMATION
def AnimOffsetSelected(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Animation as Animation
	Animation.OffsetSelected

def DeleteKeys():
	import GETOOLS_SOURCE.utils.Animation as Animation
	Animation.DeleteKeys(True)

def DeleteNonkeyable():
	import GETOOLS_SOURCE.utils.Animation as Animation
	Animation.DeleteKeysNonkeyable()

def DeleteStatic():
	import GETOOLS_SOURCE.utils.Animation as Animation
	Animation.DeleteStaticCurves()

def EulerFilterOnSelected():
	import GETOOLS_SOURCE.utils.Animation as Animation
	Animation.EulerFilterOnSelected()

def SetInfinity(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Animation as Animation
	Animation.SetInfinity

def SetTimeline(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Timeline as Timeline
	Timeline.SetTime


# RIGGING
def Constraint(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Constraints as Constraints
	Constraints.ConstrainSelectedToLastObject

def DeleteConstraints():
	import GETOOLS_SOURCE.utils.Constraints as Constraints
	Constraints.DeleteConstraintsOnSelected()

def DisconnectTargets():
	import GETOOLS_SOURCE.utils.Constraints as Constraints
	Constraints.DisconnectTargetsFromConstraintOnSelected()

def RotateOrder(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Other as Other
	Other.RotateOrderVisibility

def SegmentScaleCompensate(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Other as Other
	Other.SegmentScaleCompensate

def JointDrawStyle(): # brackets added when method used
	import GETOOLS_SOURCE.utils.Other as Other
	Other.JointDrawStyle

def CopySkin():
	import GETOOLS_SOURCE.utils.Skinning as Skinning
	Skinning.CopySkinWeightsFromLastMesh()

def SelectSkinnedMeshesOrJoints():
	import GETOOLS_SOURCE.utils.Skinning as Skinning
	Skinning.SelectSkinnedMeshesOrJoints()

def WrapsCreate():
	import GETOOLS_SOURCE.utils.Deformers as Deformers
	Deformers.WrapsCreateOnSelected()

def WrapsConvert(): # TODO
	import GETOOLS_SOURCE.utils.Deformers as Deformers
	Deformers.WrapsConvertFromSelected()

def BlendshapesReconstruct():
	import GETOOLS_SOURCE.utils.Deformers as Deformers
	Deformers.BlendshapesReconstruction()

def BlendshapesExtractShapes():
	import GETOOLS_SOURCE.utils.Blendshapes as Blendshapes
	Blendshapes.ExtractShapesFromSelected()

def BlendshapesZeroWeights():
	import GETOOLS_SOURCE.utils.Blendshapes as Blendshapes
	Blendshapes.ZeroBlendshapeWeightsOnSelected()

def CreateCurveFromSelectedObjects():
	import GETOOLS_SOURCE.utils.Curves as Curves
	Curves.CreateCurveFromSelectedObjects()

def CreateCurveFromTrajectory():
	import GETOOLS_SOURCE.utils.Curves as Curves
	Curves.CreateCurveFromTrajectory()


# MOTION TRAIL
def MotionTrailCreate():
	import GETOOLS_SOURCE.utils.MotionTrail as MotionTrail
	MotionTrail.Create()

def MotionTrailSelect():
	import GETOOLS_SOURCE.utils.MotionTrail as MotionTrail
	MotionTrail.Select()

def MotionTrailDelete():
	import GETOOLS_SOURCE.utils.MotionTrail as MotionTrail
	MotionTrail.Delete()

