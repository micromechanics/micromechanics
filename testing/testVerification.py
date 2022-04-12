import traceback
import unittest
from nanoindentation import Indentation, Tip

class TestStringMethods(unittest.TestCase):
	def test_verify1(self):
		try:
			# MAIN
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
			tip = Tip(shape = [2.4695e+001,3.9577e+002,-1.6132e+001,1.3341e+002,1.0646e+002,'iso'])
			print("**INFO: Tip-area prefactors have accuracy of 1e-4; hence area accuracy on that order")
			i = Indentation('examples/Agilent/FS_XP.xls', nuMat=0.18, tip=tip)
			while True:
				print('Sheet name:', i.testName)
				i.verifyReadCalc(plot=False)
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
