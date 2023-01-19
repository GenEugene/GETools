# GenEugeneTools v0.0.4
# Author Evgeny Gataulin (GenEugene)
# v0.0.4 - 2021.09.29

import maya.cmds as cmds, sys, os

class GETools:
	def __init__(self):
		self.m_windowTitle = "GETools_0_0_4"
		
		self.m_windowWidth = 280
		self.m_numberOfColumns = 2
		self.m_buttonHeight = 25

		self.m_column1 = "mColumn"
		
		self.fr_other = "OTHER"
		self.fr_locators = "LOCATORS"
		self.fr_joints = "JOINTS"
		self.fr_animation = "ANIMATION"
		self.fr_timeline = "TIMELINE"
		
		self.gr_other = "gOTHER"
		self.gr_locators = "gLOCATORS"
		self.gr_joints = "gJOINTS"
		self.gr_animation = "gANIMATION"
		self.gr_timeline = "gTIMELINE"

		self.m_window_name = "mWindowName"
		self.m_windowHeight = 10
	
	


	def resize_UI(self):
		cmds.window(self.m_window_name, e = True, wh = (10, 10), rtf = True)

	def CreateUI(self, createUI=False):
		### WINDOW
		if cmds.window(self.m_window_name, exists = True):
			cmds.deleteUI(self.m_window_name)
			
		cmds.window(self.m_window_name, title = self.m_windowTitle, mxb=0, s=0)
		cmds.window(self.m_window_name, e=True, rtf=True, wh=(self.m_windowWidth, self.m_windowHeight))
		cmds.columnLayout(self.m_column1, rs=10, adj=True)

		###LAYOUTS

		#OTHER
		cmds.frameLayout(self.fr_other, cll=1, p=self.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(self.gr_other, numberOfColumns = self.m_numberOfColumns, cellWidthHeight=(self.m_windowWidth/self.m_numberOfColumns, self.m_buttonHeight), p=self.fr_other)
		#LOCATORS
		cmds.frameLayout(self.fr_locators, cll=1, p=self.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(self.gr_locators, numberOfColumns = 1, cellWidthHeight=(self.m_windowWidth/1, self.m_buttonHeight), p=self.fr_locators)
		#JOINTS
		cmds.frameLayout(self.fr_joints, cll=1, p=self.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(self.gr_joints, numberOfColumns = self.m_numberOfColumns, cellWidthHeight=(self.m_windowWidth/self.m_numberOfColumns, self.m_buttonHeight), p=self.fr_joints)
		#ANIMATION
		cmds.frameLayout(self.fr_animation, cll=1, p=self.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(self.gr_animation, numberOfColumns = 1, cellWidthHeight=(self.m_windowWidth/1, self.m_buttonHeight), p=self.fr_animation)
		#TIMELINE
		cmds.frameLayout(self.fr_timeline, cll=1, p=self.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(self.gr_timeline, numberOfColumns = 5, cellWidthHeight=(self.m_windowWidth/5, self.m_buttonHeight), p=self.fr_timeline)
		

		###BUTTONS
		#OTHER
		cmds.button(l="Rotate order - SHOW", p=self.gr_other, c=("GETools.OTHER.ShowRotateOrder(1)"))
		cmds.button(l="Rotate order - HIDE", p=self.gr_other, c=("GETools.OTHER.ShowRotateOrder(0)"))
		

		#LOCATORS
		cmds.button(l="Create Locators Match", p=self.gr_locators, c=("GETools.LOCATORS.CreateLocators(3)"))	
		cmds.button(l="Create Locators Constraint", p=self.gr_locators, c=("GETools.LOCATORS.CreateLocators(3, constraint=True)"))			
		

		#JOINTS
		cmds.button(l="Joint - BONE", p=self.gr_joints, c=("GETools.JOINTS.DrawStyle(0)"))
		cmds.button(l="Joint - HIDDEN", p=self.gr_joints, c=("GETools.JOINTS.DrawStyle(2)"))
		cmds.button(l="Scale Compensate - ON", p=self.gr_joints, c=("GETools.JOINTS.ScaleCompensate(1)"))
		cmds.button(l="Scale Compensate - OFF", p=self.gr_joints, c=("GETools.JOINTS.ScaleCompensate(0)"))
		

		#ANIMATION
		cmds.button(l="Delete Nonkeyable Keys", p=self.gr_animation, c=("GETools.ANIMATION.DeleteNonkeyableKeys()"))
		cmds.button(l="Delete Keys", p=self.gr_animation, c=("GETools.ANIMATION.DeleteKeys()"))
		

		#TIMELINE
		setTimelineTime3 = GETools.TIMELINE.SetTimelineTime(3)
		setTimelineTime1 = GETools.TIMELINE.SetTimelineTime(1)
		setTimelineTime5 = GETools.TIMELINE.SetTimelineTime(5)
		setTimelineTime2 = GETools.TIMELINE.SetTimelineTime(2)
		setTimelineTime4 = GETools.TIMELINE.SetTimelineTime(4)
		# setTimelineTime4 = GETools.TIMELINE.SetTimelineTime(4)
		#
		cmds.button(l="<<", p=self.gr_timeline, c=setTimelineTime3)
		cmds.button(l="<", p=self.gr_timeline, c=setTimelineTime1)		
		cmds.button(l="ALL", p=self.gr_timeline, c=setTimelineTime5)		
		cmds.button(l=">", p=self.gr_timeline, c=setTimelineTime2)		
		cmds.button(l=">>", p=self.gr_timeline, c=setTimelineTime4)
		# cmds.button(l=">>", p=self.gr_timeline, c=setTimelineTime4)


		### RUN window
		if (createUI):
			cmds.showWindow(self.m_window_name)




	class OTHER:
		def ShowRotateOrder(on=True, *args):
			selected = cmds.ls(sl=1, l=1)
			for i in range(len(selected)):
				cmds.setAttr(selected[i] + ".rotateOrder", cb = on)
		
		def SelectTransformHierarchy(*args):
			cmds.select(hi = True)
			list = cmds.ls(sl = True, typ = "transform", s = False)
			cmds.select(cl = True )
			for i in range(len(list)):
				cmds.select(list[i], add = True)
		
		
	class LOCATORS:
		'''Create locator on selected object with matching'''
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
		def DrawStyle(mode=0):
			selected = cmds.ls(sl=1)
			for i in range(len(selected)):
				cmds.setAttr(selected[i] + ".drawStyle", mode)
		
		'''Joint segment scale compensate'''
		def ScaleCompensate(value=0):
			jointList = cmds.ls(sl=1, typ="joint")
			for i in jointList:
				cmds.setAttr(i + ".segmentScaleCompensate", value)


	class ANIMATION:
		'''Search and clear nonkeyable attributes keys'''
		def DeleteNonkeyableKeys():
			objects = cmds.ls(sl=1)
			counter = 0
			for i in range(len(objects)):
				attributes = cmds.listAttr(objects[i], cb=1)
				if attributes != None:
					for j in range(len(attributes)):
						cmds.cutKey(objects[i] + "." + attributes[j])
						counter += 1
			print ("\t{} nonkeyable detected and deleted".format(counter))


		'''Bake keys'''
		def BakeSelection(DoNotCut=1):
			startTime = cmds.playbackOptions(q=1, min=1)
			endTime = cmds.playbackOptions(q=1, max=1)
			cmds.bakeResults(t=(startTime,endTime), pok=DoNotCut, simulation=1)
			
			
		'''Delete keys'''
		def DeleteKeys():
			mel.eval('timeSliderClearKey')


	class TIMELINE:
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
			if (mode == 6):
				cmds.playbackOptions(ast = cmds.playbackOptions(q=1, min=1))
				cmds.playbackOptions(aet = cmds.playbackOptions(q=1, max=1))
			'''
			#SetTimelineTime(1)
			#SetTimelineTime(2)
			#SetTimelineTime(3)
			#SetTimelineTime(4)
			#SetTimelineTime(5)
			'''


GETOOLS = GETools()
GETOOLS.CreateUI()
# GETOOLS.CreateUI(True)


#GETools.JOINTS.ScaleCompensate()
#GETools.JOINTS.DrawStyle()
#GETools.LOCATORS.CreateLocators(2, constraint=1)
#GETools.LOCATORS.CreateLocators()
#GETools.LOCATORS.CreateGroups()
#GETools.OTHER.ShowRotateOrder(0)