# -*- coding: utf-8 -*-
"""
Display and file output helpers for SEM TIF images.
"""
import os
from typing import TYPE_CHECKING
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure
from skimage.util import img_as_float

if TYPE_CHECKING:
  from .core import Tif


class TifDisplayMixin:
  """
  Display and save methods for :class:`Tif`.
  """

  def show(self:'Tif') -> None:  # type: ignore[misc]
    """
    Show image on screen
    """
    widthPixel, heightPixel = self.image.size
    if widthPixel>1024:
      self.image.resize( (1024, int(float(heightPixel)*1024.0/widthPixel)) ).show()
    else:
      self.image.show()
    return


  def plot(self:'Tif', axis:str='on', showDuration:int=-1) -> None:  # type: ignore[misc]
    """
    Show image on screen by plotting it: showing the pixel coordinates, which is handy for cropping

    Args:
      axis (str): 'on','off' show axis
      showDuration (int): show the image for n seconds. Show for infinity if -1
    """
    plt.imshow(self.image)
    plt.axis(axis)
    if showDuration > 0:
      plt.show(block = False)
      plt.pause(showDuration)
      plt.close()
    else:
      plt.show()
    return


  def hist(self:'Tif', log:bool=False, show:bool=True) -> None:  # type: ignore[misc]
    """
    Show grey-scale histogram and cumulative histogram

    Args:
       log (bool): use a logarithmic scale on the y-scale
       show (bool): show figure
    """
    #create histograms
    img = img_as_float(self.image)
    cdf, binsCDF = exposure.cumulative_distribution(img, 256)
    his, _ = exposure.histogram(img,256)
    his = his / float( max(his) )
    ind = np.arange( len(binsCDF) )
    #plot
    plt.bar(ind, his, color='k', log=int(log))
    plt.plot(ind, cdf, 'r', linewidth=2.0)
    plt.xlim([0,256])
    plt.xticks(np.arange(0, 257, 64))
    plt.xlabel('black --> white')
    if show:
      plt.show()
    return


  def save(self:'Tif', fileType:str="jpg", scale:float|None=None, convertGrayscale:bool=True) -> None:  # type: ignore[misc]
    """
    Save file as jpg, use the same base as initial TIF image

    Args:
       fileType (str): jpg, other options eps, png |br|
          alternative is to enter full filename (must be longer than 4 characters)
       scale (float): scale down image by ratio
       convertGrayscale (bool): convert to gray-scale image
    """
    if convertGrayscale:
      self.image = self.image.convert("L")
    fileName = os.path.splitext(self.fileName)[0]
    if fileType=="png":
      fileName+=".png"
    elif fileType=="jpg":
      fileName+=".jpg"
    elif fileType=="eps":
      fileName+=".eps"
    else:
      fileName = fileType
    if scale is not None:
      widthPixel, heightPixel = self.image.size
      self.image = self.image.resize( (int(widthPixel/scale), int(heightPixel/scale)) )
    #save to file
    self.image.save(fileName)
    return
