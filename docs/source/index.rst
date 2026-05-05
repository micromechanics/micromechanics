Welcome to micromechanics' documentation
****************************************

This library allows to read datafiles from different nanoindenters and allows to analyse it by evaluating the hardness and Young's modulus using the Oliver-Pharr method. It also includes functions for frame stiffness and area function calibration as well as a number of plotting functions. Additionally the library allows to read SEM images and optimize them

The library can read:

- xls files from the vendors MTS, Agilent, Keysight, which produced the XP and G200 indenters
- txt files from FischerScope
- zip-files which include all the txt files of the Micromaterials NanoXtreme
- HDF5 files produced by the supported converters/common format
- Tif images from Zeiss and FEI/ThermoFischer

Tutorials
=========

Indentation tutorials:

- :doc:`installation`
- :doc:`tutorialBasic`
- :doc:`tutorialAdvanced`
- :doc:`auto_examples/index`

Tif tutorials:

- :doc:`tutorialTif`

.. toctree::
   :maxdepth: 1
   :hidden:

   installation
   tutorialBasic
   tutorialAdvanced
   auto_examples/index
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
