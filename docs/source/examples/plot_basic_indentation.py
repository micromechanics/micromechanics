"""
Basic Indentation Analysis
==========================

This example analyses a FischerScope HDF5 file and plots each indentation
curve.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import micromechanics
from micromechanics.indentation import Indentation, Tip

repository_root = Path(micromechanics.__file__).resolve().parents[1]
file_name = repository_root / "examples" / "FischerScope" / "N1_1.hdf5"

###############################################################################
# Define the tip and load the measurement file. The material Poisson ratio
# enters the conversion from reduced modulus to Young's modulus.

tip = Tip()
indentation = Indentation(str(file_name), nuMat=0.5, tip=tip)
rows = []

###############################################################################
# Each iteration selects the next indentation test. ``analyse`` performs the
# Oliver-Pharr evaluation and stores the resulting values in ``metaUser``.

for testname in indentation:
  indentation.analyse()
  plt.plot(indentation.h, indentation.p, label=testname)
  rows.append(indentation.metaUser.copy())

###############################################################################
# The force-depth plot gives a quick visual check for repeated measurements,
# while the dataframe collects the numerical metadata for inspection or export.

plt.xlabel("Depth / um")
plt.ylabel("Load / mN")
plt.legend()

df = pd.DataFrame(rows)
print(df)
