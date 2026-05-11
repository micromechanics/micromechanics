#!/usr/bin/python3
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from micromechanics.indentation import Indentation


def synthetic_indentation():
  indentation = Indentation("")
  indentation.fileName = "synthetic.xls"
  indentation.t = np.linspace(0, 6, 7)
  indentation.h = np.array([0.00, 0.04, 0.12, 0.22, 0.35, 0.50, 0.65])
  indentation.p = np.array([0.00, 0.20, 0.75, 1.60, 2.20, 1.10, 0.10])
  indentation.valid = np.array([False, False, True, True, True, False, False])
  indentation.slope = np.array([8.0, 9.0, 10.0])
  indentation.phase = np.array([0.05, 0.06, 0.07])
  indentation.modulus = np.array([68.0, 70.0, 72.0])
  indentation.modulusRed = np.array([72.0, 74.0, 76.0])
  indentation.hardness = np.array([6.0, 6.5, 7.0])
  indentation.hc = np.array([0.08, 0.16, 0.28])
  indentation.Ac = np.array([0.03, 0.08, 0.16])
  indentation.iLHU = [[1, 2, 4, 6]]
  indentation.output["verbose"] = 2
  return indentation


class TestPlotBranches(unittest.TestCase):
  def tearDown(self):
    plt.close("all")

  def test_plot_as_depth_entities_and_limits(self):
    indentation = synthetic_indentation()
    for entity in ["E", "modulusRed", "H", "K", "hc", "Ac"]:
      indentation.plotAsDepth(entity, hvline=1.0, vmin=0.0, vmax=100.0, show=False)

  def test_plot_as_depth_computes_k2p_when_absent(self):
    indentation = synthetic_indentation()
    delattr(indentation, "k2p")
    indentation.plotAsDepth("K2P", show=False)
    self.assertTrue(np.all(np.isfinite(indentation.k2p)))

  def test_plot_testing_method_double_and_save(self):
    indentation = synthetic_indentation()
    with tempfile.TemporaryDirectory() as tmp:
      indentation.fileName = tmp + "/method.xls"
      ax = indentation.plotTestingMethod(saveFig=True, show=False, double=True)
    self.assertEqual(ax.get_xlabel(), r"time [$\mathrm{s}$]")

  def test_plot_accepts_integer_show_and_string_save_path(self):
    indentation = synthetic_indentation()
    indentation.stiffnessFromUnloading = lambda _p, _h: (None, None, None, None, None)
    with tempfile.NamedTemporaryFile(suffix=".png") as handle:
      with redirect_stdout(StringIO()):
        indentation.plot(saveFig=handle.name, show=1, plotAllItems=True)


if __name__ == "__main__":
  unittest.main()
