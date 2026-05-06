"""
SEM Gray-Value Gradient Correction
==================================

This example builds a small SEM-like grayscale image with an illumination
gradient and compares two correction methods used for cross-section images.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from micromechanics.tif import Tif

y, x = np.mgrid[0:160, 0:220]
matrix = 90 + 40*np.sin(x/18.0)*np.sin(y/24.0)
particles = 55*np.exp(-((x-80)**2+(y-70)**2)/(2*18**2))
illumination = 0.42*y
image_array = np.clip(matrix + particles + illumination, 0, 255).astype(np.uint8)

with TemporaryDirectory() as tmp:
  file_name = Path(tmp) / "synthetic_sem.tif"
  Image.fromarray(image_array).save(file_name)

  original = Tif(str(file_name), fileType="Conventional", pixelSize=0.02)

  leveled = Tif(str(file_name), fileType="Conventional", pixelSize=0.02)
  leveled.gaussLevel(level=18, plot=False, save=True)

  row_corrected = Tif(str(file_name), fileType="Conventional", pixelSize=0.02)
  row_corrected.removeGrayGradient(save=True, plot=False)

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, title, data in zip(axes,
                          ["original", "Gaussian leveled", "row corrected"],
                          [original.image, leveled.image, row_corrected.image]):
  ax.imshow(data, cmap="gray")
  ax.set_title(title)
  ax.axis("off")
plt.tight_layout()
