m_attrName = "_rotateOrder"

selection = cmds.ls(sl=1, sn=1)
for obj in selection:
	_name = obj.split(":")
	_finalName = _name[1] + m_attrName
	try:
		cmds.cutKey(_finalName, cl=1)
		print("OK: " + obj)
	except:
		print("skip: " + obj)