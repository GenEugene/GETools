# GETools v0.1.2 (GenEugene Tools)
# Author Evgeny (GenEugene) Gataulin tek94@mail.ru tek942@gmail.com
# Maya 2017-2022
# https://github.com/GenEugene/Overlappy

import maya.cmds as cmds, sys, os
import maya.mel as mel
from datetime import datetime
from inspect import currentframe, getframeinfo

# sys.exit()

class GETOOLS_class:
	### COLORS
	cRed = [1, .5, .5]
	cOrange = [1, .6, .3]
	cYellow = [1, 1, .5]
	cGreen = [.6, 1, .6]
	cLBlue = [.4, .8, 1]
	cBlue = [.3, .7, 1]
	cPurple = [.81, .4, 1]
	cWhite = [1, 1, 1]
	cGray = [.5, .5, .5]

	def __init__(self):
		### SETUP
		self.titleText = "GETools v0.1.2"
		self.windowWidth = 300
		self.lineHeight = 26

		### WINDOW
		self.window_name = "GEToolsWindow"
		self.windowHeight = 20
		self.defaultTab = 2
		self.tabs = None
		#
		self.tabTools = None
		self.tabOverlappy = None

	def CreateUI(self):
		# WINDOW
		if cmds.window(self.window_name, exists = True):
			cmds.deleteUI(self.window_name)
		cmds.window(self.window_name, title = self.titleText, mxb = 0, s = 0)
		cmds.window(self.window_name, e = True, rtf = True, wh = (self.windowWidth, self.windowHeight))
		cmds.columnLayout(adj = True, h = self.windowHeight)


		# HEAD MENU
		cmds.menuBarLayout()

		cmds.menu(label = 'Scene')
		cmds.menuItem(label = 'Reload', c = "GETOOLS.SceneReload()")
		# cmds.menuItem(c = "print('to shelf')", optionBox=1)
		cmds.menuItem(label = 'Close MAYA', c = "GETOOLS.SceneClose()")
		# cmds.menuItem(c = "print('to shelf')", optionBox=1)

		cmds.menu(label = 'Script')
		cmds.menuItem(label = 'Reload', c = "GETOOLS.Restart()")
		# cmds.menuItem(c = "print('to shelf')", optionBox = 1)

		# cmds.menu(label = 'Help', helpMenu = True)
		# cmds.menuItem(label = 'About...', en = 1, c = "cmds.launch(web = '')")

		# cmds.menu(label = 'Test')
		# cmds.menuItem(label = 'Test', c = "print('test')")
		# cmds.menuItem(c = "print('to shelf')", optionBox = 1)


		# TABS
		self.tabs = cmds.tabLayout(innerMarginWidth = 10, innerMarginHeight = 10, cc = self.TabHide)

		self.tabTools = cmds.columnLayout("Tools", p = self.tabs)
		self.tabOverlappy = cmds.columnLayout("Overlappy", p = self.tabs)
		# other tabs...
		# other tabs...
		# other tabs...

		# RUN WINDOW
		cmds.showWindow(self.window_name)
		self.Resize_UI()
		cmds.tabLayout(self.tabs, e = 1, sti = self.defaultTab)

	def Resize_UI(self, *args):
		cmds.window(self.window_name, e = True, h = self.windowHeight, rtf = True)
		# cmds.window(self.window_name, e = True, wh = (self.windowWidth, self.windowHeight), rtf = True)

	def TabHide(self, *args):
		id = cmds.tabLayout(self.tabs, q = 1, selectTabIndex = 1)
		children = cmds.tabLayout(self.tabs, q = 1, childArray = 1)
		for i in range(len(children)):
			ii = i + 1
			if(ii == id):
				cmds.columnLayout(children[i], e = 1, vis = 1)
				ch = cmds.columnLayout(children[i], q = 1, childArray = 1)
				if(ch):
					for y in range(len(ch)):
						cmds.frameLayout(ch[y], e = 1, vis = 1)
				# else:
				# 	cmds.warning("NO TAB CHILDREN")
			else:
				cmds.columnLayout(children[i], e = 1, vis = 0)
				ch = cmds.columnLayout(children[i], q = 1, childArray = 1)
				if(ch):
					for y in range(len(ch)):
						cmds.frameLayout(ch[y], e = 1, vis = 0)
		self.Resize_UI()
	
	def NamespacesFromSelected(self, *args):
		selected = cmds.ls(sl = 1)
		if(selected):
			namespaces = list("")
			for i in range(len(selected)):
				namespace = selected[i].split(':')[0]
				
				# Empty namespace
				count = selected[i].split(':')
				if(len(count) < 2):
					namespace = ""
				
				for i in range(len(selected)):
					if(namespace not in namespaces):
						namespaces.append(namespace)

			return selected, namespaces
		else:
			return None, None

	def SceneReload(self, *args):
		currentScene = cmds.file(q = True, sceneName = True)
		if(currentScene):
			cmds.file(currentScene, open = True, force = True)
		else:
			cmds.file(new = 1, f = 1)
	
	def SceneClose(self, *args):
		cmds.quit(force = True)
	

	### MODULES
	# TOOLS v0.0.4
	class TOOLS_class:
		def SetupUI(self, _GETOOLS=None):
			layoutParent = _GETOOLS.tabTools
			width = _GETOOLS.windowWidth
			height = _GETOOLS.lineHeight
			resizeCommandText = "GETOOLS" + ".Resize_UI()"


			# OTHER
			orderOn = "GETOOLS.TLS.OTHER.ShowRotateOrder(1)"
			orderOff = "GETOOLS.TLS.OTHER.ShowRotateOrder(0)"
			#
			cmds.frameLayout(l = "OTHER", cll = 1, p = layoutParent, bv = 1, cc = resizeCommandText)
			cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (width/2, height))
			cmds.button(l = "Rotate order - SHOW", c = orderOn, bgc = GETOOLS_class.cGreen)
			cmds.button(l = "Rotate order - HIDE", c = orderOff, bgc = GETOOLS_class.cWhite)
			

			# LOCATORS
			locMatch = "GETOOLS.TLS.LOCATORS.CreateLocators(3)"
			locConstr = "GETOOLS.TLS.LOCATORS.CreateLocators(3, constraint=True)"
			#
			cmds.frameLayout(l = "LOCATORS", cll = 1, p = layoutParent, bv = 1, cc = resizeCommandText)
			cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (width/2, height))
			cmds.button(l = "Create Locators Match", c = locMatch, bgc = GETOOLS_class.cWhite)	
			cmds.button(l = "Create Locators Constraint", c = locConstr, bgc = GETOOLS_class.cWhite)			
			

			# JOINTS
			jointBone = "GETOOLS.TLS.JOINTS.DrawStyle(0)"
			jointHidden = "GETOOLS.TLS.JOINTS.DrawStyle(2)"
			scaleCompOn = "GETOOLS.TLS.JOINTS.ScaleCompensate(1)"
			scaleCompOff = "GETOOLS.TLS.JOINTS.ScaleCompensate(0)"
			#
			cmds.frameLayout(l = "JOINTS", cll = 1, p = layoutParent, bv = 1, cc = resizeCommandText)
			cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (width/2, height))
			cmds.button(l = "Joint - BONE", c = jointBone, bgc = GETOOLS_class.cWhite)
			cmds.button(l = "Joint - HIDDEN", c = jointHidden, bgc = GETOOLS_class.cWhite)
			cmds.button(l = "Scale Compensate - ON", c = scaleCompOn, bgc = GETOOLS_class.cWhite)
			cmds.button(l = "Scale Compensate - OFF", c = scaleCompOff, bgc = GETOOLS_class.cGreen)
			

			# ANIMATION
			deleteNonkeyable = "GETOOLS.TLS.ANIMATION.DeleteNonkeyableKeys()"
			deleteKeys = "GETOOLS.TLS.ANIMATION.DeleteKeys()"
			#
			cmds.frameLayout(l = "ANIMATION", cll = 1, p = layoutParent, bv = 1, cc = resizeCommandText)
			cmds.gridLayout(numberOfColumns = 1, cellWidthHeight = (width/1, height))
			cmds.button(l = "Delete Nonkeyable Keys", c = deleteNonkeyable, bgc = GETOOLS_class.cGreen)
			cmds.button(l = "Delete Keys", c = deleteKeys, bgc = GETOOLS_class.cWhite)
			

			# TIMELINE
			setTimelineTime3 = 'GETOOLS.TLS.TIMELINE.SetTimelineTime(3)'
			setTimelineTime1 = 'GETOOLS.TLS.TIMELINE.SetTimelineTime(1)'
			setTimelineTime5 = 'GETOOLS.TLS.TIMELINE.SetTimelineTime(5)'
			setTimelineTime6 = 'GETOOLS.TLS.TIMELINE.SetTimelineTime(6)'
			setTimelineTime2 = 'GETOOLS.TLS.TIMELINE.SetTimelineTime(2)'
			setTimelineTime4 = 'GETOOLS.TLS.TIMELINE.SetTimelineTime(4)'
			#
			cmds.frameLayout(l = "TIMELINE", cll = 1, p = layoutParent, bv = 1, cc = resizeCommandText)
			cmds.gridLayout(numberOfColumns = 6, cellWidthHeight = (width/6, height))
			cmds.button(l = "<<", c = setTimelineTime3, bgc = GETOOLS_class.cWhite)
			cmds.button(l = "<", c = setTimelineTime1, bgc = GETOOLS_class.cWhite)
			cmds.button(l = "ALL+", c = setTimelineTime5, bgc = GETOOLS_class.cWhite)
			cmds.button(l = "ALL-", c = setTimelineTime6, bgc = GETOOLS_class.cWhite)
			cmds.button(l = ">", c = setTimelineTime2, bgc = GETOOLS_class.cWhite)
			cmds.button(l = ">>", c = setTimelineTime4, bgc = GETOOLS_class.cWhite)


		class OTHER:
			@staticmethod
			def ShowRotateOrder(on=True, *args):
				selected = cmds.ls(sl=1, l=1)
				for i in range(len(selected)):
					cmds.setAttr(selected[i] + ".rotateOrder", cb = on)
			
			@staticmethod
			def SelectTransformHierarchy(*args):
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
		
		class JOINTS:
			'''Set joints draw style'''
			@staticmethod
			def DrawStyle(mode=0):
				selected = cmds.ls(sl = 1)
				for i in range(len(selected)):
					cmds.setAttr(selected[i] + ".drawStyle", mode)
			
			'''Joint segment scale compensate'''
			@staticmethod
			def ScaleCompensate(value=0):
				jointList = cmds.ls(sl = 1, typ = "joint")
				for i in jointList:
					cmds.setAttr(i + ".segmentScaleCompensate", value)

		class ANIMATION:
			'''Search and clear nonkeyable attributes keys'''
			@staticmethod
			def DeleteNonkeyableKeys():
				objects = cmds.ls(sl = 1)
				counter = 0
				for i in range(len(objects)):
					attributes = cmds.listAttr(objects[i], cb = 1)
					if attributes != None:
						for j in range(len(attributes)):
							cmds.cutKey(objects[i] + "." + attributes[j])
							counter += 1
				print ("\t{} nonkeyable detected and deleted".format(counter))

			'''Bake keys'''
			@staticmethod
			def BakeSelection(DoNotCut=1):
				startTime = cmds.playbackOptions(q = 1, min = 1)
				endTime = cmds.playbackOptions(q = 1, max = 1)
				cmds.bakeResults(t = (startTime,endTime), pok = DoNotCut, simulation = 1)
				
			'''Delete keys'''
			@staticmethod
			def DeleteKeys():
				mel.eval('timeSliderClearKey')

		class TIMELINE:
			@staticmethod
			def SetTimelineTime(mode=0):
				_current = cmds.currentTime(q = 1)
				if (mode == 1):
					cmds.playbackOptions(min = _current)
				elif (mode == 2):
					cmds.playbackOptions(max = _current)
				elif (mode == 3):
					cmds.playbackOptions(ast = _current)
				elif (mode == 4):
					cmds.playbackOptions(aet = _current)
				elif (mode == 5):
					cmds.playbackOptions(min = cmds.playbackOptions(q = 1, ast = 1))
					cmds.playbackOptions(max = cmds.playbackOptions(q = 1, aet = 1))
				elif (mode == 6):
					cmds.playbackOptions(ast = cmds.playbackOptions(q = 1, min = 1))
					cmds.playbackOptions(aet = cmds.playbackOptions(q = 1, max = 1))
	
	
	### EXECUTION
	@staticmethod
	def Start():
		GETOOLS.CreateUI()

		GETOOLS.TLS = GETOOLS.TOOLS_class()
		GETOOLS.TLS.SetupUI(GETOOLS)

		GETOOLS.TabHide()
	
	@staticmethod
	def Restart():
		cmds.evalDeferred("GETOOLS.Start()")

GETOOLS = GETOOLS_class()
GETOOLS.Start()