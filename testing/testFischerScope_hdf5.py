#!/usr/bin/python3
import traceback
import unittest
import numpy as np
from nanoIndent import Indentation

class TestStringMethods(unittest.TestCase):
	def test_main(self):
		try:
			### MAIN ###
			i = Indentation('examples/FischerScope/Nafion_15_100_5.hdf5')
			i.analyse()
			print(np.sum(i.modulus))
			self.assertTrue((np.sum(i.modulus)==0.45085650501100577)<1e-12,'Calculation of modulus changed')
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
