"""
Introduction
============
This is a tutorial for using nanoIndent.py while analysing nanoindentation data

.. note::
   The following units should be used: [mN], [µm], [GPa] because the area function is unit-dependent.

   Calculations are carried out by the Oliver-Pharr Method.

   Data in indentation experiment includes Method, Vendor, Indenter tip

   - Method: ISO, CSM

   - Vendor: Agilent, Hysitron, FischerScope

   - Indenter Tip: shape of indenter tip and stiffness of gantry

How it works:

1. Obtain loading and unloading data through nanoindentation, measuring force (p) and depth (h)
2. Calculate:

    - S [mN/µm]: Slope of unloading part (stiffness)
    - hc [µm]: Contact depth
    - Ac [µm2]: Contact area
    - H [GPa]: Hardness
    - Er [GPa]: reduced Young’s modulus
    - E [GPa]: Young’s modulus
3. Plot

Installation
============
1. Requirements: numpy, matplotlib, scipy ... ::

    pip3 install -r requirements.txt
2. Download "nanoIndent.py" from the sorce_code folder and use as described in the tutorial or clone this github repository::

    git clone git@github.com:micromechanics/main.git

Initialization
==============
Import necessary libraries::

    import matplotlib.pyplot as plt
    import numpy as np
    from nanoIndent import Indentation, Tip

Introduce tip::

    ourTip = Tip()  #µm/mN

Initialization: Files containing the experimental data are in hdf5, txt or xls format::

    fileName = 'FileName.hdf5'

Introduce class Indentation, where nuMat is material’s Poisson’s ratio::

    i = Indentation(fileName, nuMat=0.3, tip=ourTip)

Run through all indentations (Test 1, Test 2, etc) in the file with ``while True`` cycle::

    while True:
        <body>
        if len(i.testList)==0:
            break
        i.nextTest()

In the ``<body>`` one can analyse the data and create the plots to be viewed like following:

Calculate all the relevent data from the indent: stiffness S [mN/µm], maximum depth hMax [µm], maximum force pMax [mN], reduced Young’s modulus redE [GPa],
contact area A [µm2], contact depth hc [µm], Young’s modulus E [GPa], hardness H [GPa]::

    i.analyse()

Plotting:

- ``i.plot`` would plot each test(indent) independantly with the analysis data: slope, hc, power law etc
- ``plt.plot(i.h, i.p)`` would plot all tests(indents) together. Useful to spot outliers::

    i.plot()
    plt.plot(i.h, i.p)

Save all values to a dictionary. This can be appended to a user defined dataframe and further information can be added to it accordingly. E.g. the file name in this case::

    meta = i.metaUser
    meta["file name"]=fileName
    df = df.append(meta, ignore_index=True)

Show plots::

    plt.show()

Example:
========
This is an example code analysing the hdf5 files from FischerScope nanoindenter::

    import matplotlib.pyplot as plt
    import pandas as pd
    from nanoIndent import Indentation, Tip

    fileName = "N1_1.hdf5"
    ourTip = Tip()  #um/mN
    i = Indentation(fileName, nuMat=0.5, tip=ourTip)
    df = pd.DataFrame()

    while True:
        i.analyse()
        #i.plot()
        plt.plot(i.h, i.p)
        meta = i.metaUser
        df = df.append(meta, ignore_index=True)
        if len(i.testList)==0:
            break
        i.nextTest()

    print(df)
    plt.show()
"""
