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
			print('**PURPOSE**\nLoad a real Micromaterials HDF5 file, iterates through all '
		 		  'tests and checks that the total calculated Youngs modulus sum is unchanged. '
				  'Its purpose is a smoke/regression test for Micromaterials HDF5 parsing plus '
				  'the analysis pipeline: valid-point handling, stiffness correction, '
				  'Oliver-Pharr modulus calculation.')
			i = Indentation('examples/Micromaterials/FS_cal.hdf5')
			for testname in i:
				i.analyse()
			i.plot(show=3)
			print('  Moduli', i.modulus)
			self.assertTrue((abs(np.sum(i.modulus)-1330.378741254122)<0.1),'Modulus changed to '+str(np.sum(i.modulus)))
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
