import os
import sys

scriptPath = "C:\MyFiles\Personal\Repositories\GETools\TOOLS"

if not os.path.exists(scriptPath):
	raise IOError(r'The source path {0} does not exist!'.format(scriptPath))
	
if scriptPath not in sys.path:
	sys.path.insert(0, scriptPath)


### TEST ZONE ###
# import experimental.GeneralWindow as gtwindow
# gtwindow.GeneralWindow().RUN()

# import scripts.old_GETools as oldget
# oldget.GETOOLS_class().Start()

# import scripts.Tools as tls
# tls.Tools().RUN()

# import scripts.CenterOfMass as com
# com.CenterOfMass().RUN()

# import experimental.TESTING as testing
# testing.TEST_PRINT_1()

def onMayaDroppedPythonFile(*args, **kwargs):
	print("TODO| dropped python file empty function")