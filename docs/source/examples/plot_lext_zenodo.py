#!/usr/bin/env python3
"""
Olympus LEXT Files From Zenodo
==============================

This example downloads Olympus LEXT OLS4100 confocal microscope data from
Zenodo, extracts the ``.lext`` files, converts each intensity channel to a
display image, enhances it, and adds a scale bar.

Data source
-----------

Title:
  Raw data on tribometry of laser structured copper surfaces
Authors:
  Sebastian Suarez, Bruno Alderete, Fabian Bonner, Silas Daniel Schütz,
  Frank Thomas Mücklich
Zenodo:
  https://zenodo.org/records/17814735
"""

import os
import shutil
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree
from zipfile import ZipFile

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import tifffile

from micromechanics.tif import Tif


DATA_URL = "https://zenodo.org/api/records/17814735/files/Files%20CLSM.zip/content"
EXAMPLE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd().resolve()
DATA_DIR = EXAMPLE_DIR / "_downloads" / "lext_zenodo_17814735"
ZIP_PATH = DATA_DIR / "Files CLSM.zip"
LEXT_DIR = DATA_DIR / "Files CLSM"


def download_and_unpack() -> Path:
  """Download and unpack the Zenodo archive if the data are not present."""
  DATA_DIR.mkdir(parents=True, exist_ok=True)
  if not ZIP_PATH.exists():
    print("Downloading", DATA_URL)
    temporary_path = ZIP_PATH.with_suffix(".zip.part")
    with urlopen(DATA_URL, timeout=60) as response, temporary_path.open("wb") as file_handle:
      shutil.copyfileobj(response, file_handle)
    temporary_path.replace(ZIP_PATH)
  if not any(LEXT_DIR.glob("*.lext")):
    print("Unpacking", ZIP_PATH)
    with ZipFile(ZIP_PATH) as archive:
      archive.extractall(DATA_DIR)
  return LEXT_DIR


def processLext(path: Path, channel: str = "intensity") -> Path:
  """Read the lext file, create a display image, and save it as png."""
  with tifffile.TiffFile(path) as tif:
    lext_description = tif.pages[0].description or ""
    channels = {"intensity": 0}
    for page_index, page in enumerate(tif.pages):
      description = (page.description or "").strip()
      if description == "INTENSITY":
        channels["intensity"] = page_index
      elif description == "HEIGHT":
        channels["height"] = page_index
    print("  Available channels:", ", ".join(channels))
    data = tif.pages[channels[channel]].asarray()
  root = ElementTree.fromstring(lext_description)
  tag_name = "HeightDataPerPixelX" if channel == "height" else "IntensityDataPerPixelX"
  tag = root.find(f".//{tag_name}")
  if tag is None or tag.text is None:
    raise ValueError(f"Could not find {tag_name} in {path}")
  pixel_size = float(tag.text) / 1_000_000.0  # Olympus LEXT stores lateral spacing in picometers in these files.

  values = data.astype(np.float64, copy=False)
  low, high = np.percentile(values, (0.5, 99.5))
  if high <= low:
    high = low + 1.0
  scaled = np.clip((values - low) / (high - low), 0.0, 1.0)
  image = Image.fromarray((scaled * 255).astype(np.uint8)).convert("L")

  # custom resizing
  # targetWidthPx = round(640 / pixel_size) # make image exactly 640um wide
  # if image.size[0] > targetWidthPx:
  #   image = image.crop((0, 0, targetWidthPx, image.size[1]))
  # targetHeightPx = round(480 / pixel_size) # make image exactly 480um tall
  # if image.size[1] > targetHeightPx:
  #   image = image.crop((0, 0, image.size[0], targetHeightPx))

  tif = Tif()
  tif.setData(image, pixel_size)
  tif.enhance("adaptive")
  tif.addScaleBar("BR", scale=int(tif.width / 7.0))
  output_path = path.with_suffix(".png")
  tif.image.convert("RGB").save(output_path)
  print(f"  pixelSize={pixel_size:g} um, width={tif.width:g} um, height={tif.image.size[1]*pixel_size:g} um")
  return output_path


###############################################################################
# Download the public Zenodo archive only once, unpack it, and process all LEXT
# files in the archive. Generated PNG files are written next to the extracted
# measurement files under ``docs/source/examples/_downloads/``.

lext_dir = download_and_unpack()
output_paths = []
for file_name in sorted(os.listdir(lext_dir)):
  if not file_name.endswith(".lext"):
    continue
  print("Processing", file_name)
  output_paths.append(processLext(lext_dir / file_name, "intensity"))

###############################################################################
# Display the first processed image in the generated documentation page.

first_image = Image.open(output_paths[0])
plt.imshow(first_image)
plt.axis("off")
