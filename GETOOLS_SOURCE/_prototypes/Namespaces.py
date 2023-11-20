import maya.cmds as cmds

def ClearRigNamespaces(_namespace=''):
	rigNamespace = _namespace # Filename of rig (.mb)
	
	refs = cmds.ls(type = 'reference')
	for i in range(len(refs)):
		if (refs[i][0:-2] == rigNamespace):
			rFile = cmds.referenceQuery(refs[i], f=True)
			cmds.file(rFile, importReference=True) # Import reference
	
	name2 = ':' + rigNamespace
	cmds.namespace( rm = name2, mnr = True) # Remove namespace
	
	cmds.setAttr('Main.jointVis', 1 ) # Show root joint
	cmds.setAttr('MotionSystem.visibility', 1 ) # Show controls
	cmds.setAttr('_controllers.visibility', 1 ) # Set visibility to controls layer
	cmds.select("SET_EXPORT_ANIM_ALL", r=1) # Select all objects for baking

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
