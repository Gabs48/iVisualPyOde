"""
ivpyode/lib.py
A library of iVisualPyODE objects / assemblies..

Created By:
	James Thomas
	Email: jt@missioncognition.net
	Web: http://missioncognition.net/
	
Arranged for iVisual Python By:
	Gabriel Urbain
	Email: gabriel.urbain@ugent.be
	Web: http://github.com/Gabs48/

Copyright 2015

This file is part of the iVisualPyODE package.

This library is free software; you can redistribute it and/or
modify it under the terms of EITHER:
  (1) The GNU Lesser General Public License as published by the Free
      Software Foundation; either version 2.1 of the License, or (at
      your option) any later version. The text of the GNU Lesser
      General Public License is included with this library in the
      file LICENSE.
  (2) The BSD-style license that is included with this library in
      the file LICENSE-BSD.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the files
LICENSE and LICENSE-BSD for more details. 

Note: See http://pyode.sourceforge.net and https://pypi.python.org/pypi/IVisual/0.1.87
      to get the PyODE and iVisualPython libraries which is required to run this package.
"""

import odelib
import ivpyode

class Piston(ivpyode.GDMFrameAssembly):
    def __init__(self, World, Length, Diameter, MinSpringForce=0, MaxSpringForce=0):
	"""Create a visualized pistion with spring, damping, and actuation properties.
		World: 		The pyode world that this object resides in
		Length: 	The fully extended length of the pistion
		Diameter: 	The diameter of the outer cylinder
		MinSpringForce: The spring force applied at the minimum length position
		MaxSpringForce: The spring force applied at the maximum length position
				Note:	A positive spring force makes the pistons expand
        				A negative spring force makes the pistons contract
	"""

        # Initialize the ivpyode.GDMFrameAssembly class
        ivpyode.GDMFrameAssembly.__init__(self, World)

        self._length = Length # We might want to keep this around

        cylLength = Length / 2.0 # The le3ngth of each cylinder is half of the total.

        # Create the two halves of the piston -- Build it collapsed

        innerCylBody = ivpyode.GDMFrameBody(World)
        innerCylElement = ivpyode.GDMElement(False).DefineCylinder(2000, 0.75 * Diameter, cylLength)
        innerCylBody.AddGDMElement('cyl', innerCylElement)
        innerCylBody.DefineConnectionPoint('Tip', (0, 0, cylLength / 2.0))
        innerCylBody.DefineConnectionPoint('Slider', (0, 0, 0), (0,0,1)) # Along the z-axis

        outerCylBody = ivpyode.GDMFrameBody(World)
        outerCylElement = ivpyode.GDMElement(False).DefineCylinder(2000, Diameter, cylLength)
        outerCylBody.AddGDMElement('cyl', outerCylElement)
        outerCylBody.DefineConnectionPoint('Tip', (0, 0, -cylLength / 2.0))
        outerCylBody.DefineConnectionPoint('Slider', (0, 0, 0), (0,0,1)) # Along the z-axis

        self._linearActuatorJoint = odelib.LinearActuator(World)

        # This order gives us positive slider positions whith fully extended being cylLength
        innerCylBody.Connect(self._linearActuatorJoint, 'Slider', outerCylBody, 'Slider')

        # Add these bodies to the assembly
        self.AddBody('Inner', innerCylBody)
        self.AddBody('Outer', outerCylBody)

        # MinSpringForce is the force you get at MinStop
        # MaxSpringForce is the force you get at MaxStop
        # A positive spring force makes the pistons expand
        # A negative spring force makes the pistons contract
        self._linearActuatorJoint.ChangeProperties(MinSpringForce=MinSpringForce,
                    MaxSpringForce=MaxSpringForce, MinStop=0, MaxStop=cylLength)

    def GetInnerConnectionInfo(self):
        """Get the (body, ID) information for the connection on the inner cylinder's end."""
        return (self.GetBody('Inner'), 'Tip')

    def GetInnerConnectionLocation(self):
        """Get the location of the connection point on the inner cylinder's end."""
        return self.GetBody('Inner').GetConnectionLocation('Tip')

    def GetOuterConnectionInfo(self):
        """Get the (body, ID) information for the connection on the outer cylinder's end."""
        return (self.GetBody('Outer'), 'Tip')

    def GetOuterConnectionLocation(self):
        """Get the location of the connection point on the outer cylinder's end."""
        return self.GetBody('Outer').GetConnectionLocation('Tip')
    
    def PositionInnerTip(self, Position):
        """Reposition the connection point on the tip of the inner cylinder."""
        self.MoveToPlaceConnectionAt('Inner', 'Tip', Position)
    
    def PositionOuterTip(self, Position):
        """Reposition the connection point on the tip of the outer cylinder."""
        self.MoveToPlaceConnectionAt('Outer', 'Tip', Position)



