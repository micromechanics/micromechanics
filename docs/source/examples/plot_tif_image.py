"""
Tif Image Processing
====================

This example opens a Zeiss TIF image, enhances the gray values, adds a scale
bar, and displays the processed image.
"""

from pathlib import Path

import matplotlib.pyplot as plt

import micromechanics
from micromechanics.tif import Tif

repository_root = Path(micromechanics.__file__).resolve().parents[1]
file_name = repository_root / "examples" / "Zeiss" / "Zeiss.tif"

image = Tif(str(file_name))
image.enhance()
image.addScaleBar()

plt.imshow(image.image, cmap="gray")
plt.axis("off")
