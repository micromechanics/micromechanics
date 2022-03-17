#!/usr/bin/python3
import traceback
import unittest
import numpy as np
from nanoIndent import Indentation


class TestStringMethods(unittest.TestCase):
	def test_main(self):
		try:
			### MAIN ###
			i = Indentation('examples/Micromaterials/Sample1_Vac_200C.hdf5')
			i.analyse()
			self.assertTrue((np.sum(i.modulus)==7.074141923076374e-05),'Calculation of modulus changed')
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
