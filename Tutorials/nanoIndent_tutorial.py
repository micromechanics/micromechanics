"""
Introduction
============
This is a tutorial for using nanoIndent.py while analysing nanoindentation data

.. note::
   The following units should be used: [mN], [µm], [GPa] because the area function is unit-dependent. Calculations are carried out by the Oliver-Pharr Method.

How it works:

1. Measure maximum force (Pmax) and depth (hmax), get loading and unloading data through nanoindentation
2. Calculate:

    - S [mN/µm]: Slope of unloading part (stiffness)
    - hc [µm]: Contact depth
    - Ac [µm2]: Contact area
    - H [GPa]: Hardness
    - Er [GPa]: reduced Young’s modulus
    - E [GPa]: Young’s modulus
3. Plot

Example code:
=============

This is an example code analysing the data from a Fischer nanoindenter::

    df = pd.DataFrame()
    ourTip = Tip()  #um/mN
    for fileName in os.listdir('.'):
        if fileName.endswith('100mN_10s.hdf5'):
            i = Indentation(fileName, nuMat=0.3, tip=ourTip)
            while True:
                #print("Test list",i.testList)
                i.analyse()
                #i.plot()
                plt.plot(i.h, i.p)
                meta = i.metaUser
                meta["test name"]=i.testName
                meta["file name"]=fileName
                df = df.append(meta, ignore_index=True)
                if len(i.testList)==0:
                    break
                i.nextTest()
    print(df)
    plt.show()

Explanation of the code
=======================
Import necessary libraries::
    
    import matplotlib.pyplot as plt
    import os
    import numpy as np
    import pandas as pd
    from nanoIndent import Indentation, Tip

Create an empty dataframe before the cycle to store all analyzed data::

    df = pd.DataFrame()

Introduce tip::

    ourTip = Tip()  #µm/mN

Initialization: Start cycle to open and read through all hdf files.
One can navigate through the hdf files using ``startswith("...")`` and ``endswith("...")`` like in the example::

    for fileName in os.listdir('.'):
        if fileName.endswith('100mN_10s.hdf5'):
            i = Indentation(fileName, nuMat=0.3, tip=ourTip)

Run through all indentations (Test 1, Test 2, etc) in the hdf file with ``while True`` cycle to make sure the code will run through all of them::

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
- ``plt.plot(i.h, i.p)`` would plot all tests(indents) together. Useful to spot outliers like indentations on dirt or dust particles::


    i.plot()
    plt.plot(i.h, i.p)

Save all values and add any additional information that might be of use to a dictionary to append to the dataframe storing all analized data accordingly::

    meta = i.metaUser
    meta["test name"]=i.testName
    meta["file name"]=fileName
    df = df.append(meta, ignore_index=True)

Show the plots, print the dataframe if needed::

    print(df)
    plt.show()

Doctest
=======

.. doctest::

   >>> from nanoIndent import Indentation, Tip
   >>> import os
   >>> import matplotlib.pyplot as plt
   >>> import pandas as pd
   >>> import numpy as np
   >>> from nanoIndent import Indentation, Tip
   >>> ourTip = Tip()  #um/mN
   >>> df = pd.DataFrame()
   >>> fileName = "polymer_100mN_10s.hdf5"
   >>> i = Indentation(fileName, nuMat=0.3, tip=ourTip)
   Open hdf5-file: polymer_100mN_10s.hdf5
   Number Unloading segments 1
   >>> while True:
   ...   #print("Test list",i.testList)
   ...   i.analyse()
   ...   #i.plot()
   ...   #plt.plot(i.h, i.p)
   ...   meta = i.metaUser
   ...   meta["test name"]=i.testName
   ...   meta["file name"]=fileName
   ...   df = df.append(meta, ignore_index=True)
   ...   if len(i.testList)==0:
   ...     break
   ...   _ = i.nextTest()
   ...
    Number of unloading segments:1  Method:Method.ISO
    Number Unloading segments 1
    Number of unloading segments:1  Method:Method.ISO
    Number Unloading segments 1
    Number of unloading segments:1  Method:Method.ISO
    Number Unloading segments 1
    Number of unloading segments:1  Method:Method.ISO
   >>> print(df.shape)
   (4, 13)
   >>> #plt.show()
     

   

"""