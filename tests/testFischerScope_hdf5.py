#!/usr/bin/python3
import traceback
import unittest
import numpy as np
import matplotlib.pyplot as plt
from micromechanics.indentation import Indentation

class TestStringMethods(unittest.TestCase):
	def test_main(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nLoad a real FischerScope HDF5 file, iterates through all '
		 		  'tests and checks that the total calculated Youngs modulus sum is unchanged. '
				  'Its purpose is a smoke/regression test for FischerScope HDF5 parsing plus '
				  'the analysis pipeline: valid-point handling, stiffness correction, '
				  'Oliver-Pharr modulus calculation.')
			i = Indentation('examples/FischerScope/N1_1.hdf5')
			for testname in i:
				i.analyse()
			i.plot(show=3)
			self.assertTrue((   abs(np.sum(i.modulus)-0.6685824443995321)<0.01 ),'Modulus changed to '+str(np.sum(i.modulus)))
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
