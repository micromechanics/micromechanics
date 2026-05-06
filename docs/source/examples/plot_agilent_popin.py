"""
Agilent Pop-In Detection
========================

This example loads an Agilent XLS file, detects pop-in events in each test,
and plots the indentation curve with the strongest detected depth jump.
"""

from pathlib import Path
import warnings

import matplotlib
import pandas as pd

matplotlib.use("Agg")
warnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive")

import micromechanics
from micromechanics.indentation import Indentation

repository_root = Path(micromechanics.__file__).resolve().parents[1]
file_name = repository_root / "examples" / "Agilent" / "Popin.xls"

###############################################################################
# Load the multi-test Agilent workbook. Iterating over an ``Indentation`` object
# advances through the individual tests/sheets in the file.

indentation = Indentation(str(file_name), output={"verbose": 0})
rows = []

###############################################################################
# ``popIn`` searches for a sudden depth jump in the loading curve. Besides the
# force at the jump, it returns diagnostic values that help rank how clear the
# event is in each test.

for testname in indentation:
  popin_force, certainty = indentation.popIn(plot=False)
  rows.append({
    "test": testname,
    "popin_force_mN": popin_force,
    "delta_depth_um": certainty["deltaH"],
    "delta_slope": certainty["deltaSlope"],
    "second_rate": certainty["secondRate"],
  })

df = pd.DataFrame(rows)
print(df)

###############################################################################
# Plot the test with the largest detected depth jump. Reopening the file resets
# the iterator, making it easy to revisit one selected test and request the
# diagnostic plot only for that curve.

best_test = df.sort_values("delta_depth_um", ascending=False).iloc[0]["test"]

indentation = Indentation(str(file_name), output={"verbose": 0})
for testname in indentation:
  if testname == best_test:
    indentation.popIn(plot=True)
    break
