"""
Indentation Tip Calibration
===========================

This example calibrates a tip from Agilent calibration measurements and uses
the calibrated tip to initialize a measurement file.
"""

from pathlib import Path

import micromechanics
from micromechanics.indentation import Indentation

repository_root = Path(micromechanics.__file__).resolve().parents[1]
calibration_file = repository_root / "examples/Agilent/FS_Calibration.xls"
measurement_file = repository_root / "examples/Agilent/NiAl_250nm_TUIL_max_depth_1000nm_GM3_SM_previousGM1.xls"

###############################################################################
# Inspect the calibration measurements first. ``analyse`` evaluates the current
# test, and ``K2P`` plots stiffness squared over load, a common diagnostic for
# frame stiffness and tip-area calibration quality.

calibration = Indentation(str(calibration_file), nuMat=0.18)
calibration.analyse()
calibration.plotAsDepth("K2P")

###############################################################################
# Fit the frame stiffness and tip shape. ``plotStiffness`` shows the frame
# correction step; ``plotTip`` shows the calibrated tip shape against the
# reference geometry.

calibration.calibration(plotStiffness=True, plotTip=True)

###############################################################################
# Reuse the calibrated tip for a measurement file. Passing ``tip=calibration.tip``
# ensures the later analysis uses the area function found from the calibration
# workbook instead of the default ideal tip.

measurement = Indentation(str(measurement_file), tip=calibration.tip)
