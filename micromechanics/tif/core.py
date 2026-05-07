# -*- coding: utf-8 -*-
"""
Class to allow for Zeiss/FEI-ThermoFischer TIF image loading and enhancing using python

- Unit: all sizes are in um: pixel-size, image-width
- All images have an image, pixelsize, width, height

"""
import logging
import os

from PIL import ImageFile, Image

from .output import TifDisplayMixin
from .input import TifInputMixin
from .processing import TifProcessingMixin
from .scalebar import TifScaleBarMixin
from .transform import TifTransformMixin

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Tif(TifInputMixin, TifScaleBarMixin, TifDisplayMixin, TifProcessingMixin, TifTransformMixin):
  """Tif class to read SEM images"""

  def __init__(self, fileName:str, fileType:str='', pixelSize:float=1):
    """
    Read input file, initialize things

    Args:
       fileName (str): file name in the present directory
       fileType (str): type of Tif file ("Zeiss", "NPVE", "Void", "NoQuestion") |br|
                       if no type is given, the type will be identified (which takes time) |br|
                       NoQuestion does not ask for non-Zeiss,NPVE file type
       pixelSize (float): pixel size for conventional tif-files
    """
    #initialize
    fontFile = os.path.dirname(os.path.abspath(__file__))+os.sep+'OpenSans-Regular.ttf'
    self.fontFile:str = ''
    if os.path.exists(fontFile):
      self.fontFile = fontFile
    else:
      logging.error("**ERROR** FOUND NO FONT FILE")
    self.fileName:str = fileName
    #set default values
    self.meta:dict[str,str]    = {}
    self.image:Image.Image
    self.origImage:Image.Image|None = None
    self.pixelSize:float       = -1
    self.width:float           = -1
    self.bestLength:float      = -1
    self.barPixel:int          = -1

    #read input file and identify the type
    self.producer = "Else"
    if not fileType:
      with open(self.fileName,'r', encoding='iso-8859-1') as fileHandle:
        for line in fileHandle:
          if "SV_SERIAL_NUMBER" in line:  #file starts with 49492a0008
            self.producer = "Zeiss"
            break
          if "[User]" in line:
            self.producer = "FEI"
            break
          if '<Fibics version="1.0">' in line:
            self.producer = "NPVE"
            break
          if 'ImageJ=' in line:
            self.producer = 'ImageJ'  #not handled since I don't see any length or unit in it
            break
    else:
      self.producer = fileType
    if self.producer=='Else':
      with open(self.fileName,'rb') as fIn:   #based on initial digits
        if fIn.read(16).hex()=='49492a0010c000005448554d42313238':
          self.producer = 'TEM'

    logging.info("Open file: "+fileName+' producer '+self.producer)    #all other types
    if self.producer == "Zeiss":
      self.initZeiss()
    elif self.producer == "NPVE":
      self.initNPVE()
    elif self.producer == "FEI":
      self.initFEI()
    else:
      self.initConventional(pixelSize)
