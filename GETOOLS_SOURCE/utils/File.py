# GETOOLS is under the terms of the MIT License
# Copyright (c) 2018-2024 Eugene Gataulin (GenEugene). All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene https://discord.gg/heMxJhTqCz
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

import os
import ast # For safely converting strings to Python objects
import maya.cmds as cmds


_basicFileDialogFilter = "*.txt"
_dialogStyle = 2


def SaveLogic(filepath, variablesDictionary, title="", *args): # TODO MERGE PATH CHECK LOGIC
	### Extract the directory from the provided file path
	directory = os.path.dirname(filepath)
	
	### Check if the directory exists; if not, create it
	if not os.path.exists(directory):
		os.makedirs(directory) # Create the directory, including any intermediate directories
	
	with open(filepath, 'w') as line:
		if (title != ""):
			line.write("{0}\n\n".format(title))
		for var_name, var_value in variablesDictionary.items():
			line.write("{0} = {1}\n".format(var_name, var_value))
def SaveDialog(startingDirectory, variablesDict, title="", *args):
	fileDialog = cmds.fileDialog2(fileMode = 0, startingDirectory = startingDirectory, fileFilter = _basicFileDialogFilter, dialogStyle = _dialogStyle)
	if fileDialog is None:
		return
	SaveLogic(fileDialog[0], variablesDict, title = title)
	print("File Saved {0}".format(fileDialog))

def ReadLogic(filepath, *args):
	variablesDictionary = {}

	### Check if file exists
	if not os.path.exists(filepath):
		print("File \"{0}\" not found!".format(filepath))
		return None

	### Open the file in read mode
	with open(filepath, 'r') as f:
		for line in f:
			### Parse each line in the format "name = value"
			if " = " in line:
				var_name, var_value = line.strip().split(" = ", 1)
				
				try:
					### Use ast.literal_eval to convert strings to proper Python objects (int, float, list, etc.)
					var_value = ast.literal_eval(var_value)
				except (ValueError, SyntaxError):
					### If literal_eval fails, keep it as a string
					pass
				
				# Store the variable in the dictionary
				variablesDictionary[var_name] = var_value

	### Set the variables in the global namespace
	globals().update(variablesDictionary)
	print("Variables loaded from {0}".format(filepath))
	return variablesDictionary, filepath
def ReadDialog(startingDirectory, *args):
	fileDialog = cmds.fileDialog2(fileMode = 1, startingDirectory = startingDirectory, fileFilter = _basicFileDialogFilter, dialogStyle = _dialogStyle)
	if fileDialog is None:
		return
	readResult = ReadLogic(fileDialog[0])
	print("File Read {0}".format(readResult))
	return readResult

