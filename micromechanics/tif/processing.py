# -*- coding: utf-8 -*-
"""
Image processing methods for SEM TIF images.
"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import exposure


class TifProcessingMixin:
  """
  Image processing methods for :class:`Tif`.
  """

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
    self.image = Image.fromarray(tempArray).convert(self.image.mode)
    widthPixel, heightPixel = self.image.size
    print("   After cropping: new size of image: ",widthPixel, heightPixel)
    self.width = widthPixel*self.pixelSize
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
      lineThreshold = np.where(lineAvg>254)[0]
    elif color=='b':
      lineThreshold = np.where(lineAvg<1)[0]
    else:
      print('**ERROR** only know colors b,w')
      return
    if len(lineThreshold)>0:
      self.crop(yMax=lineThreshold[0])
    return


  def scale(self, scaleFactor=1):
    """
    Scale image by a factor. Scale by factor two decreases the pixelSize and increases the image size by factor two

    Args:
      scaleFactor (float): scaling factor
    """
    self.pixelSize /= scaleFactor
    widthPixel, heightPixel = self.image.size
    self.image = self.image.resize((int(widthPixel*scaleFactor), int(heightPixel*scaleFactor)), Image.NEAREST)
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
        print('**ERROR** something not correct here')
      if method in ['rescale', 'r']:
        pMin, pMax = np.percentile(self.image, (percent, 100-percent))
        self.image = Image.fromarray(exposure.rescale_intensity(np.array(self.image), in_range=(pMin, pMax))).convert('P')
      if method in ['adaptive', 'a']:
        try:
          self.image = Image.fromarray(exposure.equalize_adapthist(np.array(self.image), clip_limit=percent/100.)*255).convert('P')
        except:
          print("**ERROR** Exception hit in Tif.py:426")
    elif self.image.mode == "RGB":
      print('**ERROR** enhancement does not work work for color images')
      print('Do first: i.image = i.image.convert(mode="L")')
      print('Do second: i.image = i.image.convert(mode="P")')
    else:
      print(f"**ERROR** Enhance - image type not supported: {self.image.mode}")
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
    EXPERIMENTAL:
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
    imageArray = np.array(self.image)/255.       #convert to array
    # evaluate mean (scalar) and average (collum/row vector)
    mean = imageArray.mean()                     #get mean of original image
    widthPixel, heightPixel = self.image.size
    if axis=="V":
      average = imageArray.sum(axis=0) / heightPixel  #get average of every collum, this is a vector
    else:
      average = imageArray.sum(axis=1) / widthPixel
    scale = mean / average                       #scaling factor vector
    # do actual change of the pixels
    start = max(start, 0)
    if end<0:
      end = len(scale)                           #use scale here since it automatically adopts to horizontal/vertical
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


  def reset(self):
    """
    Reset it if you want to restart after making unwanted change
    """
    self.image = self.origImage
    return
