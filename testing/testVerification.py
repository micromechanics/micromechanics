import traceback
import unittest
from nanoindentation import Indentation

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
			i = Indentation('examples/Agilent/FS_Calibration.xls', nuMat=0.18)
			if hasattr(self, 'hc') and hasattr(self, 'Ac') and hasattr(self, 'modulusRed') and \
				 hasattr(self, 'modulus') and hasattr(self, 'hardness'):
				i.verifyReadCalc()
			else:
				print("\n\n** ERROR file has not enough data for verification! **\n\n")
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
