# -*- coding: utf-8 -*-
"""
Input and metadata readers for SEM TIF images.
"""
from typing import TYPE_CHECKING
import logging
import re
import warnings
from xml.etree import ElementTree

from PIL import Image

if TYPE_CHECKING:
  from .core import Tif

class TifInputMixin:
  """
  File loading helpers for :class:`Tif`.
  """

  def initZeiss(self:'Tif') -> None:  # type: ignore[misc]
    """
    Init ZEISS file
    """
    with warnings.catch_warnings():
      warnings.filterwarnings('ignore',category=ResourceWarning)  #Image open sometimes triggers "ResourceWarning"
      self.image     = Image.open(self.fileName).convert("L").convert("P")
    self.origImage:Image.Image|None = self.image.copy()
    #parse for information
    self.meta['measurementType'] = 'Zeiss SEM TIF-Image'
    with open(self.fileName,'r', encoding='iso-8859-1') as fIn:
      for line in fIn:
        if " = " in line:
          key, value = line.split("=")
          key = key.strip().replace(' ','_')
          value=value.strip()
          self.meta[key]=value
          if key=='File_Name': #don't get confused by subsequent '='
            break
    # meta data checks and handling
    valueArray = self.meta['Width'].split()
    self.width = float(valueArray[0])  #guess it is um
    if valueArray[1]=='mm': self.width *= 1000
    if valueArray[1]=='nm': self.width /= 1000
    valueArray = self.meta['Image_Pixel_Size'].split()
    self.pixelSize = float(valueArray[0])/1000  #guess it is nm
    if valueArray[1]=='nm':
      self.pixelSize = self.pixelSize
    elif valueArray[1].encode('utf-8')==b'\xc2\xb5m':  #um
      self.pixelSize *= 1000
    else:
      logging.error("**ERROR** Pixel size not nm or um")
      return
    valueArray = self.meta['Store_resolution'].split()
    widthPixel  = int(valueArray[0])
    logging.info("  Picture width "+str(self.width)+"[um], pixel size: "+str(self.pixelSize)+" [um], widthPixel "+str(widthPixel))
    if abs(widthPixel*self.pixelSize-self.width)/self.width > 0.01:
      logging.error("**ERROR** Width, PixelSize, Width "+str(widthPixel)+' '+str(self.pixelSize)+' '+str(self.width))
      logging.error("**ERROR** Data keys error")
    return


  def initNPVE(self:'Tif') -> None:  # type: ignore[misc]
    """
    Init NPVE file, no original image saved since files are large
    """
    logging.info("  Start initNPVE")
    with warnings.catch_warnings():
      warnings.filterwarnings('ignore',category=ResourceWarning)  #Image open sometimes triggers "ResourceWarning"
      image = Image.open(self.fileName).convert("L").convert("P")
    self.image = image
    self.origImage = None #do not save, since files rather large
    widthPixel = image.size[0]

    #parse the xml line in the file
    xmlLine = ""
    with open(self.fileName,'r', encoding='iso-8859-1') as fIn:
      for line in fIn:
        if '<Fibics version="1.0">' in line:
          xmlLine = line
          break
    xmlLine  = re.sub(r'[^\x00-\x7F]+',' ', xmlLine)  #clean off any non-ascii characters
    xmlObject= ElementTree.fromstring(xmlLine)        #parse it
    requiredKeys = ['Width', 'Height', 'FOV_X', 'Ux', 'Vy']
    optionalKeys = ['Contrast', 'Brightness']
    for key in requiredKeys + optionalKeys:
      element = xmlObject.find('.//'+key)
      if element is not None and element.text is not None:
        self.meta[key.lower()] = element.text

    # meta data checks and handling
    if all(key.lower() in self.meta for key in requiredKeys):
      self.width = float(self.meta['fov_x'])  #guess it is um
      fovElement = xmlObject.find(".//FOV_X")
      if fovElement is None or fovElement.get("units") != "um":
        print("**ERROR** field of view not in um", None if fovElement is None else fovElement.get("units"))
        return
      print("Picture width",self.width,'[um]')
      self.pixelSize = float(self.meta['fov_x'])/float(self.meta['width'])  #guess it is um
      print("Pixel size",self.pixelSize,'[um]')
      self.meta['pixelSize'] = str(self.pixelSize)
      widthPixel  = int(self.meta['width'])
      print("widthPixel",widthPixel)
      if abs(widthPixel*self.pixelSize-self.width)/self.width > 0.01:
        print("**ERROR** Width, PixelSize, Width", widthPixel,self.pixelSize,self.width)
        print("**ERROR** Data keys error")
        return
    else:
      print("**ERROR** Some required keys were missing. Found keys:\n",self.meta)
      return


  def initFEI(self:'Tif') -> None:  # type: ignore[misc]
    """
    Init FEI / ThermoFischer file
    """
    logging.info("  Start initFEI")
    with warnings.catch_warnings():
      warnings.filterwarnings('ignore',category=ResourceWarning)  #Image open sometimes triggers "ResourceWarning"
      self.image     = Image.open(self.fileName).convert("L").convert("P")
    self.origImage = self.image.copy()

    #parse for information
    self.meta['measurementType'] = 'FEI SEM TIF-Image'
    with open(self.fileName,'rb') as fIn:
      metadataBytes = fIn.read()
      found = int(metadataBytes.hex().find('5B557365725D'.lower())/2) #/2 since two letters=1byte; corresponds to [USER]
      metadataLines = metadataBytes[found:].decode('utf-8', errors='replace').split('\n')
      self.meta = {i.split('=')[0]:i.split('=')[1].strip() for i in metadataLines if '=' in i }

    # metadata handling
    self.width = float(self.meta['HorFieldsize'])*1.e6  #uses SI unit m
    logging.info("  Picture width "+str(self.width)+'[um]')
    self.pixelSize = float(self.meta['PixelWidth'])*1.e6  #uses SI unit m
    logging.info("  Pixel size "+str(self.pixelSize)+'[um]')
    widthPixel = int(self.meta['ResolutionX'])
    logging.info("  widthPixel "+str(widthPixel))
    return


  def initConventional(self:'Tif', pixelSize:float=1) -> None:  # type: ignore[misc]
    """
    Init conventional file

    Args:
       pixelSize (float): pixel size in um
    """
    logging.info("  Start initConventional")
    self.origImage = Image.open(self.fileName)
    self.image     = self.origImage.copy()
    widthPixel = self.image.size[0]
    logging.info("widthPixel "+str(widthPixel))
    self.pixelSize = pixelSize
    logging.info("Pixel size "+str(self.pixelSize)+' [um]')
    self.width = self.pixelSize * widthPixel
    logging.info("Picture width "+str(self.width)+'[um]')
    return


  def setData(self:'Tif', image:Image.Image, pixelSize:float, copy:bool=True ) -> None:  # type: ignore[misc]
    """
    import data, image and pixelSize from another source |br|
    (image, pixelSize): image and pixelSize in a list

    Args:
      image (PIL): image
      pixelSize (float): pixelSize
      copy (bool): create backup copy. Don't do if big file
    """
    if copy:
      self.origImage = image.convert("P")
    self.image     = image.convert("P")
    widthPixel = self.image.size[0]
    print("widthPixel",widthPixel)
    self.pixelSize = pixelSize
    print("Pixel size",self.pixelSize,'[um]')
    self.width = self.pixelSize * widthPixel
    print("Picture width",self.width,'[um]')
    return
