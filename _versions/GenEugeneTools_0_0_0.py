# To run from console
# import CreateLocators
# CreateLocators.create_locators()
'''

LOCATORS
- Create locators
- Create and match locators

JOINTS
- Change draw style
- Change scale compensate

OTHER
- Clear nonkeyable keys
- Baking with/without cut keys

- Rotate to aim
- *Curve walker
- *Chain parent

'''

import maya.cmds as cmds
import sys



class Locators:
	'''Tool for create locator on selected object with matching'''
	@staticmethod
	def create_locators():
		setScale = 3
		tempList = cmds.ls(sl = True)
		for i in range(len(tempList)):
			locName = tempList[i] + "_loc_" + str(i+1)
			cmds.spaceLocator(n = locName)
			cmds.matchTransform(locName, tempList[i])
			cmds.setAttr(locName + "Shape.localScaleX", setScale)
			cmds.setAttr(locName + "Shape.localScaleY", setScale)
			cmds.setAttr(locName + "Shape.localScaleZ", setScale)
	
	'''DRAFT'''
	@staticmethod
	def CreateMatchLocator(mode=0):
		locGrpName = "temp_locators"
		pConstrGrpName = "temp_pConstraints"
		setScale = 3
		objList = cmds.ls(sl = True)
	
		for i in range(len(objList)):
			locName = objList[i] + "_loc_" + str(i+1)
			cmds.spaceLocator(n = locName)
			cmds.matchTransform(locName, objList[i])
			cmds.setAttr(locName + "Shape.localScaleX", setScale)
			cmds.setAttr(locName + "Shape.localScaleY", setScale)
			cmds.setAttr(locName + "Shape.localScaleZ", setScale)
			# Loc group creation
			'''
			cmds.select(locName, r=1)
			if cmds.objExists(locGrpName):
				#cmds.parent(locName, locGrpName)
				cmds.parent(locGrpName)
			else:
				cmds.group(n = locGrpName, w=1)
			'''
		
			if mode==1:
				# Constraint part
				pConstrName = locName + "_parentConstraint1"
				sConstrName = locName + "_scaleConstraint1"
				cmds.parentConstraint(objList[i], locName)
				cmds.scaleConstraint(objList[i], locName)
				'''
				# Parent constraint group creation
				cmds.select(constrName, r=1)
				if cmds.objExists(pConstrGrpName):
					cmds.parent(constrName, pConstrGrpName)
				else:
					cmds.group(n = pConstrGrpName, w=1)
			
				# Scale constraint group creation
				cmds.select(constrName, r=1)
				if cmds.objExists(pConstrGrpName):
					cmds.parent(constrName, pConstrGrpName)
				else:
					cmds.group(n = pConstrGrpName, w=1)
				'''
	
		cmds.select(cl=1)


class Joints:
	'''Set joints draw style'''
	@staticmethod
	def DrawStyle(mode=0):
		selected = cmds.ls(sl=1)
		for i in range(len(selected)):
			cmds.setAttr(selected[i] + ".drawStyle", mode)
	
	'''Joint segment scale compensate'''
	@staticmethod
	def ScaleCompensate(value=0):
		jointList = cmds.ls(sl=1, typ="joint")
		for i in jointList:
			cmds.setAttr(i + ".segmentScaleCompensate", value)


