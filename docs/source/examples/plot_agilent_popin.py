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

indentation = Indentation(str(file_name), output={"verbose": 0})
rows = []

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
# Plot the test with the largest detected depth jump.
best_test = df.sort_values("delta_depth_um", ascending=False).iloc[0]["test"]

indentation = Indentation(str(file_name), output={"verbose": 0})
for testname in indentation:
  if testname == best_test:
    indentation.popIn(plot=True)
    break
