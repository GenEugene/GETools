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

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene
# Source code: https://github.com/GenEugene/GETools or https://app.gumroad.com/geneugene

from .utils import Colors


# Interface
buttonLabel = "GETools"
windowName = "windowGETools"
dockName = "dockGETools"
dockAllowedAreas = ("left", "right")
dockStartArea = dockAllowedAreas[0] # start docking state, 0 - left, 1 - right
windowHeight = 500 # vertical window size when undocked
windowWidth = 300
windowWidthScrollSpace = 20
lineHeight = 24
margin = 2
sliderWidth = (60, 54, 10)
sliderWidthMarker = 14
windowWidthScroll = windowWidth - windowWidthScrollSpace
windowWidthMargin = windowWidthScroll - margin * 2
frames1Color = Colors.blackWhite13
frames2Color = Colors.blackWhite20
frames2Prefix = "//  "
presetsPath = "/GETOOLS_SOURCE/PRESETS/"

# Default values
checkboxEulerFilter = False # automatic euler filter checkbox

