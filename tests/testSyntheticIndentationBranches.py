#!/usr/bin/python3
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from micromechanics.indentation import Indentation, Tip
from micromechanics.indentation.definitions import Method


class TestSyntheticIndentationBranches(unittest.TestCase):
  def tearDown(self):
    plt.close("all")

  def make_indentation(self):
    indentation = Indentation("")
    h = np.array([0.05, 0.15, 0.30, 0.45, 0.60])
    p = np.array([0.10, 0.40, 0.90, 1.30, 1.60])
    t = np.linspace(0, 4, 5)
    valid = np.array([True, True, True, True, True])
    slope = np.array([6.0, 8.0, 10.0, 12.0, 14.0])
    indentation.setRawData(h, p, t, valid, slope=slope)
    indentation.hRaw = indentation.h.copy()
    indentation.sRaw = indentation.slope.copy()
    indentation.modulus = np.linspace(60.0, 80.0, 5)
    indentation.hardness = np.linspace(4.0, 8.0, 5)
    return indentation

  def test_modulus_hardness_and_stiffness2force_plot_branches(self):
    indentation = self.make_indentation()
    modulus_average = indentation.calcYoungsModulus(minDepth=0.2, plot=True)
    indentation.calcHardness(minDepth=0.2, plot=True)
    prefactors = indentation.calcStiffness2Force(minDepth=0.01, plot=True)
    self.assertGreater(modulus_average, 0)
    self.assertEqual(len(prefactors), 2)
    self.assertEqual(len(indentation.hardness), 5)

  def test_analyse_returns_when_unloading_fit_fails(self):
    indentation = self.make_indentation()
    indentation.method = Method.ISO
    indentation.identifyLoadHoldUnload = lambda: True
    indentation.stiffnessFromUnloading = lambda _p, _h: (None, None, None, None, None)
    indentation.analyse()
    self.assertEqual(len(indentation.slope), 0)
    self.assertFalse(np.any(indentation.valid))

  def test_analyse_restarts_from_raw_data(self):
    indentation = self.make_indentation()
    indentation.method = Method.CSM
    indentation.tip.compliance = 0.01
    indentation.model["driftRate"] = 0.001
    indentation.analyse()
    h_once = indentation.h.copy()
    slope_once = indentation.slope.copy()

    indentation.analyse()
    np.testing.assert_allclose(indentation.h, h_once)
    np.testing.assert_allclose(indentation.slope, slope_once)

  def test_save_to_user_meta_csm_empty_slope(self):
    indentation = self.make_indentation()
    indentation.method = Method.CSM
    indentation.slope = np.array([])
    indentation.saveToUserMeta()
    self.assertEqual(indentation.metaUser["code"], "main.py")
    self.assertNotIn("S_mN/um", indentation.metaUser)

  def test_hertz_fit_and_failure_branch(self):
    indentation = Indentation("")
    indentation.h = np.linspace(0.0, 0.2, 80)
    true_h0 = 0.015
    shifted = np.maximum(indentation.h.copy()-true_h0, 0.0)
    indentation.p = 4.0/3.0*9000.0*np.sqrt(shifted**3)
    fit = indentation.hertzFit(forceRange=(0.02, 6.0), correctH=True, plot=True)
    self.assertEqual(len(fit), 2)
    self.assertAlmostEqual(fit[0], true_h0, places=3)

    sparse = Indentation("")
    sparse.h = np.array([0.0, 0.1, 0.2])
    sparse.p = np.array([0.0, 0.01, 10.0])
    with self.assertRaises(ValueError):
      sparse.hertzFit(forceRange=(0.02, 1.0), plot=False)

  def test_tip_area_models_and_repr_branches(self):
    depth = np.array([0.05, 0.2, 0.6])
    iso_plus_constant = Tip("perfect")
    iso_plus_constant.prefactors = [24.5, 100.0, 10.0, "isoPlusConstant"]
    sphere = Tip(shape=[3.0, 70.3, "sphere"])
    perfect = Tip("perfect")
    self.assertTrue(np.all(iso_plus_constant.areaFunction(depth.copy()) > 0))
    self.assertTrue(np.all(sphere.areaFunction(depth.copy()) > 0))
    inverse_area = perfect.areaFunctionInverse(np.array([1.0]))
    self.assertIsNotNone(inverse_area)
    self.assertGreater(inverse_area[0], 0)
    self.assertIn("prefactors", repr(perfect))


if __name__ == "__main__":
  unittest.main()
