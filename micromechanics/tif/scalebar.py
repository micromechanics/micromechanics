# -*- coding: utf-8 -*-
"""
Scale-bar helpers for SEM TIF images.
"""
import logging
import math

from PIL import ImageDraw, ImageFont


class TifScaleBarMixin:
  """
  Scale-bar methods for :class:`Tif`.
  """

  def findScaleBar(self,length=None):
    """
    Find the optimal scale-bar, if no length is given

    Args:
       length (float): length of scale bar in um, only integer values are used
    """
    if length is None:
      quarter = round(self.width/4.)
      if quarter>=1:
        digits = int(math.log10(quarter))
        self.bestLength = round(self.width/4., -digits)
      else:
        self.bestLength = 0.1
    else:
      self.bestLength = length
    widthPixel = self.image.size[0]
    self.barPixel = int(widthPixel * self.bestLength/self.width)
    return


  def addScaleBar(self, site="BL", length=None, scale = -1):
    """
    Add scale-bar to image

    Args:
       site (str): where to put the scale bar: bottom-left "BL", bottom-right "BR", top-left "TL", top-right "TR", bottom "B"
       length (float): length of scale bar in um; if not give calculate automatically
       scale (int): of font and rectangle. Default: widthInPixel / 16, which is for a 1024x786 image = 64
    """
    if self.bestLength < 0 or length is not None:
      self.findScaleBar(length)
    draw = ImageDraw.Draw(self.image)
    widthPixel, heightPixel = self.image.size
    if scale < 0:
      scale = widthPixel / 16
    font = ImageFont.truetype(self.fontFile,int(scale/5*3) )
    #identify top-left corner of scale bar section
    if   site=="BR":  offsetX = widthPixel-self.barPixel-scale/5;    offsetY = heightPixel-scale
    elif site=="TL":  offsetX = 0;                                   offsetY = 0
    elif site=="TR":  offsetX = widthPixel-self.barPixel-scale/5;    offsetY = 0
    elif site=="B" :  offsetX =(widthPixel-self.barPixel-scale/5)/2; offsetY = heightPixel-scale
    else:             offsetX = 0;                                   offsetY = heightPixel-scale   #BL
    if self.bestLength<0.5:
      textString = str(int(self.bestLength*1000.))+" nm"
    else:
      textString = str(int(self.bestLength))+" \u03BCm"
    textWidth = draw.textlength( textString, font=font)
    logging.info("  Scale bar length="+str(self.bestLength)+" ="+str(self.barPixel)+"[px], font scale: "+str(scale))
    if self.image.mode == "P":
      draw.rectangle((offsetX,        offsetY,         offsetX+self.barPixel+scale/5,  offsetY+scale    ), fill=256)  #white background
      draw.rectangle((offsetX+scale/10, offsetY+scale*7/10, offsetX+self.barPixel+scale/10, offsetY+scale*9/10), fill=0)    #black bar
      draw.text( (offsetX+(self.barPixel+scale/5-textWidth)/2,offsetY-2), textString, font=font)
    elif self.image.mode == "RGB":
      draw.rectangle((offsetX,        offsetY,         offsetX+self.barPixel+scale/5,  offsetY+scale    ), 'white')  #white background
      draw.rectangle((offsetX+scale/10, offsetY+scale*7/10, offsetX+self.barPixel+scale/10, offsetY+scale*9/10), 'black')    #black bar
      draw.text( (offsetX+(self.barPixel+scale/5-textWidth)/2,offsetY), textString, 'black', font=font)
    else:
      logging.error("**ERROR** image mode not supported "+self.image.mode)
