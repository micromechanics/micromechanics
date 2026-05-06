#!/usr/bin/python3
import traceback
import unittest
from micromechanics.indentation import Indentation

testFiles = [
	'examples/Agilent/CSM_short.xls',
	'examples/Agilent/FQ.xls',
	'examples/Agilent/ISO_short.xls',
	'examples/Hysitron/RobinSteel0000LC.txt',
]

class TestMethods(unittest.TestCase):
	def test_all_filesn(self):
		try:
			print('**Purpose**\nCheck if all example files can be loaded and analysed.')
			### MAIN ###
			for fullPath in testFiles:
				print('\nStart with file:',fullPath)
				i = Indentation(fullPath)
				for _ in range(2):
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
