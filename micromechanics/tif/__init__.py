# -*- coding: utf-8 -*-
"""
Class to allow for Zeiss/FEI-ThermoFischer TIF image loading and enhancing using python

- Unit: all sizes are in um: pixel-size, image-width
- All images have an image, pixelsize, width, height

"""
import logging, re, math, os, sys, warnings, codecs
from xml.dom import minidom
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
from skimage import img_as_float, exposure
import cv2

class Tif:
  """Tif class to read SEM images"""

  ##
  # @name IMPORT METHODS
  #@{
  def __init__(self, fileName, fileType=None, pixelSize=1):
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
    if os.path.exists(fontFile):
      self.fontFile = fontFile
    else:
      logging.error("**ERROR: FOUND NO FONT FILE")
      self.fontFile = None
    self.fileName = fileName
    #set default values
    self.meta = {}
    self.image = None
    self.origImage = None
    self.pixelSize = -1
    self.width = -1
    self.widthPixel = -1
    self.heightPixel = -1
    self.bestLength = -1
    self.barPixel = -1

    #read input file and identify the type
    self.producer = "Else"
    if fileType is None:
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


  def initZeiss(self):
    """
    Init ZEISS file
    """
    logging.info("  Start initZeiss")
    with warnings.catch_warnings():
      warnings.filterwarnings('ignore',category=ResourceWarning)  #Image open sometimes triggers "ResourceWarning"
      self.image     = Image.open(self.fileName).convert("L").convert("P")
    self.origImage = self.image.copy()

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
    logging.info("  Picture width "+str(self.width)+' [um]')
    valueArray = self.meta['Image_Pixel_Size'].split()
    self.pixelSize = float(valueArray[0])/1000  #guess it is nm
    if valueArray[1]=='nm':
      self.pixelSize = self.pixelSize
    elif valueArray[1].encode('utf-8')==b'\xc2\xb5m':  #um
      self.pixelSize *= 1000
    else:
      logging.error("  Pixel size not nm or um")
      return
    logging.info("  Pixel size "+str(self.pixelSize)+' [um]')
    valueArray = self.meta['Store_resolution'].split()
    self.widthPixel  = int(valueArray[0])
    self.heightPixel = int(valueArray[2])
    logging.info("  widthPixel "+str(self.widthPixel))
    if abs(self.widthPixel*self.pixelSize-self.width)/self.width > 0.01:
      logging.error("Width, PixelSize, Width "+str(self.widthPixel)+' '+str(self.pixelSize)+' '+str(self.width))
      logging.error("Data keys error")
    return


  def initNPVE(self):
    """
    Init NPVE file, no original image saved since files are large
    """
    logging.info("  Start initNPVE")
    imgArray = cv2.imread(self.fileName)[:,:,0]
    self.image = Image.fromarray(imgArray).convert("P")
    self.origImage = None #do not save, since files rather large
    self.widthPixel, self.heightPixel = imgArray.shape

    #parse the xml line in the file
    xmlLine = ""
    with open(self.fileName,'r', encoding='iso-8859-1') as fIn:
      for line in fIn:
        if '<Fibics version="1.0">' in line:
          xmlLine = line
          break
    xmlLine  = re.sub(r'[^\x00-\x7F]+',' ', xmlLine)  #clean off any non-ascii characters
    xmlData  = minidom.parseString(xmlLine)           #parse it
    xmlObject= xmlData.documentElement		       #make an object
    keys = ['Width', 'Height', 'Contrast', 'Brightness', 'FOV_X', 'Ux', 'Vy']
    for key in keys:
      self.meta[key.lower()] = xmlObject.getElementsByTagName(key)[0].childNodes[0].data

    # meta data checks and handling
    if len(keys) == len(self.meta):
      self.width = float(self.meta['fov_x'])  #guess it is um
      if xmlObject.getElementsByTagName("FOV_X")[0].getAttribute("units") != "um":
        print("Error field of view not in um", xmlObject.getElementsByTagName("FOV_X")[0].getAttribute("units"))
        return
      print("Picture width",self.width,'[um]')
      self.pixelSize = float(self.meta['fov_x'])/float(self.meta['width'])  #guess it is um
      print("Pixel size",self.pixelSize,'[um]')
      self.meta['pixelSize'] = self.pixelSize
      self.widthPixel  = int(self.meta['width'])
      self.heightPixel = int(self.meta['height'])
      print("widthPixel",self.widthPixel)
      if abs(self.widthPixel*self.pixelSize-self.width)/self.width > 0.01:
        print("Width, PixelSize, Width", self.widthPixel,self.pixelSize,self.width)
        print("Data keys error")
        return
    else:
      print("Some keys were missing. Found keys:\n",self.meta)
      return


  def initFEI(self):
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
      metadata = fIn.read()
      found = int(metadata.hex().find('5B557365725D'.lower())/2) #/2 since two letters=1byte; corresponds to [USER]
      metadata = bytearray(source=metadata[found:]).decode('utf-8', errors='replace').split('\n')
      self.meta = {i.split('=')[0]:i.split('=')[1].strip() for i in metadata if '=' in i }

    # metadata handling
    self.width = float(self.meta['HorFieldsize'])*1.e6  #uses SI unit m
    logging.info("  Picture width "+str(self.width)+'[um]')
    self.pixelSize = float(self.meta['PixelWidth'])*1.e6  #uses SI unit m
    logging.info("  Pixel size "+str(self.pixelSize)+'[um]')
    self.widthPixel = int(self.meta['ResolutionX'])
    self.heightPixel = int(self.meta['ResolutionY'])
    logging.info("  widthPixel "+str(self.widthPixel))
    return


  def initConventional(self, pixelSize=1):
    """
    Init conventional file

    Args:
       pixelSize (float): pixel size in um
    """
    logging.info("  Start initConventional")
    self.origImage = Image.open(self.fileName)
    self.image     = self.origImage.copy()
    self.widthPixel, self.heightPixel = self.image.size
    logging.info("widthPixel "+str(self.widthPixel))
    self.pixelSize = pixelSize
    logging.info("Pixel size "+str(self.pixelSize)+' [um]')
    self.width = self.pixelSize * self.widthPixel
    logging.info("Picture width "+str(self.width)+'[um]')
    return


  def setData(self, image, pixelSize, copy=True ):
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
    self.widthPixel, self.heightPixel = self.image.size
    print("widthPixel",self.widthPixel)
    self.pixelSize = pixelSize
    print("Pixel size",self.pixelSize,'[um]')
    self.width = self.pixelSize * self.widthPixel
    print("Picture width",self.width,'[um]')
    return


  #@}
  ##
  # @name SCALE-BAR METHODS
  #@{

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
    self.barPixel = int(self.widthPixel * self.bestLength/self.width)
    logging.info("Scale bar length="+str(self.bestLength)+"  and in pixel="+str(self.barPixel))
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
    if scale < 0:
      scale = self.widthPixel / 16
    font = ImageFont.truetype(self.fontFile,int(scale/5*3) )
    #identify top-left corner of scale bar section
    if   site=="BR":  offsetX = self.widthPixel-self.barPixel-scale/5;    offsetY = self.heightPixel-scale
    elif site=="TL":  offsetX = 0;				          offsetY = 0
    elif site=="TR":  offsetX = self.widthPixel-self.barPixel-scale/5;    offsetY = 0
    elif site=="B" :  offsetX =(self.widthPixel-self.barPixel-scale/5)/2; offsetY = self.heightPixel-scale
    else:             offsetX = 0;                                        offsetY = self.heightPixel-scale   #BL
    if self.bestLength<0.5:
      textString = str(int(self.bestLength*1000.))+" nm"
    else:
      textString = str(int(self.bestLength))+" \u03BCm"
    textWidth, _ = draw.textsize( textString, font=font)
    logging.info("Scale used"+str(scale))
    if self.image.mode == "P":
      draw.rectangle((offsetX,        offsetY,         offsetX+self.barPixel+scale/5,  offsetY+scale    ), fill=256)  #white background
      draw.rectangle((offsetX+scale/10, offsetY+scale*7/10, offsetX+self.barPixel+scale/10, offsetY+scale*9/10), fill=0)    #black bar
      draw.text( (offsetX+(self.barPixel+scale/5-textWidth)/2,offsetY), textString, font=font)
    elif self.image.mode == "RGB":
      draw.rectangle((offsetX,        offsetY,         offsetX+self.barPixel+scale/5,  offsetY+scale    ), 'white')  #white background
      draw.rectangle((offsetX+scale/10, offsetY+scale*7/10, offsetX+self.barPixel+scale/10, offsetY+scale*9/10), 'black')    #black bar
      draw.text( (offsetX+(self.barPixel+scale/5-textWidth)/2,offsetY), textString, 'black', font=font)
    else:
      logging.error("image mode not supported "+self.image.mode)



  #@}
  ##
  # @name METHODS TO PLOT, SAVE
  #@{

  def show(self):
    """
    Show image on screen
    """
    if self.widthPixel>1024:
      self.image.resize( (1024, int(float(self.heightPixel)*1024.0/self.widthPixel)) ).show()
    else:
      self.image.show()
    return


  def plot(self):
    """
    Show image on screen by plotting it: showing the pixel coordinates, which is handy for cropping
    """
    plt.imshow(self.image)
    plt.show()
    return


  def reset(self):
    """
    Reset it if you want to restart after making unwanted change
    """
    self.image = self.origImage
    self.widthPixel, self.heightPixel = self.image.size
    return


  def hist(self, log=False, show=True):
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

  def save(self, fileType="jpg", scale=None, convertGrayscale=True):
    """
    Save file as jpg, use the same base as initial TIF image

    Args:
       fileType (str): jpg, other options eps, png |br|
          alternative is to enter full filename (must be longer than 4 characters)
       scale (float): scale down image by ratio
       convertGrayscale (bool): convert to gray-scale image
    """
    if convertGrayscale: self.image = self.image.convert("L")
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
      self.image = self.image.resize( (self.widthPixel/scale, self.heightPixel/scale) )
    #save to file
    self.image.save(fileName)
    return


  #@}
  ##
  # @name METHODS TO CHANGE THE IMAGE
  #@{

  def crop(self, xMin=-1, xMax=-1, yMin=-1, yMax=-1):
    """
    Crop image: set those that you want to crop, unset ones are not altered

    Args:
       xMin (int): minimum x-value that should be cut away
       xMax (int): maximum x-value that should be cut away
       yMin (int): minimum y-value that should be cut away
       yMax (int): maximum y-value that should be cut away
    """
    tempArray = np.array(self.image)
    if xMin>-1  and xMax>-1:
      tempArray = tempArray[:,xMin:xMax]
    if xMin==-1 and xMax>-1:
      tempArray = tempArray[:,0:xMax]
    if xMin>-1  and xMax==-1:
      tempArray = tempArray[:,xMin:]
    if yMin>-1  and yMax>-1:
      tempArray = tempArray[yMin:yMax,:]
    if yMin==-1 and yMax>-1:
      tempArray = tempArray[0:yMax,:]
    if yMin>-1  and yMax==-1:
      tempArray = tempArray[yMin:,:]
    self.image = Image.fromarray(tempArray).convert('P')
    self.widthPixel, self.heightPixel = self.image.size
    print("   After cropping: new size of image: ",self.widthPixel, self.heightPixel)
    self.width = self.widthPixel*self.pixelSize
    return


  def autoCrop(self, color='w'):
    """
    Automatically crop the bottom bar from the image.
    The top line cropped is the line that only contains white/black pixel

    Args:
      color (str): color to crop black=b, white=w
    """
    lineAvg = np.sum(self.image, axis=1) /self.image.size[0]
    if color=='w':
      lineThreshold = np.where(lineAvg==255)[0]
    elif color=='b':
      lineThreshold = np.where(lineAvg==0)[0]
    else:
      print('**ERROR, only know colors b,w')
    if len(lineThreshold)>0:
      self.crop(yMax=lineThreshold[0])
    return


  def enhance(self, method='rescale', percent=1):
    """
    Automatic contrast improvement |br|
    mode = 1 black-white |br|
    mode = L grey-scale |br|
    read http://scikit-image.org/docs/0.9.x/auto_examples/plot_equalize.html for details |br|

    Args:
       method (str):

	      - 'rescale' or 'r': Automatic gray-value rescaling, default, smallest change
	      - 'adaptive' or 'a': Gray equalization, leads to centered Gaussian curve, medium change, favorite
	      - 'equalization' or 'e': Gray equalization, leads to cumulative histogram that is a line largest change
       percent (int): percent (default: 0) to allow for clipping at the top and at the bottom
	      (e.g. top 1% of values become white and bottom 1% of values become black
    """
    if self.image.mode == 'P':
      if method in ['equalization', 'e']:
        self.image = Image.fromarray(exposure.equalize_hist(np.array(self.image))*255).convert('P')
        print('something not correct here')
      if method in ['rescale', 'r']:
        pMin, pMax = np.percentile(self.image, (percent, 100-percent))
        self.image = Image.fromarray(exposure.rescale_intensity(np.array(self.image), in_range=(pMin, pMax))).convert('P')
      if method in ['adaptive', 'a']:
        try:
          self.image = Image.fromarray(exposure.equalize_adapthist(np.array(self.image), clip_limit=percent/100.)*255).convert('P')
        except:
          print("Exception hit in Tif.py:426")
    elif self.image.mode == "RGB":
      print('enhancement does not work work for color images')
      print('Do first: i.image = i.image.convert(mode="L")')
      print('Do second: i.image = i.image.convert(mode="P")')
    else:
      print("Image type not supported")
    return


  def medianFilter(self, level=1, recursive=1):
    """
    Use median filter (remove single pixel noise)

    Args:
       level (int): radius of median filter in pixel, the larger the slower the algorithm
       recursive (int): subsequent iterations of filter, default=1=no recursive
    """
    if level < 1:
      return
    for _ in range(0, recursive):
      self.image = Image.fromarray(  ndimage.median_filter(self.image, level) )
    self.image = self.image.convert("P")
    return


  def gaussFilter(self, level=1, recursive=1):
    """
    Use gaussian filter (smooth pixels, much more smoothing than median)

    Args:
       level (int): radius of gauss filter in pixel
       recursive (int): subsequent iterations of filter, default=1=no recursive
    """
    if level < 1:
      return
    for _ in range(0, recursive):
      self.image = Image.fromarray(  ndimage.gaussian_filter(self.image, level) )
    return


  def gaussLevel(self, level=100, plot=True, save=False):
    """
    excenturate and remove gradients

    Args:
       level (int): radius used for leveling
       plot (bool): plot graphs during processing
       save (bool): only save once set true; allows to test varios settings before saving
    """
    level = ndimage.gaussian_filter(self.image, level)
    imArray = np.array(self.image).astype(np.float64) - level
    imArray -= np.min(imArray)
    imArray *= 255.0/np.max(imArray)
    imArray = imArray.astype(np.uint8)
    if plot:
      plt.imshow(np.array(self.image), cmap="gray")
      plt.title("Original")
      plt.colorbar()
      plt.show()
      plt.imshow(imArray,cmap="gray")
      plt.title("New")
      plt.colorbar()
      plt.show()
    if save:
      self.image = Image.fromarray(imArray).convert("P")
    else:
      print("NOT SAVED")
    return


  def contrast(self,magnitude=1, offset=0.5, yoffset=1.0, save=False, plot=False, points=31):
    """
    Manual contrast improvement: fast but memory expensive

    Args:
       magnitude (float): curve curvature image: figZeiss1.png
       offset (float): move neutral point up-down diagonal image: figZeiss2.png
       yoffset (float): move neutral point up-down image: figZeiss3.png
       save (bool): save resulting contrast change
       plot (bool): plot the desired curve on the screen, no contrast changes are performed to the image.|br|
             this is to verify ones choice
       points (int): smoothness of curve, the more the smoother
    """
    def curve(x,magnitude,offset, yoffset):
      #print "min max",np.min(x), np.max(x), np.mean(x)
      mask = x<offset
      y = np.empty_like(x)
      y[mask] =                   np.power(x[mask]/offset, magnitude) * offset * yoffset
      mask = np.invert(mask)
      y[mask] =  1.0 - np.power(np.absolute(1.0-x[mask])/(1.-offset),magnitude)*(1.-offset*yoffset)
      #print "min max",np.min(y), np.max(y), np.mean(y)
      return y
    tempArray = curve( np.array(self.image).astype(np.float16)/255, magnitude, offset, yoffset)
    tempArray = (tempArray*255).astype(np.uint8)
    #plot & save
    if plot:
      plt.subplot(131)
      plt.imshow(np.array(self.image),cmap='gray')
      plt.title("Before")
      plt.axis('off')
      #---------------
      plt.subplot(132)
      x= np.linspace(0,1.0,points)
      y= curve(x, magnitude,offset, yoffset)
      self.hist(False, False)
      plt.plot(x*256,y,'-b',label='contrast')
      plt.plot([0,256],[0,1],'--b',label='diagonal')
      plt.legend(loc=4)
      plt.title("Contrast")
      #---------------
      plt.subplot(133)
      plt.imshow( tempArray,cmap='gray')
      plt.title("After")
      plt.axis('off')
      plt.show()
    if save:
      self.image = Image.fromarray(tempArray).convert("P")
    return


  def topology(self, axis="V", upperEnd=4.0, start=-1, end=-1):
    """
    rescale grey values such that each row/collum has the same average, cancel topological shadowing

    The algorithm tries to scale (change contrast) the grey-values such as that each collum (V) or
    row (H) has the same average grey value. However:

    - It is not allowed to scaling down (<1) [because that deletes contrast]
    - or scale more than upperEnd [because then the image becomes to pixely]

    To still reach the given average: the grey scales are shifted (change brightness)

    Args:
       axis (str): "V" vertical or "H" horizontal
       upperEnd (float): maximum scaling allowed
       start (int): start scaling only in row/collum. default=-1=scale everything
       end (int): end scaling in row/collum. default=-1=scale everything
    """
    imageArray = np.array(self.image)/255.  			#convert to array
    # evaluate mean (scalar) and average (collum/row vector)
    mean = imageArray.mean()		   			#get mean of original image
    if axis=="V":
      average = imageArray.sum(axis=0) / self.heightPixel	#get average of every collum, this is a vector
    else:
      average = imageArray.sum(axis=1) / self.widthPixel
    scale = mean / average					#scaling factor vector
    # do actual change of the pixels
    start = max(start, 0)
    if end<0:
      end = len(scale)  					#use scale here since it automatically adopts to horizontal/vertical
    for i in range (start, end):
      if scale[i]< 1:
        effScale = 1.0
      elif scale[i]>upperEnd:
        effScale = upperEnd
      else:
        effScale = scale[i]
      effShift = mean - average[i]*effScale
      if axis=="V":
        imageArray[:,i] = imageArray[:,i]*effScale + effShift
      else:
        imageArray[i,:] = imageArray[i,:]*effScale + effShift
    self.image =  Image.fromarray(  (imageArray*255).astype(np.uint8)  ).convert("P")
    return


  def filterCurtain(self, xmin=6, xmax=250, ymax=6, gauss=3, plot=True, zoom=1, save=False):
    """
    Remove FIB curtains by FFT filtering

    Args:
       xmin (int): minimum in x direction of filter, removes long waves
       xmax (int): maximum in x direction of filter, x-direction is mirrored, removes short waves
       ymax (int): maximum in y direction of filter
       gauss (float): spread of corners to remove filter artifacts
       plot (bool): plot the original image, filter, processed image
       zoom (float): zoom FFT image by factor: e.g. 4 zoom x and y by 2
       save (bool): only save once set true; allows to test varios settings before saving
    """
    crow, ccol = int(self.heightPixel/2), int(self.widthPixel/2)
    #do forward FFT transformation
    dft = cv2.dft(np.float32(self.image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum=20*np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))
    #create a mask for filtering
    if xmax<xmin: xmax=ccol
    mask = np.ones((self.heightPixel, self.widthPixel,2),np.uint8)
    mask[crow-ymax:crow+ymax, ccol+xmin:ccol+xmax] = 0
    mask[crow-ymax:crow+ymax, ccol-xmax:ccol-xmin] = 0
    mask = ndimage.gaussian_filter(mask*255, gauss)
    mask = ((mask-np.min(mask))*255.0/(np.max(mask)-np.min(mask))).astype(np.uint8)
    # apply mask and inverse DFT
    fshift = dft_shift*mask.astype(np.float32)/255.0
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    img_back /= ( np.max(img_back) / 255.0)
    #plot mask and result
    if plot:
      fftImage = np.zeros((self.heightPixel, self.widthPixel,3),np.uint8)
      fftImage[:,:,2] = magnitude_spectrum*255/np.max(magnitude_spectrum)
      #fftImage[:,:,2][mask[:,:,0]<255] = 0
      fftImage[:,:,0] = (magnitude_spectrum*255/np.max(magnitude_spectrum)) * (mask[:,:,0])
      fftImage[:,:,0][mask[:,:,0]>250] = 0
      zoom = max(zoom, 1)
      xpad =int( self.widthPixel*(1.0-1.0/np.sqrt(zoom))/2 )
      ypad =int(self.heightPixel*(1.0-1.0/np.sqrt(zoom))/2 )
      xend =self.widthPixel-xpad
      yend =self.heightPixel-ypad
      fftImage = fftImage[ypad:yend,xpad:xend,:]
      #print "shape",fftImage.shape,xpad,ypad
      plt.subplot(131)
      plt.imshow(self.image , cmap='gray')
      plt.xticks([])
      plt.yticks([])
      plt.title("Before")
      plt.subplot(132)
      plt.imshow(fftImage)
      plt.xticks([])
      plt.yticks([])
      plt.title("Filter")
      plt.subplot(133)
      plt.imshow(img_back   , cmap='gray')
      plt.xticks([])
      plt.yticks([])
      plt.title("After")
      plt.tight_layout(pad=-0.5, w_pad=-0.5, h_pad=-0.5)
      plt.show()
    #save
    if save:
      self.image = Image.fromarray(img_back).convert("P")
    return


  def removeGrayGradient(self, save=False, plot=True):
    """
    remove gradient that may occur in cross sections

    Args:
       save (bool): only save once set true; allows to test varios settings before saving
       plot (bool): plot graphs during processing
    """
    imArray = np.array(self.image)
    if plot:
      plt.imshow(imArray,cmap="gray")
      plt.colorbar()
      plt.show()
    ysum = np.average(imArray, axis=1)
    x = np.arange(len(ysum))
    maxYsum = np.argmax(ysum)
    myFit = np.polyfit(x[maxYsum:], ysum[maxYsum:],2)
    fitCurve = np.poly1d(myFit)
    if plot:
      plt.plot(x,ysum, '.', x, fitCurve(x), 'r-')
      plt.show()
    imCorr = np.zeros( imArray.shape )
    for i in range(len(ysum)):
      correction = fitCurve(i)-np.average(ysum)
      correction = max(correction, 0)
      imCorr[i,:] = imArray[i,:]-(correction)
    imCorr[imCorr<0] = 0
    imCorr = imCorr.astype(np.uint8)
    if plot:
      plt.imshow(imCorr,cmap="gray")
      plt.colorbar()
      plt.show()
    if save: self.image = Image.fromarray(imCorr).convert("P")
    return



  #@}
  ##
  # @name METHODS TO ROTATE, ... (no modification)
  #@{

  def rotateCCW(self):
    """
    rotate image counter clock-wise
    """
    self.image = self.image.rotate(90)
    self.width = self.width * self.image.size[0]/self.widthPixel
    self.widthPixel  = self.image.size[0]
    self.heightPixel = self.image.size[1]


  def rotateCW(self):
    """
    rotate image clock-wise
    """
    self.image = self.image.rotate(-90)
    self.width = self.width * self.image.size[0]/self.widthPixel
    self.widthPixel  = self.image.size[0]
    self.heightPixel = self.image.size[1]


  def rotate180(self):
    """
    rotate image by 180 degrees
    """
    self.image = self.image.rotate(180)


  def flip(self):
    """
    flip image vertically
    """
    self.image = Image.fromarray(np.array(self.image)[::-1,:]).convert("P")
  #@}
