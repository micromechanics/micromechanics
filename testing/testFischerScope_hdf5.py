#!/usr/bin/python3
import traceback
import unittest
import numpy as np
import matplotlib.pyplot as plt
from nanoindentation import Indentation

class TestStringMethods(unittest.TestCase):
	def test_main(self):
		try:
			### MAIN ###
			i = Indentation('examples/FischerScope/Nafion_15_100_5.hdf5')
			for testname in i:
				i.analyse()
			i.plot(show=3)
			self.assertTrue((   abs(np.sum(i.modulus)-0.4132913081938913)<1e-6 ),'Calculation of modulus changed')
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
