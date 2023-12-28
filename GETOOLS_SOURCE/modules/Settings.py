# Copyright 2023 by Eugene Gataulin (GenEugene). All Rights Reserved.

from GETOOLS_SOURCE.utils import Colors

windowName = "windowGETools"
dockName = "dockGETools"
dockAllowedAreas = ["left", "right"]
dockStartArea = dockAllowedAreas[0] # start docking state, 0 - left, 1 - right

windowHeight = 500 # vertical window size when undocked
windowWidth = 280
windowWidthScrollSpace = 20
lineHeight = 24
margin = 2

sliderWidth = (60, 54, 10)
sliderWidthMarker = 14

windowWidthScroll = windowWidth - windowWidthScrollSpace
windowWidthMargin = windowWidthScroll - margin * 2

frames1Color = Colors.blackWhite00
frames2Color = Colors.blackWhite20
frames2Prefix = "//  "

