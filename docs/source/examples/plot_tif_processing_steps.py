"""
Tif Processing Steps
====================

This example applies common processing steps to a Zeiss SEM TIF image and
compares the intermediate results.
"""

from pathlib import Path

import matplotlib.pyplot as plt

import micromechanics
from micromechanics.tif import Tif

repository_root = Path(micromechanics.__file__).resolve().parents[1]
file_name = repository_root / "examples" / "Zeiss" / "Zeiss.tif"

image = Tif(str(file_name))
image.crop(xMin=50, xMax=450, yMin=50, yMax=350)
cropped = image.image.copy()

image.medianFilter(level=2)
image.gaussFilter(level=1)
filtered = image.image.copy()

image.contrast(magnitude=1.4, offset=0.45, save=True)
image.addScaleBar(site="BR", length=1)
processed = image.image.copy()

fig, axes = plt.subplots(1, 3, figsize=(9, 3))
for ax, title, data in zip(axes,
                          ["cropped", "filtered", "processed"],
                          [cropped, filtered, processed]):
  ax.imshow(data, cmap="gray")
  ax.set_title(title)
  ax.axis("off")

plt.tight_layout()
