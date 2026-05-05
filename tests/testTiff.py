#!/usr/bin/python3
import traceback
import unittest
from micromechanics.tif import Tif

class TestStringMethods(unittest.TestCase):
	def test_zeiss(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nLoad a real Zeiss TIF file, enhances the image and adds a '
				  'scale bar. Its purpose is to catch changes in Zeiss TIF parsing, image '
				  'enhancement, bundled font handling, or scale-bar rendering behavior. ')
			i = Tif('examples/Zeiss/Zeiss.tif')
			i.enhance()
			i.addScaleBar()
			i.plot(showDuration=3)
			### END OF MAIN ###
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return

	def test_fei(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nLoad a real FEI TIF file, enhances the image and adds a '
				  'scale bar. Its purpose is to catch changes in TIF parsing, image '
				  'enhancement, bundled font handling, or scale-bar rendering behavior. ')
			i = Tif('examples/FEI/KBZ_REM_01.tif')
			i.enhance()
			i.addScaleBar()
			i.plot(showDuration=3)
			### END OF MAIN ###
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return


	def test_npve(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nLoad a real NPVE TIF file, enhances the image and adds a '
				  'scale bar. Its purpose is to catch changes in TIF parsing, image '
				  'enhancement, bundled font handling, or scale-bar rendering behavior. ')
			i = Tif('examples/NPVE/Pearlite.tif')
			i.enhance()
			i.addScaleBar()
			i.plot(showDuration=3)
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
