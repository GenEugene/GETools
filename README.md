# GETools
Autodesk Maya animation and rigging tool

---

# Description
The idea is to mix all my scripts to one tool. I have a lot small and very useful algorithms, Overlappy script for secondary animation and other. So, when it will be done, I will rewrite this description and add instruction for use.

Also plan to create video tutorial about features and how to use them.

---

# Feature list:
- #### Dropdown menu
	- Fast reload current scene (without save popup)
	- Fast quit maya application (without save popup)
	- Collapse/Expand all frames
	- Dock window left, right or undock
- #### Tools
	- Select Transform hierarchy
	- Locators creation with different baking animation modes
	- Multiple Constraints 
	- Multiple Copy Skin Weights
	- Multiple Rotate Order visibility edit
	- Multiple Joint Segment Scale Compensate edit
	- Multiple Joint Draw Style edit
	- Bake Classic with cut option
	- Bake Custom (alternative baking, works with additional layers)
	- Bake Selected objects by last object (keep relative positions)
	- Delete all animation on selected objects
	- Delete key range on selected objects
	- Delete Nonkeyable keys on selected objects
	- Timeline range manipulator
- #### Overlappy
	- Works fast with all selected objects in order
	- nParticle based (full particle settings control)
	- Translate bake
	- Rotate bake
	- Scale bake (not implemented yet)
	- Baking on override layers
	- Hierarchy mode
	- Loop mode
- #### Center Of Mass
	- Point Constrain based
	- Extra projections on XYZ planes
	- Humanoid weights preset
	- Custom weights
	- Ability to animate weights to achieve specific goals like lifting heavy objects
	- Fast baking tools to be focused on animation
- #### Experimental
	- Multiple Motion Trail (simplified Maya's motion trail)

---

# Known issues:
- Overlappy module may be unstable
- Undocking resets all values
- Folding issue with CenterOfMass/Weights