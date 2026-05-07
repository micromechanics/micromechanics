# -*- coding: utf-8 -*-
"""
Geometry transforms for SEM TIF images.
"""
from typing import TYPE_CHECKING
import numpy as np
from PIL import Image

if TYPE_CHECKING:
  from .core import Tif

class TifTransformMixin:
  """
  Rotation and flip methods for :class:`Tif`.
  """

  def rotateCCW(self:'Tif') -> None: # type: ignore[misc]
    """
    rotate image counter clock-wise
    """
    widthPixel = self.image.size[0]
    self.image = self.image.rotate(90)
    self.width = self.width * self.image.size[0]/widthPixel
    return


  def rotateCW(self:'Tif') -> None: # type: ignore[misc]
    """
    rotate image clock-wise
    """
    widthPixel = self.image.size[0]
    self.image = self.image.rotate(-90)
    self.width = self.width * self.image.size[0]/widthPixel
    return


  def rotate180(self:'Tif') -> None: # type: ignore[misc]
    """
    rotate image by 180 degrees
    """
    self.image = self.image.rotate(180)
    return


  def flip(self:'Tif') -> None: # type: ignore[misc]
    """
    flip image vertically
    """
    self.image = Image.fromarray(np.array(self.image)[::-1,:]).convert("P")
    return
