import maya.cmds as cmds

def KeysNonkeyableDelete():
	objects = cmds.ls(sl = 1)
	counter = 0
	
	for i in range(len(objects)):
		attributes = cmds.listAttr(objects[i], cb = 1)
		if attributes != None:
			for j in range(len(attributes)):
				cmds.cutKey(objects[i] + "." + attributes[j])
				counter += 1
	
	print ("\t{} nonkeyable detected and deleted".format(counter))