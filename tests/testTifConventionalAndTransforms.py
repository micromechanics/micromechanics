#!/usr/bin/python3
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

import matplotlib
matplotlib.use("Agg")
import numpy as np
from PIL import Image

from micromechanics.tif import Tif


class TestTifConventionalAndTransforms(unittest.TestCase):
  def make_image(self, mode="L", size=(32, 24)):
    y, x = np.mgrid[0:size[1], 0:size[0]]
    data = np.clip(30 + 4*x + 3*y, 0, 255).astype(np.uint8)
    if mode == "RGB":
      return Image.fromarray(np.dstack([data, 255-data, data//2]), mode="RGB")
    return Image.fromarray(data, mode=mode)

  def test_default_generated_image(self):
    image = Tif()
    data = np.array(image.image)
    self.assertEqual(image.producer, "Default")
    self.assertEqual(image.image.size, (1024, 800))
    self.assertEqual(image.pixelSize, 1)
    self.assertEqual(image.width, 1024)
    self.assertEqual(data.min(), 0)
    self.assertEqual(data.max(), 255)
    self.assertGreater(np.count_nonzero(data == 0), 1000)
    self.assertGreater(np.count_nonzero(data == 255), 1000)

  def test_conventional_file_type_and_set_data_copy(self):
    with tempfile.TemporaryDirectory() as tmp:
      file_name = tmp + "/conventional.tif"
      self.make_image().save(file_name)
      image = Tif(file_name, fileType="Conventional", pixelSize=0.05)
      self.assertEqual(image.producer, "Conventional")
      self.assertAlmostEqual(image.width, 32*0.05)

      replacement = self.make_image(size=(12, 10))
      image.setData(replacement, pixelSize=0.2, copy=True)
      self.assertIsNotNone(image.origImage)
      self.assertAlmostEqual(image.width, 12*0.2)

  def test_scale_bar_crop_autocrop_save_and_enhance_paths(self):
    with tempfile.TemporaryDirectory() as tmp:
      file_name = tmp + "/image.tif"
      data = np.full((20, 30), 120, dtype=np.uint8)
      data[-3:, :] = 0
      Image.fromarray(data).save(file_name)

      image = Tif(file_name, fileType="Conventional", pixelSize=0.01)
      image.image = image.image.convert("P")
      image.findScaleBar()
      self.assertAlmostEqual(image.bestLength, 0.1)
      image.addScaleBar(site="TR", length=0.1)
      image.crop(xMax=20)
      image.crop(xMin=2)
      image.crop(yMax=12)
      image.crop(yMin=1)
      image.autoCrop("b")
      with redirect_stdout(StringIO()):
        image.enhance(method="equalization")
      image.enhance(method="adaptive", percent=1)
      image.save(fileType=tmp + "/saved.png", scale=2, convertGrayscale=True)

  def test_rgb_scale_bar_and_unsupported_enhance(self):
    with tempfile.TemporaryDirectory() as tmp:
      file_name = tmp + "/rgb.tif"
      self.make_image("RGB").save(file_name)
      image = Tif(file_name, fileType="Conventional", pixelSize=0.1)
      image.addScaleBar(site="BR", length=1)
      with redirect_stdout(StringIO()):
        image.enhance()
      self.assertEqual(image.image.mode, "RGB")

  def test_topology_and_remove_gray_gradient(self):
    with tempfile.TemporaryDirectory() as tmp:
      file_name = tmp + "/gradient.tif"
      self.make_image(size=(40, 30)).save(file_name)
      vertical = Tif(file_name, fileType="Conventional", pixelSize=0.02)
      vertical.topology(axis="V", start=1, end=10)
      horizontal = Tif(file_name, fileType="Conventional", pixelSize=0.02)
      horizontal.topology(axis="H", upperEnd=1.1, start=1, end=10)
      horizontal.removeGrayGradient(save=True, plot=False)
      self.assertEqual(horizontal.image.mode, "P")


if __name__ == "__main__":
  unittest.main()
