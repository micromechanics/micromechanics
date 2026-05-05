#!/usr/bin/python3
import traceback
import unittest

from micromechanics.tif import Tif


class TestZeissTransforms(unittest.TestCase):
	def test_non_gallery_image_transforms(self):
		try:
			### MAIN ###
			print('**PURPOSE**\nLoad a real Zeiss TIF file and exercise image transformation '
			      'helpers that are not covered by the executable documentation examples. '
			      'Its purpose is to catch changes in reset, scaling, topology correction, '
			      'rotation, flipping, and histogram generation behavior.')
			i = Tif('examples/Zeiss/Zeiss.tif')
			original_size = i.image.size
			original_width = i.width
			original_pixel_size = i.pixelSize

			i.scale(2)
			self.assertEqual(i.image.size[0], original_size[0] * 2)
			self.assertAlmostEqual(i.pixelSize, original_pixel_size / 2)

			i.topology(axis="H", start=0, end=5)
			i.rotateCCW()
			i.rotateCW()
			i.rotate180()
			i.flip()
			i.hist(show=False)

			i.reset()
			self.assertEqual(i.image.size, original_size)
			self.assertAlmostEqual(i.width, original_width)
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
