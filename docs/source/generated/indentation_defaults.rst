.. This file is generated from micromechanics/indentation/definitions.py by docs/source/conf.py.
.. Do not edit it manually.

Default Model
-------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Key
     - Default
     - Description
   * - nuTip
     - 0.07
     - 
   * - modulusTip
     - 1140
     - GPa from Oliver,Pharr Method paper
   * - beta
     - 0.75
     - beta: contact depth coefficient
   * - nonMetal
     - 1
     - switch between metal=0 and nonMetal=amorphous=default=1.
   * - driftRate
     - 0
     - drift rate in [um/s]
   * - unloadPMax
     - 0.99
     - upper end of fitting domain of unloading stiffness: Vendor-specific change
   * - unloadPMin
     - 0.5
     - lower end of fitting domain of unloading stiffness: Vendor-specific change
   * - unloadInitialM
     - -1
     - initial value of m that is used to determine the initial values of B and hf, which are then used to fit the unloading curve. 1<m0<10, if -1 then best m0 is automatically identified
   * - relForceRateNoise
     - 0.02
     - threshold of dp/dt use to identify start of loading: Vendor-specific change
   * - relForceRateNoiseFilter
     - 'median'
     - 
   * - forceNoise
     - 0.001
     - threshold force to identify start of loading
   * - evaluateSAtMax
     - True
     - evaluate stiffness at maximum or at end of power-law fit domain
   * - maxSizeFluctuations
     - 10
     - maximum size of small fluctuations that are removed in identifyLoadHoldUnload
   * - cropSlopeToLoading
     - True
     - crop the slope to the domain between the surface and loading, after those are identified

Vendor Dependent Defaults
--------------------------

.. list-table::
   :header-rows: 1

   * - Vendor
     - unloadPMax
     - unloadPMin
     - relForceRateNoise
     - Description
   * - Agilent
     - 0.999
     - 0.5
     - 0.02
     - 
   * - Hysitron
     - 0.95
     - 0.4
     - 0.2
     - 
   * - Micromaterials
     - 0.99
     - 0.5
     - 0.02
     - 
   * - FischerScope
     - 0.95
     - 0.21
     - 0.01
     - 
   * - Hdf5
     - 0.99
     - 0.5
     - 0.02
     - 
   * - AgilentHDF5
     - 0.99
     - 0.5
     - 0.02
     - 
   * - KLAHDF5
     - 0.99
     - 0.5
     - 0.007
     - enhanced accuracy
   * - FischerScopeHDF5
     - 0.99
     - 0.21
     - 0.02
     - reduced accuracy
   * - MicromaterialsHDF5
     - 0.99
     - 0.5
     - 0.02
     - 
   * - HysitronHDF5
     - 0.99
     - 0.5
     - 0.04
     - 
   * - FemtotoolsHDF5
     - 0.99
     - 0.5
     - 0.04
     - 
   * - SurfaceHDF5
     - 0.99
     - 0.5
     - 0.04
     - 

Default Output
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Key
     - Default
     - Description
   * - verbose
     - 2
     - the higher, the more information printed: 2=default, 1=minimal, 0=print nothing
   * - plotLoadHoldUnload
     - False
     - plot intermediate steps; helpful for debugging
   * - ax
     - None
     - matplotlib axis to use for plotting
   * - plotWithLabel
     - False
     - plot legend
   * - progressBar
     - None
     - callback function to use for plotting progress bar f(value, location)
   * - successTest
     - []
     - list of all test with valid load-hold-unload sequence

Default Surface
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Key
     - Default
     - Description
   * - surfaceIdx
     - {}
     - 
