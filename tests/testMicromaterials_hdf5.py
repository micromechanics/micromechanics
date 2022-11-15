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
			i = Indentation('examples/Micromaterials/Sample1_Vac_200C.hdf5')
			for testname in i:
				i.analyse()
			i.plot(show=3)
			self.assertTrue((abs(np.sum(i.modulus)-51.664364831662226)<0.1),'Calculation of modulus changed')
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
