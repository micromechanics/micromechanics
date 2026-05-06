import traceback
import unittest
from micromechanics.indentation import Indentation, Tip

class TestStringMethods(unittest.TestCase):
	def test_verify1(self):
		try:
			# MAIN
			print('**PURPOSE**\nRun the built-in single-data verification routine. Its purpose '
				  'is to catch changes in the reference Oliver-Pharr calculation, tip-area '
				  'handling, or scalar verification workflow.')
			i = Indentation('')
			i.verifyOneData()
			# END OF MAIN
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return


	def test_verify2(self):
		try:
			# MAIN
			print('**PURPOSE**\nRun the alternate built-in single-data verification routine. '
				  'Its purpose is to catch changes in the second reference verification path '
				  'for Oliver-Pharr calculation and tip-area handling.')
			i = Indentation('')
			i.verifyOneData1()
			# END OF MAIN
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return


	def test_verify3(self):
		try:
			# MAIN
			print('**PURPOSE**\nLoad a real Agilent XLS file with a reference ISO tip, iterates '
				  'through the first two tests/sheets and verifies read values against recalculated values. '
				  'Its purpose is to catch changes in Agilent XLS parsing, tip-area handling, '
				  'and Oliver-Pharr verification behavior.')
			tip = Tip(shape = [2.4695e+001,3.9577e+002,-1.6132e+001,1.3341e+002,1.0646e+002,'iso'])
			print("**INFO: Tip-area prefactors have accuracy of 1e-4; hence area accuracy on that order")
			i = Indentation('examples/Agilent/FS_XP.xls', nuMat=0.18, tip=tip, model={'cropSlopeToLoading': False})
			for _ in range(2):
				print('Sheet name:', i.testName)
				i.verifyReadCalc(plot=True)
				if len(i.testList)==0:
					break
				i.nextTest()
			# END OF MAIN
			print('\n*** DONE WITH VERIFY ***')
		except:
			print('ERROR OCCURRED IN VERIFY TESTING\n'+ traceback.format_exc() )
			self.assertTrue(False,'Exception occurred')
		return


	def tearDown(self):
		return

if __name__ == '__main__':
	unittest.main()
