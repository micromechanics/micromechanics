"""
Indentation Surface Detection
=============================

This example loads a FischerScope HDF5 file with surface detection enabled.
"""

from pathlib import Path

import micromechanics
from micromechanics.indentation import Indentation

repository_root = Path(micromechanics.__file__).resolve().parents[1]
file_name = repository_root / "examples/FischerScope/N1_1.hdf5"

###############################################################################
# Inspect the raw file: it does not start at 0 / 0
indentation = Indentation(str(file_name), nuMat=0.45)
indentation.plot()

###############################################################################
# Use surface correction using a load threshold; the depth is now at 0. But the force not
# - one can use different values as critical axis and filtering to smooth signals
indentation = Indentation(str(file_name), nuMat=0.45, surface={"load": 0.1})
indentation.plot()

###############################################################################
# Use surface correction using a load threshold and tare the force. Both are now at 0 / 0
indentation = Indentation(str(file_name), nuMat=0.45, surface={"load": 0.1, "tare load": True})
indentation.plot()
