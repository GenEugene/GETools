################################################################################
# MAYA TOOLBELT v0.0.1
################################################################################
""" TO DO    ||| FOR DEBUG ||| sys.exit() |||
	-
	-
	-
"""
################################################################################

### Import ###
import maya.cmds as cmds
import sys

#from datetime import datetime
#from inspect import currentframe, getframeinfo

### Class ###
class GETools:


	class OTHER:
		@staticmethod
		def ShowRotateOrder(on=True):
			selected = cmds.ls(sl=1, l=1)
			for i in range(len(selected)):
				cmds.setAttr(selected[i] + ".rotateOrder", cb = on)
				
				
		@staticmethod	
		def SetTimelineTime(mode):
			_current = cmds.currentTime(q=1)
			if (mode == 1):
				cmds.playbackOptions(min = _current)
			if (mode == 2):
				cmds.playbackOptions(max = _current)
			if (mode == 3):
				cmds.playbackOptions(ast = _current)
			if (mode == 4):
				cmds.playbackOptions(aet = _current)
			if (mode == 5):
				cmds.playbackOptions(min = cmds.playbackOptions(q=1, ast=1))
				cmds.playbackOptions(max = cmds.playbackOptions(q=1, aet=1))
			'''
			#SetTimelineTime(1)
			#SetTimelineTime(2)
			#SetTimelineTime(3)
			#SetTimelineTime(4)
			#SetTimelineTime(5)
			'''

	class LOCATORS:
		'''Create locator on selected object with matching'''
		@staticmethod
		def CreateLocators(locScale=1, match=True, constraint=False):
			m_emptyGrpName = "grp_01"
			m_emptyLocName = "loc_"
			
			m_tempList = cmds.ls(sl = True)
			cmds.select(cl = True)
			
			if (len(m_tempList) == 0):
				cmds.spaceLocator(n = m_emptyGrpName)
				_grp = cmds.ls(sl = True)
				cmds.spaceLocator(n = m_emptyLocName)
				_loc = cmds.ls(sl = True)
				cmds.parent(_loc, _grp)
				cmds.rename(_loc[0], m_emptyLocName + _grp[0][4:])
				_loc = cmds.ls(sl = True)
				cmds.setAttr(_grp[0] + "Shape.visibility", 0)
				
				cmds.setAttr(_loc[0] + "Shape.localScaleX", locScale)
				cmds.setAttr(_loc[0] + "Shape.localScaleY", locScale)
				cmds.setAttr(_loc[0] + "Shape.localScaleZ", locScale)
			else:
				for i in range(len(m_tempList)):
					_grpName = "grp_" + m_tempList[i] + "_" + str(i+1)
					_locName = "loc_" + m_tempList[i] + "_" + str(i+1)
					
					cmds.spaceLocator(n = _grpName)
					_grp = cmds.ls(sl = True)
					cmds.spaceLocator(n = _locName)
					_loc = cmds.ls(sl = True)
					cmds.parent(_loc, _grp)
					cmds.rename(_loc[0], m_emptyLocName + _grp[0][4:])
					_loc = cmds.ls(sl = True)
					cmds.setAttr(_grp[0] + "Shape.visibility", 0)
					
					cmds.setAttr(_loc[0] + "Shape.localScaleX", locScale)
					cmds.setAttr(_loc[0] + "Shape.localScaleY", locScale)
					cmds.setAttr(_loc[0] + "Shape.localScaleZ", locScale)
					
					if(match):
						cmds.matchTransform(_grp[0], m_tempList[i])
					if(constraint):
						cmds.parentConstraint(m_tempList[i], _grp[0])
						cmds.scaleConstraint(m_tempList[i], _grp[0])
			
			cmds.select(cl = True)
		
		
		'''Create parent group from selected object with matching'''
		@staticmethod
		def CreateGroups(match=True):
			m_emptyGrpName = "grp_01"
			m_emptyLocName = "loc_"
			
			m_tempList = cmds.ls(sl = True)
			cmds.select(cl = True)
			
			if (len(m_tempList) == 0):
				print("Objects not selected")
			else:
				for i in range(len(m_tempList)):
					_grpName = "grp_" + m_tempList[i] + "_" + str(i+1)
					_locName = "loc_" + m_tempList[i] + "_" + str(i+1)
					
					cmds.group(n = _grpName, em=1)
					_grp = cmds.ls(sl = True)
					
					cmds.select(m_tempList[i])
					_parent = cmds.listRelatives(p=1, f=1, pa=1, typ="transform")
					cmds.select(cl = True)
					
					try:
						cmds.parent(_grp[0], _parent[0])
						_grp = cmds.ls(sl = True)
					except:
						pass
					
					if(match): cmds.matchTransform(_grp[0], m_tempList[i])
					#cmds.makeIdentity(a=1,t=1, r=1, s=1) ///freeze attributes
					
					cmds.parent(m_tempList[i], _grp[0])
						
			
			cmds.select(cl = True)


	class JOINTS:
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


	class ANIMATION:
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
		def BakeSelection(DoNotCut=1):
			startTime = cmds.playbackOptions(q=1, min=1)
			endTime = cmds.playbackOptions(q=1, max=1)
			cmds.bakeResults(t=(startTime,endTime), pok=DoNotCut, simulation=1)




#GETools.JOINTS.ScaleCompensate()
#GETools.JOINTS.DrawStyle()
#GETools.LOCATORS.CreateLocators(2, constraint=1)

#GETools.LOCATORS.CreateLocators()
#GETools.LOCATORS.CreateGroups()

#GETools.OTHER.ShowRotateOrder(0)