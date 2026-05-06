#!/usr/bin/python3
import traceback, os
import unittest
import numpy as np
from micromechanics.indentation import Indentation

skipFiles = ['examples/Agilent/FS_XP_MethodInclCalibration.txt', 'examples/Agilent/ISO.txt',
			 'examples/Agilent/CSM.txt', 'examples/Zeiss/Zeiss.tif', 'examples/FEI/KBZ_REM_01.tif',
			 'examples/NPVE/Pearlite.tif']

class TestMethods(unittest.TestCase):
	def test_all_filesn(self):
		try:
			print('**Purpose**\nCheck if all example files can be loaded and analysed.')
			### MAIN ###
			for path, _, files in os.walk('examples'):
				if files == []:
					continue
				for fileName in files:
					fullPath = path+os.sep+fileName
					if fullPath in skipFiles:
						continue
					print('\nStart with file:',fullPath)
					i = Indentation(fullPath)
					while True:
						i.analyse()
						print('   Test succeeded', i.testName)
						if (not i.testList) or len(i.testList)==0:
							break
						i.nextTest()
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
