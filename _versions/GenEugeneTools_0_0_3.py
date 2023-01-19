# GenEugeneTools v0.0.3
################################################################################

### Import ###
import maya.cmds as cmds, sys, os

### Class ###
class GETools:
	m_windowTitle = "GETools_0_0_3"
	
	
	m_windowWidth = 280
	m_numberOfColumns = 2
	m_buttonHeight = 25


	m_column1 = "mColumn"
	
	
	fr_other = "OTHER"
	fr_locators = "LOCATORS"
	fr_joints = "JOINTS"
	fr_animation = "ANIMATION"
	fr_timeline = "TIMELINE"
	
	gr_other = "gOTHER"
	gr_locators = "gLOCATORS"
	gr_joints = "gJOINTS"
	gr_animation = "gANIMATION"
	gr_timeline = "gTIMELINE"


	m_window_name = "mWindowName"
	m_windowHeight = 10
	
	
	
	
	@staticmethod
	def resize_UI():
		cmds.window(GETools.m_window_name, e = True, wh = (10, 10), rtf = True)

	@staticmethod
	def CreateUI(createUI=False):
		### WINDOW
		if cmds.window(GETools.m_window_name, exists = True):
			cmds.deleteUI(GETools.m_window_name)
			
		cmds.window(GETools.m_window_name, title = GETools.m_windowTitle, mxb=0, s=0)
		cmds.window(GETools.m_window_name, e=True, rtf=True, wh=(GETools.m_windowWidth, GETools.m_windowHeight))
		cmds.columnLayout(GETools.m_column1, rs=10, adj=True)

		###LAYOUTS
		#OTHER
		cmds.frameLayout(GETools.fr_other, cll=1, p=GETools.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(GETools.gr_other, numberOfColumns = GETools.m_numberOfColumns, cellWidthHeight=(GETools.m_windowWidth/GETools.m_numberOfColumns, GETools.m_buttonHeight), p=GETools.fr_other)
		#LOCATORS
		cmds.frameLayout(GETools.fr_locators, cll=1, p=GETools.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(GETools.gr_locators, numberOfColumns = 1, cellWidthHeight=(GETools.m_windowWidth/1, GETools.m_buttonHeight), p=GETools.fr_locators)
		#JOINTS
		cmds.frameLayout(GETools.fr_joints, cll=1, p=GETools.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(GETools.gr_joints, numberOfColumns = GETools.m_numberOfColumns, cellWidthHeight=(GETools.m_windowWidth/GETools.m_numberOfColumns, GETools.m_buttonHeight), p=GETools.fr_joints)
		#ANIMATION
		cmds.frameLayout(GETools.fr_animation, cll=1, p=GETools.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(GETools.gr_animation, numberOfColumns = 1, cellWidthHeight=(GETools.m_windowWidth/1, GETools.m_buttonHeight), p=GETools.fr_animation)
		#TIMELINE
		cmds.frameLayout(GETools.fr_timeline, cll=1, p=GETools.m_column1, bv=1, cc="GETools.resize_UI()")
		cmds.gridLayout(GETools.gr_timeline, numberOfColumns = 5, cellWidthHeight=(GETools.m_windowWidth/5, GETools.m_buttonHeight), p=GETools.fr_timeline)
		
		
		###BUTTONS
		#OTHER
		cmds.button(l="Rotate order - SHOW", p=GETools.gr_other, c=("GETools.OTHER.ShowRotateOrder(1)"))
		cmds.button(l="Rotate order - HIDE", p=GETools.gr_other, c=("GETools.OTHER.ShowRotateOrder(0)"))
		
		#LOCATORS
		cmds.button(l="Create Locators Match", p=GETools.gr_locators, c=("GETools.LOCATORS.CreateLocators(3)"))	
		cmds.button(l="Create Locators Constraint", p=GETools.gr_locators, c=("GETools.LOCATORS.CreateLocators(3, constraint=True)"))			
		
		#JOINTS
		cmds.button(l="Joint - BONE", p=GETools.gr_joints, c=("GETools.JOINTS.DrawStyle(0)"))
		cmds.button(l="Joint - HIDDEN", p=GETools.gr_joints, c=("GETools.JOINTS.DrawStyle(2)"))
		cmds.button(l="Scale Compensate - ON", p=GETools.gr_joints, c=("GETools.JOINTS.ScaleCompensate(1)"))
		cmds.button(l="Scale Compensate - OFF", p=GETools.gr_joints, c=("GETools.JOINTS.ScaleCompensate(0)"))
		
		#ANIMATION
		cmds.button(l="Delete Nonkeyable Keys", p=GETools.gr_animation, c=("GETools.ANIMATION.DeleteNonkeyableKeys()"))
		cmds.button(l="Delete Keys", p=GETools.gr_animation, c=("GETools.ANIMATION.DeleteKeys()"))
		
		#TIMELINE
		cmds.button(l="<<", p=GETools.gr_timeline, c=("GETools.TIMELINE.SetTimelineTime(3)"))
		cmds.button(l="<", p=GETools.gr_timeline, c=("GETools.TIMELINE.SetTimelineTime(1)"))		
		cmds.button(l="ALL", p=GETools.gr_timeline, c=("GETools.TIMELINE.SetTimelineTime(5)"))		
		cmds.button(l=">", p=GETools.gr_timeline, c=("GETools.TIMELINE.SetTimelineTime(2)"))		
		cmds.button(l=">>", p=GETools.gr_timeline, c=("GETools.TIMELINE.SetTimelineTime(4)"))


		### RUN window
		if (createUI):
			cmds.showWindow(GETools.m_window_name)




	class OTHER:
		@staticmethod
		def ShowRotateOrder(on=True):
			selected = cmds.ls(sl=1, l=1)
			for i in range(len(selected)):
				cmds.setAttr(selected[i] + ".rotateOrder", cb = on)
		
		
		@staticmethod		
		def SelectTransformHierarchy():
			cmds.select(hi = True)
			list = cmds.ls(sl = True, typ = "transform", s = False)
			cmds.select(cl = True )
			for i in range(len(list)):
				cmds.select(list[i], add = True)
		
		
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
		@staticmethod
		def BakeSelection(DoNotCut=1):
			startTime = cmds.playbackOptions(q=1, min=1)
			endTime = cmds.playbackOptions(q=1, max=1)
			cmds.bakeResults(t=(startTime,endTime), pok=DoNotCut, simulation=1)
			
			
		'''Delete keys'''
		@staticmethod
		def DeleteKeys():
			mel.eval('timeSliderClearKey')


	class TIMELINE:		
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




#GETools.JOINTS.ScaleCompensate()
#GETools.JOINTS.DrawStyle()
#GETools.LOCATORS.CreateLocators(2, constraint=1)
#GETools.LOCATORS.CreateLocators()
#GETools.LOCATORS.CreateGroups()
#GETools.OTHER.ShowRotateOrder(0)