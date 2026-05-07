# -*- coding: utf-8 -*-
"""
Class to allow for Zeiss/FEI-ThermoFischer TIF image loading and enhancing using python

- Unit: all sizes are in um: pixel-size, image-width
- All images have an image, pixelsize, width, height

"""
from .core import Tif

__all__ = ["Tif"]
