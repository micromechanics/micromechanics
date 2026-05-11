#!/usr/bin/python3
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.interpolate import interp1d

from micromechanics.indentation import Indentation, Tip
from micromechanics.indentation.definitions import Method, Vendor
from micromechanics.tif import Tif


class TestCoverageBranchTargets(unittest.TestCase):
  def tearDown(self):
    plt.close("all")

  def make_gray_image(self, size=(40, 30)):
    y, x = np.mgrid[0:size[1], 0:size[0]]
    return Image.fromarray(np.clip(40 + 3*x + 5*y, 0, 255).astype(np.uint8))

  def make_image_file(self, tmp, name="image.tif", size=(40, 30)):
    file_name = Path(tmp) / name
    self.make_gray_image(size).save(file_name)
    return file_name

  def test_tif_detection_show_save_and_plot_branches(self):
    with tempfile.TemporaryDirectory() as tmp:
      image_file = self.make_image_file(tmp)
      image = Tif(str(image_file), fileType="Conventional", pixelSize=0.05)

      with patch.object(image.image, "show") as show:
        image.show()
        self.assertTrue(show.called)

      wide_file = self.make_image_file(tmp, "wide.tif", size=(1100, 20))
      wide = Tif(str(wide_file), fileType="Conventional", pixelSize=0.01)
      with patch.object(Image.Image, "show") as show:
        wide.show()
        self.assertTrue(show.called)

      image.plot(showDuration=-1)
      image.hist(show=True)
      image.save(fileType="png")
      image.save(fileType="jpg")
      image.save(fileType="eps")

      data = np.full((20, 30), 120, dtype=np.uint8)
      data[-2:, :] = 255
      white_bar = Path(tmp) / "white_bar.tif"
      Image.fromarray(data).save(white_bar)
      cropped = Tif(str(white_bar), fileType="Conventional", pixelSize=0.01)
      cropped.autoCrop("w")
      self.assertLess(cropped.image.size[1], 20)

      text_file = Path(tmp) / "imagej.txt"
      text_file.write_text("ImageJ=1.54\n", encoding="iso-8859-1")
      with patch.object(Tif, "initConventional", lambda self, pixelSize: None):
        detected = Tif(str(text_file))
      self.assertEqual(detected.producer, "ImageJ")

      tem_file = Path(tmp) / "tem.bin"
      tem_file.write_bytes(bytes.fromhex("49492a0010c000005448554d42313238"))
      with patch.object(Tif, "initConventional", lambda self, pixelSize: None):
        detected = Tif(str(tem_file))
      self.assertEqual(detected.producer, "TEM")

  def test_tif_processing_plot_branches(self):
    with tempfile.TemporaryDirectory() as tmp:
      image_file = self.make_image_file(tmp, size=(50, 35))
      image = Tif(str(image_file), fileType="Conventional", pixelSize=0.02)
      with redirect_stdout(StringIO()):
        image.gaussLevel(level=2, plot=True, save=False)
      image.contrast(magnitude=1.2, offset=0.45, save=False, plot=True, points=11)
      image.removeGrayGradient(save=False, plot=True)

  def test_tip_interpolation_repr_plot_and_warnings(self):
    x = np.linspace(0.02, 0.5, 8)
    interp = interp1d(x, 25*x*x, fill_value="extrapolate")
    tip = Tip(interpFunction=interp)
    self.assertIn("interpolation function", repr(tip))
    np.testing.assert_allclose(tip.areaFunction(np.array([0.1])), interp([0.1]))

    new_interp = interp1d(x, 30*x*x, fill_value="extrapolate")
    tip.setInterpolationFunction(new_interp)
    np.testing.assert_allclose(tip.areaFunction(np.array([0.1])), new_interp([0.1]))

    with tempfile.NamedTemporaryFile(suffix=".png") as handle:
      tip.plotIndenterShape(show=True, fileName=handle.name)

    with redirect_stdout(StringIO()) as out:
      Tip("perfect", compliance=0, verbose=2)
      Tip("perfect", compliance=0.1, verbose=2)
      Tip("perfect", plot=True)
    self.assertIn("stiffness outside domain", out.getvalue())

  def make_surface_indentation(self, surface):
    indentation = Indentation("")
    indentation.method = Method.CSM
    indentation.testName = "test"
    indentation.surface = surface
    indentation.h = np.linspace(-0.03, 0.12, 8)
    indentation.p = np.linspace(0.0, 0.7, 8)
    indentation.t = np.linspace(0.0, 7.0, 8)
    indentation.valid = np.ones(8, dtype=bool)
    indentation.slope = np.linspace(0.01, 0.8, 8)
    indentation.phase = np.linspace(0.8, 0.01, 8)
    indentation.model["cropSlopeToLoading"] = False
    def identify():
      indentation.iLHU = [[0, 2, 5, 6]]
      indentation.iDrift = [6, 7]
      return True
    indentation.identifyLoadHoldUnload = identify
    return indentation

  def test_surface_criteria_filters_and_plot_branches(self):
    cases = [
      {"stiffness": 0.2},
      {"phase angle": 0.3},
      {"abs(dp/dh)": 1.0},
      {"dp/dt": 0.01},
      {"stiffness": 0.2, "median filter": 3},
      {"stiffness": 0.2, "gauss filter": 1},
      {"stiffness": 0.2, "butterfilter": (1, 0.2)},
      {"stiffness": 0.2, "tare load": True},
    ]
    for surface in cases:
      with self.subTest(surface=surface):
        indentation = self.make_surface_indentation(surface)
        original_h = indentation.h.copy()
        with redirect_stdout(StringIO()) as out:
          self.assertTrue(indentation.nextTest(newTest=False, plotSurface=True))
        np.testing.assert_allclose(indentation.h, original_h)
        self.assertEqual(indentation.iLHU, [])
        self.assertIn("Run analyse() to show the full data.", out.getvalue())
        indentation.analyse()

    indexed = self.make_surface_indentation({"test": {"surfaceIdx": 2}})
    self.assertTrue(indexed.nextTest(newTest=False))
    self.assertNotAlmostEqual(indexed.h[2], 0.0)
    indexed.analyse()
    self.assertAlmostEqual(indexed.h[2], 0.0)

    no_criterion = self.make_surface_indentation({})
    with redirect_stdout(StringIO()) as out:
      self.assertTrue(no_criterion.nextTest(newTest=False, plotSurface=True))
    self.assertIn("Run analyse() to show the full data.", out.getvalue())

  def test_calibration_control_flow_variants(self):
    indentation = Indentation("")
    indentation.allTestList = ["test"]
    indentation.testList = []
    indentation.output["progressBar"] = lambda value, location: None
    indentation.restartFile = lambda: None
    indentation.nextTest = lambda *args, **kwargs: False
    indentation.calibrateStiffness = lambda **kwargs: 0.002
    h = np.linspace(0.2, 1.2, 101)
    p = np.linspace(1.0, 8.0, 101)
    slope = np.linspace(6.0, 16.0, 101)

    def analyse():
      indentation.metaUser = {"S_mN/um": slope, "hMax_um": h, "pMax_mN": p}
    indentation.analyse = analyse

    self.assertTrue(indentation.calibration(frameCompliance=0.001,
                                            numPolynomial=2,
                                            constantTerm=True))
    self.assertEqual(indentation.tip.prefactors[-1], "isoPlusConstant")

    hc, area = indentation.calibration(frameCompliance=0.001,
                                       numPolynomial=None,
                                       returnArea=True)
    self.assertEqual(len(hc), len(area))
    self.assertIsNone(indentation.tip.prefactors)

    csm = Indentation("")
    csm.method = Method.CSM
    csm.allTestList = ["test"]
    csm.testList = []
    csm.output["progressBar"] = lambda value, location: None
    csm.restartFile = lambda: None
    csm.nextTest = lambda *args, **kwargs: True
    csm.calibrateStiffness = lambda **kwargs: 0.001
    csm.h, csm.p, csm.slope = h, p, slope
    csm.valid = np.ones_like(h, dtype=bool)
    csm.analyse = lambda: None
    self.assertTrue(csm.calibration(numPolynomial=2))

  def test_plot_save_show_variants(self):
    indentation = Indentation("")
    indentation.fileName = "synthetic.xls"
    indentation.t = np.linspace(0, 4, 5)
    indentation.h = np.linspace(0, 0.4, 5)
    indentation.p = np.linspace(0, 2, 5)
    indentation.valid = np.array([False, True, True, True, False])
    indentation.slope = np.array([4.0, 5.0, 6.0])
    indentation.phase = np.array([0.1, 0.2, 0.3])
    indentation.iLHU = [[0, 1, 3, 4]]
    indentation.iDrift = [3, 4]
    indentation.hc = np.array([0.1])
    indentation.Ac = np.array([0.2])
    indentation.modulus = np.array([70.0])
    indentation.modulusRed = np.array([75.0])
    indentation.hardness = np.array([6.0])
    indentation.output["verbose"] = 2
    indentation.stiffnessFromUnloading = lambda _p, _h: (None, None, None, None, None)

    indentation.plotTestingMethod(saveFig=False, show=True, double=False)
    with tempfile.NamedTemporaryFile(suffix=".png") as handle:
      indentation.plot(saveFig=handle.name, show=False, plotAllItems=False)
    with tempfile.TemporaryDirectory() as tmp:
      indentation.fileName = str(Path(tmp) / "synthetic.xls")
      indentation.plot(saveFig=True, show=False, plotAllItems=False)

    indentation.restartFile = lambda: None
    calls = {"count": 0}
    def next_iter():
      if calls["count"]:
        raise StopIteration
      calls["count"] += 1
      return "synthetic"
    indentation.__iter__ = lambda: indentation
    indentation.__next__ = next_iter
    with tempfile.TemporaryDirectory() as tmp:
      indentation.fileName = str(Path(tmp) / "all.xls")
      indentation.plotAll(saveFig=True, show=1)

  def create_kla_hdf5(self, file_name, include_depth=True):
    with h5py.File(file_name, "w") as h5:
      h5.attrs["version"] = "2.0"
      h5.attrs["uri"] = "https://example.org/nmd2hdf.py"
      instrument = h5.create_group("instrument")
      instrument.attrs["json"] = json.dumps({"SAMPLE": {"@TEMPLATENAME": "Dynamic Test"}})
      data = h5.create_group("test_1").create_group("data")
      values = np.linspace(1.0, 2.0, 70)
      if include_depth:
        data.create_dataset("depth", data=values*1e-6)
      data.create_dataset("load", data=values*1e-3)
      data.create_dataset("time", data=np.linspace(0.0, 1.0, 70))
      data.create_dataset("show_stiffness", data=values*1e3)
      data.create_dataset("dynamic_phase", data=np.linspace(0.0, 1.0, 70))

  def test_hdf5_metadata_and_missing_data_paths(self):
    with tempfile.TemporaryDirectory() as tmp:
      good = Path(tmp) / "kla.hdf5"
      self.create_kla_hdf5(good)
      indentation = Indentation(str(good), output={"verbose": 0})
      self.assertEqual(indentation.vendor, Vendor.KLAHDF5)
      self.assertEqual(indentation.method, Method.CSM)

      missing = Path(tmp) / "missing.hdf5"
      self.create_kla_hdf5(missing, include_depth=False)
      bad = Indentation("")
      bad.vendor = Vendor.Hdf5
      bad.fileType = 2
      bad.output["verbose"] = 0
      with redirect_stdout(StringIO()) as out:
        self.assertTrue(bad.loadHDF5(str(missing)))
      self.assertIn("Missing information", out.getvalue())


if __name__ == "__main__":
  unittest.main()