class Other:
	'''Search and clear nonkeyable attributes keys'''
	@staticmethod
	def ClearNonkeyableKeys():
		objects = cmds.ls(sl=1)
		counter = 0
		for i in range(len(objects)):
			attributes = cmds.listAttr(objects[i], cb=1)
			if attributes != None:
				for j in range(len(attributes)):
					cmds.cutKey(objects[i] + "." + attributes[j])
					counter += 1
		print ("\t{} nonkeyable detected and deleted".format(counter))


	'''Search and clear nonkeyable attributes keys'''
	@staticmethod
	def MyBake(DoNotCut=1):
		startTime = cmds.playbackOptions(q=1, min=1)
		endTime = cmds.playbackOptions(q=1, max=1)
		cmds.bakeResults(t=(startTime,endTime), pok=DoNotCut, simulation=1)
	
	#'''Rotate to aim'''
	#@staticmethod
	#def RotateToAim(vector=(0,0,1)):
	#	'''Need to select 2 objects (child and parent)'''
	#	selection = cmds.ls(sl=True)
	#	cmds.aimConstraint(selection[1], selection[0],
	#	wu = vector)
	#	cmds.delete(selection[0]+'_aimConstraint1')
	
	#'''Set scale to keys of selected objects'''
	#@staticmethod
	#def SetScale():
	#	scaleValue = 0.001
	#	cutSymbols = 13
		
	#	cmds.select("rig_Adult_01:FKWrist_holdObject_R", r=1)
	#	cmds.select("rig_Adult_01:FKWrist_holdObject_L", add=1)
	#	cmds.select("rig_Adult_01:CT_MainHoldObject_01", add=1)
	#	cmds.select("rig_Adult_01:CT_MainHoldObject_02", add=1)
	#	cmds.select("rig_Adult_01:CT_MainHoldObject_03", add=1)
	#	cmds.select("rig_Adult_01:CT_MainHoldObject_04", add=1)
	#	cmds.select("rig_Adult_01:CT_MainHoldObject_05", add=1)
	#	cmds.select("rig_Adult_01:CT_MainHoldObject_06", add=1)
	#	holdObjects = cmds.ls(sl=1)
		
	#	for i in range(len(holdObjects)):
	#		holdObjects[i] = holdObjects[i][cutSymbols:]
			
	#		try:
	#			cmds.selectKey(holdObjects[i] + "_scaleX", r=1)
	#			cmds.selectKey(holdObjects[i] + "_scaleY", add=1)
	#			cmds.selectKey(holdObjects[i] + "_scaleZ", add=1)
	#			cmds.keyframe(absolute=1, valueChange=scaleValue)
	#		except:
	#			print (holdObjects[i] + "has no scale keys")
	
	
	#'''DRAFT Create nurbs curve from selected trail'''
	#@staticmethod
	#def CurveFromTrail():
	#	# Variables
	#	step = 1
	#	degree = 3
	#	# Names
	#	mtName = "newMotionTrail"
	#	mtFinalName = mtName + "Handle"
	#	curveName = "testCurve"
		
	#	# Get time start/end
	#	start = cmds.playbackOptions(q=1, min=1)
	#	end = cmds.playbackOptions(q=1, max=1)
	#	# Create motion trail
	#	cmds.snapshot(n = mtName, mt=1, i=step, st = start, et = end)
		
	#	# Get points from motion trail
	#	cmds.select(mtFinalName, r=1)
	#	selected = cmds.ls(sl=1, dag=1, et="snapshotShape")
	#	pts = cmds.getAttr(selected[0] + ".pts")
	#	size = len(pts)
	#	for i in range(size):
	#		pts[i] = pts[i][0:3]
	#		#print "{0}: {1}".format(i, pts[i])
		
	#	# Create curve
	#	newCurve = cmds.curve(n = curveName, d = degree, p = pts)
		
	#	# End
	#	cmds.delete(mtFinalName)
	#	cmds.select(cl=1)
	
	


### Create instance ###
#python("from GenEugeneToolbelt import Other as Other");

#python("import GenEugeneToolbelt as myTools");
#python("myLocators = myTools.Locators()");
#python("myJoints = myTools.Joints()");
#python("myOther = myTools.Other()");

'''Locators'''
#python("myLocators.CreateMatchLocator(1)");

'''Delete Nonkeyable'''
#python("import GenEugeneToolbelt as myTools");
#python("myOther = myTools.Other()");
#python("myOther.ClearNonkeyableKeys()");

'''Bake/CutBake'''
#python("import GenEugeneToolbelt as myTools");
#python("myOther = myTools.Other()");
#python("myOther.MyBake(1)");
#python("myOther.MyBake(0)");