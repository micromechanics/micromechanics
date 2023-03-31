Welcome to micromechanics' documentation
****************************************

This library allows to read datafiles from different nanoindenters and allows to analyse it by evaluating the hardness and Young's modulus using the Oliver-Pharr method. It also includes functions for frame stiffness and area function calibration as well as a number of plotting functions. Additionally the library allows to read SEM images and optimize them

The library can read:

- xls files from the vendors MTS, Agilent, Keysight, which produced the XP and G200 indenters
- hap files from the Fischer-Scope
- zip-files which include all the files of the Micromaterials NanoXtreme
- some common format which is based on the NeXus common data format
- Tif images from Zeiss and FEI/ThermoFischer

Tutorials
=========

.. toctree::
   :maxdepth: 1

   installation
   tutorialBasic
   tutorialAdvanced
   tutorialTif

Libraries
=========

.. toctree::
   :maxdepth: 1

   nanoindentation
   tip
   tif


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
