#!/usr/bin/python3
import traceback
import unittest
import numpy as np
import matplotlib.pyplot as plt
from micromechanics.indentation import Indentation

class TestStringMethods(unittest.TestCase):
	def test_calibration(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nChecks that the fitted tip area-function prefactors stay close'
		 		  ' to known reference values. Its purpose is to catch changes in Agilent XLS '
				  'loading, frame stiffness correction, calibration fitting, or area-function '
				  'behavior.')
			i = Indentation('examples/Agilent/FS_Calibration.xls', nuMat = 0.18, model={'cropSlopeToLoading': False})
			i.calibration()
			prerecorded = np.array([25.99088100777346, 305.6978416681741, 2050.70109154738])
			self.assertTrue(np.max(np.abs(np.array(i.tip.areaPrefactors)-prerecorded))<0.1,
								'Tip prefactors changed to '+str(i.tip.prefactors))
			### END OF MAIN ###
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return

	def test_other(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nLoad a real NiAl Agilent XLS file, iterates through all '
		 		  'tests/sheets and checks that the total calculated Youngs modulus sum '
				  'is unchanged. Its purpose is a broader smoke/regression test for multi-test'
				  'Agilent XLS parsing plus the analysis pipeline: valid-point handling, '
				  'stiffness correction,  Oliver-Pharr modulus calculation.')
			model = {'cropSlopeToLoading': False}
			i = Indentation('examples/Agilent/NiAl_250nm_TUIL_max_depth_1000nm_GM3_SM_previousGM1.xls', model=model)
			for testname in i:
				i.analyse()
			i.plot(show=3)
			self.assertTrue((abs(np.sum(i.modulus)-136478.52405870787)<0.1),'Calculation of modulus changed to '+str(np.sum(i.modulus)))
			i.identifyLoadHoldUnload(True)
			### END OF MAIN ###
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return

	def tearDown(self):
		return

if __name__ == '__main__':
	unittest.main()
