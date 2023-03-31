#!/usr/bin/python3
import traceback
import unittest
from micromechanics.tif import Tif

class TestStringMethods(unittest.TestCase):
	def test_calibration(self):
		try:
			### MAIN ###
			i = Tif('examples/Zeiss/Zeiss.tif')
			i.enhance()
			i.addScaleBar()
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
