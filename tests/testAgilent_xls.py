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
			i = Indentation('examples/Agilent/FS_Calibration.xls', nuMat = 0.18)
			i.calibration()
			prerecorded = np.array([25.99088100777346, 305.6978416681741, 2050.70109154738])
			self.assertTrue(np.max(np.abs(np.array(i.tip.prefactors[:-1])-prerecorded))<0.1,
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
			i = Indentation('examples/Agilent/NiAl_250nm_TUIL_max_depth_1000nm_GM3_SM_previousGM1.xls')
			for testname in i:
				i.analyse()
			i.plot(show=3)
			self.assertTrue((abs(np.sum(i.modulus)-136478.52405870787)<0.1),'Calculation of modulus changed to '+str(np.sum(i.modulus)))
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
