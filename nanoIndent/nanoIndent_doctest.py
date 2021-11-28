"""

Example for Aglient G200 file and ISO indentation test method
=================

.. doctest::

	>>> from nanoIndent import Tip, Indentation

	>>> i = Indentation(".../ExperimentalMicromechanics-master/Examples/Agilent/CSM.xls")
	=============  .../ExperimentalMicromechanics-master/Examples/Agilent/CSM.xls  ============
     	Displacement Into Surface      : h                    
     	Load On Sample                 : p                    
     	Time On Sample                 : t                    
     	Harmonic Contact Stiffness     : slope                
     	Hardness                       : hardness             
     	Modulus                        : modulus              
     	Contact Area                   : A_c                  
     	Contact Depth                  : h_c                  
 	*** CSM Status                     NOT USED
     	Harmonic Displacement          : hHarmonic            
 	*** Harmonic Frequency             NOT USED
     	Harmonic Load                  : pHarmonic            
     	Harmonic Stiffness             : slopeInvalid         
     	Load vs Disp Slope             : pVsHSlope            
     	Phase Angle                    : phaseAngle           
     	Raw Displacement               : hRaw                 
     	Raw Load                       : pRaw                 
     	Reduced Modulus                : modulusRed           
     	Stiffness Squared Over Load    : k2p                  
     	Support Spring Stiffness       : slopeSupport         
     	Time                           : tTotal               
     	X Position                     : xCoarse              
     	Y Position                     : yCoarse              
	*WARNING* identifyLoadHoldUnload: cut two from end of unloadIdx: UNDESIRED
	Number Unloading segments 1

	>>> i.nuMat = 0.2 # nuMat is the Poisson‘s ratio of material

	>>> i.plotTestingMethod() # Plot testing method

.. _Test_Method:
.. figure:: ../source/img/test_method.png
  :width: 400
  :align: center
  :alt: Alternative text

  Test method

.. doctest::

	>>> i.plot()
	Stiffness:232.4mN/um   hMax:0.4013um    pMax:20.09mN
	E*:       120.6GPa     A:   2.9157um2    hc: 0.3365um
	E:        129.4GPa     H:   6.9GPa
	Number of unloading segments:1  Method:Method.ISO
	<AxesSubplot:xlabel='depth [$\\mu m$]', ylabel='force [$mN$]'>

.. _Indentation_curve:
.. figure:: ../source/img/indentation_curve.png
  :width: 400
  :align: center
  :alt: Alternative text

  Indentation curve

.. doctest::

	>>> i.verifyReadCalc() # Error calculation
	Error in hc: 0.000e+00 % between 3.365e-01 and 3.365e-01
	Error in Ac: 9.976e-04 % between 2.916e+00 and 2.916e+00
	Error in E*: 4.988e-04 % between 1.206e+02 and 1.206e+02
	Error in E:  1.087e-02 % between 1.294e+02 and 1.294e+02
	Error in H:  9.976e-04 % between 6.890e+00 and 6.890e+00

	>>> S = i.stiffnessFromUnloading(i.p, i.h, plot = False) # Calculate single stiffness according to unloading data
	Number of unloading segments:1  Method:Method.ISO

	>>> print("Error in stiffness: %.2e"%((i.slope[0] - S[0])/S[0])) 
	Error: -3.23e-04

Attention: error << 1% means it is small compared to the values itself


Example for Hysitron file and ISO indentation test method
=================

.. doctest::

	>>> from nanoIndent import Tip, Indentation
	
	>>> i = Indentation("....../ExperimentalMicromechanics-master/Examples/Hysitron/Exp-50mN_0000.hld")
	Open Hysitron file: ....../ExperimentalMicromechanics-master/Examples/Hysitron/Exp-50mN_0000.hld
	
	>>> i.analyse()
	Number of unloading segments:1  Method:Method.ISO

	>>> i.plot()
	Stiffness:153.3mN/um   hMax:0.5755um    pMax:50.07mN
	E*:       106.4GPa     A:   1.6318um2    hc: 0.3306um
	E:        106.7GPa     H:   30.7GPa
	Number of unloading segments:1  Method:Method.ISO
	<AxesSubplot:xlabel='depth [$\\mu m$]', ylabel='force [$mN$]'>
	
	>>> i.verifyReadCalc()
	Error in hc: 0.000e+00 % between 3.306e-01 and 3.306e-01
	Error in Ac: 0.000e+00 % between 1.632e+00 and 1.632e+00
	Error in E*: 0.000e+00 % between 1.064e+02 and 1.064e+02
	Error in E:  0.000e+00 % between 1.067e+02 and 1.067e+02
	Error in H:  0.000e+00 % between 3.068e+01 and 3.068e+01
"""
