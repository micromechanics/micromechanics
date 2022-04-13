#!/usr/bin/python3
import traceback
import unittest
import numpy as np
import matplotlib.pyplot as plt
from nanoindentation import Indentation

class TestStringMethods(unittest.TestCase):
	def test_calibration(self):
		try:
			### MAIN ###
			i = Indentation('examples/Agilent/FS_Calibration.xls', nuMat = 0.18)
			i.calibration()
			self.assertTrue(i.tip.prefactors==[25.99088100777346, 305.6978416681741, 2050.70109154738, 'iso'],'Tip prefactors changed')
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
			self.assertTrue(np.sum(i.modulus)==136478.52405870787,'Calculation of modulus changed')
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
