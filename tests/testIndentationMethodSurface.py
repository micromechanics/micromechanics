#!/usr/bin/python3
# Verify:
# 1. Methods imported from separate modules are actually attached to Indentation
#     - e.g. parser methods, analysis methods, plotting, calibration, verification helpers.
#     - It checks both Indentation.method_name and indentation.method_name.
# 2. Representative vendor files still load and analyze
#     - Agilent .xls
#     - Hysitron .hld
#     - Micromaterials .zip
#     - FischerScope .txt
#     - Converted FischerScope .hdf5
# 3. Iteration and plotting still work on a multi-test HDF5 file.
# It is a smoke/integration test that catches accidental breakage in the package’s dynamic class composition and vendor loading paths.
import inspect
import unittest

import numpy as np

from micromechanics.indentation import Indentation
from micromechanics.indentation.definitions import FileType, Vendor


ATTACHED_METHODS = [
  'loadAgilent', 'nextAgilentTest', 'loadHysitron', 'loadMicromaterials',
  'nextMicromaterialsTest', 'loadFischerScope', 'nextFischerScopeTest',
  'loadHDF5', 'nextHDF5Test', 'restartFile', 'setRawData',
  'calcYoungsModulus', 'calcHardness', 'calcStiffness2Force', 'analyse',
  'identifyLoadHoldUnload', 'identifyLoadHoldUnloadCSM', 'nextTest',
  'saveToUserMeta',
  'YoungsModulus', 'ReducedModulus', 'OliverPharrMethod',
  'inverseOliverPharrMethod', 'stiffnessFromUnloading', 'unloadingPowerFunc',
  'popIn', 'hertzFit',
  'plotTestingMethod', 'plot', 'plotAsDepth', 'plotAll',
  'calibration', 'calibrateStiffness',
  'verifyOneData', 'verifyOneData1', 'verifyReadCalc'
]


class TestIndentationMethodSurface(unittest.TestCase):
  def test_imported_methods_are_available_on_class_and_instance(self):
    print('**PURPOSE**\nChecks that methods imported from separate modules are attached '
          'to both the Indentation class and instance. Its purpose is to catch changes '
          'in dynamic class composition, staticmethod binding, and basic theory helper '
          'availability.')
    indentation = Indentation('examples/Agilent/Popin.xls', output={'verbose': 0})

    for method_name in ATTACHED_METHODS:
      with self.subTest(method_name=method_name):
        self.assertTrue(callable(getattr(Indentation, method_name)), method_name)
        self.assertTrue(callable(getattr(indentation, method_name)), method_name)

    self.assertIsInstance(inspect.getattr_static(Indentation, 'unloadingPowerFunc'), staticmethod)
    np.testing.assert_allclose(indentation.unloadingPowerFunc(np.array([2.0]), 3.0, 1.0, 2.0), np.array([3.0]))
    self.assertGreater(indentation.YoungsModulus(100.0), 0.0)
    self.assertGreater(indentation.ReducedModulus(100.0), 0.0)

  def test_representative_vendor_files_load_and_analyse(self):
    print('**PURPOSE**\nLoad representative vendor files and checks that each file is '
          'recognized with the expected vendor and file type. Its purpose is a smoke/'
          'regression test for Agilent, Hysitron, Micromaterials, FischerScope, and '
          'converted FischerScope HDF5 loading plus the analysis pipeline.')
    cases = [
      ('examples/Agilent/Popin.xls', Vendor.Agilent, FileType.Multi),
      ('examples/Hysitron/Exp-50mN_0000.hld', Vendor.Hysitron, FileType.Single),
      ('examples/Micromaterials/multipleIndentations.zip', Vendor.Micromaterials, FileType.Multi),
      ('examples/FischerScope/FS1.txt', Vendor.FischerScope, FileType.Multi),
      ('examples/FischerScope/N1_1.hdf5', Vendor.FischerScopeHDF5, FileType.Multi),
    ]

    for file_name, vendor, file_type in cases:
      with self.subTest(file_name=file_name):
        indentation = Indentation(file_name, output={'verbose': 0})
        self.assertEqual(indentation.vendor, vendor)
        self.assertEqual(indentation.fileType, file_type)
        if file_type == FileType.Multi:
          self.assertTrue(indentation.testName)
        indentation.analyse()
        self.assertGreater(len(indentation.h), 0)
        self.assertGreater(len(indentation.p), 0)

  def test_iteration_and_plotting_use_bound_methods(self):
    print('**PURPOSE**\nLoad a multi-test FischerScope HDF5 file, iterates through all '
          'tests and checks that plotting still works through bound Indentation methods. '
          'Its purpose is to catch changes in HDF5 iteration, analysis dispatch, and '
          'plotting method binding.')
    indentation = Indentation('examples/FischerScope/N1_1.hdf5', output={'verbose': 0})
    test_names = []
    for test_name in indentation:
      test_names.append(test_name)
      indentation.analyse()

    self.assertGreater(len(test_names), 0)
    indentation.plot(show=3)


if __name__ == '__main__':
  unittest.main()
