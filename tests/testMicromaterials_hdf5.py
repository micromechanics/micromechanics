#!/usr/bin/python3
import traceback
import unittest
import numpy as np
import matplotlib.pyplot as plt
from micromechanics.indentation import Indentation

class TestStringMethods(unittest.TestCase):
	def test_main(self):

		#TODO_P1 repair micromaterials and include test
		# try:
		# 	### MAIN ###
		# 	i = Indentation('examples/Micromaterials/Sample1_Vac_RT.hdf5')
		# 	for testname in i:
		# 		i.analyse()
		# 	i.plot(show=3)
		# 	print(i.modulus)
		# 	self.assertTrue((abs(np.sum(i.modulus)-150.7015476364166)<0.1),'Modulus changed to '+str(np.sum(i.modulus)))
		# 	### END OF MAIN ###
		# 	print('\n*** DONE WITH VERIFY ***')

		# except:
		# 	print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
		# 	self.assertTrue(False,'Exception occurred')

		return

	def tearDown(self):
		return

if __name__ == '__main__':
	unittest.main()
