import maya.cmds as cmds

toggleValue = (0, 1)

cmds.select("test1:cube1", replace = True)

# Extract namespace from selected
selected = cmds.ls(selection = True)[0]
resultNamespace = selected.split(':')[0]
count = selected.split(':')

if (len(count) < 2):
	resultNamespace = None

attributePath = selected + ".translateY"

currentValue = cmds.getAttr(attributePath)
resultValue = None

if (currentValue < toggleValue[0]):
	resultValue = toggleValue[0]

elif (currentValue > toggleValue[1]):
	resultValue = toggleValue[1]

elif (currentValue > toggleValue[0] and currentValue < toggleValue[1]):
	mathResult = currentValue - (toggleValue[1] - toggleValue[0]) / 2
	if (mathResult <= 0):
		resultValue = toggleValue[0]
	else:
		resultValue = toggleValue[1]

elif (currentValue == toggleValue[0]):
	resultValue = toggleValue[1]

elif (currentValue == toggleValue[1]):
	resultValue = toggleValue[0]

cmds.setAttr(attributePath, resultValue)

cmds.select(resultNamespace + ":" + "cube2", replace = True)
		
