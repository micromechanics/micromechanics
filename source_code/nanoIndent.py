# pylint: disable=W0311, C0321, C0209
# @file
# @brief Classes to evaluate indentation data and indenter tip
#
# Indentation data: indentation experiment
# - Methods: iso (can have multiple unloading segments), csm
# - Vendor: Agilent, Hysitron
#
# Indenter tip: shape of indenter tip and gantry stiffness (that what you calibrate)
#
# UNITS: one should use mSB units in this code, since Agilent area function is unit-dependent
# mSB: [mN], [um], [GPa] (force, length, stress)
#
##### Variables: differentiate different length ########
# array of full length: force, time, depth, validMask, ...  [used for plotting]
# array of valid length: E,H,Ac,hc, ... [only has the length where these values are valid]
#    force[validMask] = pMax
#    all these are vectors: OliverPharr et al methods are only vector functions
#
# Coding rules:
# - Change all variables: do not keep original-depth as can be reread and makes code less readable

# TODO:
#    - fitting unloading curve: assume as intial guess m=1.5
import math, io, re, os, json, traceback # pylint: disable=multiple-imports
from enum import Enum
from zipfile import ZipFile
import numpy as np
import pandas as pd
import h5py, lmfit # pylint: disable=multiple-imports
import matplotlib.pyplot as plt
from scipy.optimize import fmin_l_bfgs_b, curve_fit, newton
from scipy import ndimage, interpolate
from scipy.signal import savgol_filter


# enum classes: make code more readable
class Method(Enum):
  """
  Nanoindentation method: e.g. one unloading, multiple,...
  """
  ISO = 1    #one unloading
  MULTI = 2  #multiple ISO unloadings in one loading curve
  CSM = 3    #CSM method: number of unloadings ~ all data-points

class Vendor(Enum):
  """
  HDF5 files are converted
  TXT, XLS files are exported
  """
  Agilent        = 1 #Agilent, KLA, MTS: XLS file format                        # pylint: disable=invalid-name
  Hysitron       = 2 #Hysitron HLD or TXT file format                           # pylint: disable=invalid-name
  Micromaterials = 3 #Micromaterials TXT, ZIP of TXT, HDF5 file format          # pylint: disable=invalid-name
  FischerScope   = 4 #FischerScope TXT file format                              # pylint: disable=invalid-name
  CommonHDF5     = 5 #This hdf5 should work for all indenters                   # pylint: disable=invalid-name

class FileType(Enum):
  """
  Type of file: containing one or multiple tests
  """
  Single = 1  #single test in file                                              # pylint: disable=invalid-name
  Multi  = 2  #multiple tests in file                                           # pylint: disable=invalid-name


class Indentation:
  """
  Main class
  """
  def __init__(self, fileName, nuMat= 0.3, tip=None, verbose=2):
    """
    Initialize indentation experiment data

    Args:
       fileName: fileName to open (.xls, .hld)
       nuMat: material's Poisson ratio.
       tip:  tip class to use; None=perfect
       verbose: the higher, the more information printed: 2=default, 1=minimal, 0=print nothing
    """
    self.nuMat = nuMat                                      #nuMat: material's Posson ratio
    self.nuIndent = 0.07
    self.EIndent  = 1140                                    #GPa from Oliver,Pharr Method paper
    self.beta = 0.75                                        #beta: contact depth coefficient
    self.verbose = verbose
    self.method    = Method.ISO                             #iso default: csm uses different methods
    self.onlyLoadingSegment = False                         #use all data by default

    if tip is None:
      tip = Tip()
    self.tip = tip
    self.iLHU   = [ [-1,-1,-1,-1] ]                         #indicies of Load-Hold-Unload cycles (StartLoad-StartHold-StartUnload-EndLoad)
    self.iDrift = [-1,-1]                                   #start and end indicies of drift segment
    self.metaVendor = {}                                    #some results come from input file
    self.metaUser   = {}                                    #metadata added by analysis
    # define all attributes
    self.testName, self.testList = None, None
    self.h, self.t, self.p, self.valid       = [],[],[],[]
    self.hRaw = []
    self.slope, self.k2p, self.hc, self.Ac = [],[],[],[]
    self.modulus, self.modulusRed, self.hardness = [],[],[]

    #initialize and load first data set
    #set default parameters
    success = False
    if not os.path.exists(fileName) and fileName!='':
      print("*ERROR* __init__: file does not exist",fileName)
      return
    if fileName.endswith(".xls") or fileName.endswith(".xlsx"):
      # KLA, Agilent, Keysight, MTS
      self.vendor = Vendor.Agilent
      self.fileType = FileType.Multi
      self.unloadPMax = 0.999
      self.unloadPMin = 0.5
      success = self.loadAgilent(fileName)
    if (fileName.endswith(".hld") or fileName.endswith(".txt")) and not success:
      # Hysitron
      self.vendor = Vendor.Hysitron
      self.fileType = FileType.Single
      self.unloadPMax = 0.95
      self.unloadPMin = 0.4
      success = self.loadHysitron(fileName)
    if (fileName.endswith(".txt") or
        fileName.endswith(".zip")) and not success:
      # Micromaterials
      self.vendor = Vendor.Micromaterials
      self.unloadPMax = 0.99
      self.unloadPMin = 0.5
      if fileName.endswith(".txt"):
        self.fileType = FileType.Single
      else:
        self.fileType = FileType.Multi
      success = self.loadMicromaterials(fileName)
    if fileName.endswith(".txt") and not success:
      # Fischer Scope
      self.vendor = Vendor.FischerScope
      self.fileType = FileType.Multi
      self.unloadPMax = 0.95
      self.unloadPMin = 0.21
      success = self.loadFischerScope(fileName)
    if fileName.endswith(".hdf5") and not success:
      # Common hdf5 file
      self.vendor = Vendor.CommonHDF5
      self.fileType = FileType.Multi
      self.unloadPMax = 0.99
      self.unloadPMin = 0.5
      success = self.loadHDF5(fileName)
    return

  ##
  # @name CONVENTIONAL NANOINDENTATION FUNCTIONS: area, E,.
  # only area prefactors and stiffness are class variables
  #@{
  def YoungsModulus(self, modulusRed, nuThis=-1):
    """
    Calculate the Youngs modulus from the reduced Youngs modulus

    Args:
       modulusRed (float): reduced Youngs modulus [GPa]

       nuThis (float): use a non-standard Poission's ratio

    Returns:
        float: Young's modulus
    """
    nu = self.nuMat
    if nuThis>0:
      nu = nuThis
    modulus = (1.0-nu*nu) / ( 1.0/modulusRed - (1.0-self.nuIndent*self.nuIndent)/self.EIndent )
    return modulus


  def ReducedModulus(self, modulus, nuThis=-1):
    """
    Calculate the reduced modulus from the Youngs modulus

    Args:
       modulus (float): Youngs modulus [GPa]

       nuThis (float): use a non-standard Young's modulus

    Returns:
        float: Reduced Young's modulus
    """
    nu = self.nuMat
    if nuThis>0:
      nu = nuThis
    modulusRed =  1.0/(  (1.0-nu*nu)/modulus + (1.0-self.nuIndent*self.nuIndent)/self.EIndent )
    return modulusRed


  def OliverPharrMethod(self, stiffness, pMax, h):
    """
    Conventional Oliver-Pharr indentation method to calculate reduced Modulus modulusRed

    The following equations are used in that order:

      hc = h-beta pMax/stiffness

      Ac = hc(prefactors)

      stiffness = 2/sqrt(pi) sqrt(Ac) modulusRed

      Ac the contact area, hc the contact depth

    Args:
       stiffness (float): stiffness = slope dP/dh

       pMax (float): maximal force

       h (float): total penetration depth

    Returns:
       list: modulusRed, Ac, hc
    """
    threshAc = 1.e-12  #units in um: threshold = 1pm^2
    hc = h - self.beta*pMax/stiffness
    Ac   = self.tip.areaFunction(hc)
    Ac[Ac< threshAc] = threshAc  # prevent zero or negative area that might lock sqrt
    modulus   = stiffness / (2.0*np.sqrt(Ac)/np.sqrt(np.pi))
    return [modulus, Ac, hc]

  def inverseOliverPharrMethod(self, stiffness, pMax, modulusRed):
    """
    Inverse Oliver-Pharr indentation method to calculate contact area Ac

    - equations and variable definitions given above; order in reverse order
    - only used for verification of the Oliver-Pharr Method

    Args:
       stiffness (float): slope dP/dh

       pMax (float): maximal force

       modulusRed (float): modulusRed

    Returns:
       float: h penetration depth
    """
    Ac = math.pow( stiffness / (2.0*modulusRed/math.sqrt(math.pi))  ,2)
    hc0 = math.sqrt(Ac / 24.494)           # first guess: perfect Berkovich
    hc = self.tip.areaFunctionInverse(Ac, hc0=hc0)
    h = hc + self.beta*pMax/stiffness
    return h.flatten()


  @staticmethod
  def UnloadingPowerFunc(h,B,hf,m):
    """
    internal function describing the unloading regime
    - function: p = B*(h-hf)^m
    - B:  scaling factor (no physical meaning)
    - m:  exponent       (no physical meaning)
    - hf: final depth = depth where force becomes 0
    """
    value = B*np.power(h-hf,m)
    return value


  def stiffnessFromUnloading(self, p, h, plot=False):
    """
    Calculate single unloading stiffness from Unloading
    see G200 manual, p7-6

    Args:
       p (np.array): vector of forces

       h (np.array): vector of depth

       plot (bool): plot results

    Returns:
       list: stiffness, validMask [values of P,h where stiffness is determined], mask, optimalVariables, powerlawFit-success
    """
    if self.method== Method.CSM:
      print("*ERROR* Should not land here: CSM method")
      return None,None,None,None
    if self.verbose>2:
      print("Number of unloading segments:"+str(len(self.iLHU))+"  Method:"+str(self.method))
    stiffness, mask, opt, powerlawFit = [], None, None, []
    validMask = np.zeros_like(p, dtype=bool)
    if plot:
      plt.plot(h,p,'-k')
    for cycleNum, cycle in enumerate(self.iLHU):
      loadStart, loadEnd, unloadStart, unloadEnd = cycle
      if loadStart>loadEnd or loadEnd>unloadStart or unloadStart>unloadEnd:
        print('*ERROR* stiffnessFromUnloading: indicies not in order:',cycle)
      maskSegment = np.zeros_like(h, dtype=bool)
      maskSegment[unloadStart:unloadEnd+1] = True
      maskForce   = np.logical_and(p<p[loadEnd]*self.unloadPMax, p>p[loadEnd]*self.unloadPMin)
      mask        = np.logical_and(maskSegment,maskForce)
      if len(mask[mask])==0:
        print('*ERROR* mask of unloading is empty. Cannot fit\n')
        return None, None, None, None, None
      if plot:
        plt.plot(h[mask],p[mask],'ob')
      #initial values of fitting
      hf0    = h[mask][-1]/2.0
      m0     = 2
      B0     = max(abs(p[0] / np.power(h[0]-hf0,m0)), 0.001)  #prevent neg. or zero
      bounds = [[0,0,0.8],[np.inf, max(np.min(h[mask]),hf0), 10]]
      if self.verbose>2:
        print("Initial fitting values", hf0, m0, B0)
        print("Bounds", bounds)
      # Old linear assumptions
      # B0  = (P[mask][-1]-P[mask][0])/(h[mask][-1]-h[mask][0])
      # hf0 = h[mask][0] - P[mask][0]/B0
      # m0  = 1.5 #to get of axis
      try:
        opt, _ = curve_fit(self.UnloadingPowerFunc, h[mask],p[mask],
                            p0=[B0,hf0,m0], bounds=bounds,
                            ftol=1e-4, maxfev=3000 )#set ftol to 1e-4 if accept more and fail less
        if self.verbose>2:
          print("Optimal values", opt)
        B,hf,m = opt
        if np.isnan(B):
          raise ValueError("NAN after fitting")
        powerlawFit.append(True)
      except:
        #if fitting fails: often the initial bounds and initial values do not match
        print(traceback.format_exc())
        if self.verbose>0:
          print("stiffnessFrommasking: #",cycleNum," Fitting failed. use linear")
        B  = (p[mask][-1]-p[mask][0])/(h[mask][-1]-h[mask][0])
        hf = h[mask][0] -p[mask][0]/B
        m  = 1.
        opt= (B,hf,m)
        powerlawFit.append(False)
      stiffness_ = B*m*math.pow( (h[unloadStart]-hf), m-1)
      stiffness.append(stiffness_)
      validMask[unloadStart]=True
      if plot:
        plt.plot(h[mask],   self.UnloadingPowerFunc(h[mask],B,hf,m),'m-')
        stiffnessN= p[unloadStart]-stiffness_*h[unloadStart]
        plt.plot(h[mask],   stiffness_*h[mask]+stiffnessN, 'r--', lw=3)
    if plot:
      plt.xlim(left=0)
      plt.ylim(bottom=0)
      plt.title('magenta: power function, red: linear slope')
      plt.xlabel(r'depth [$\mathrm{\mu m}$]')
      plt.ylabel(r'force [$\mathrm{mN}$]')
      plt.show()
    return stiffness, validMask, mask, opt, powerlawFit


  def popIn(self, correctH=True, plot=True, removeInitialNM=2.):
    """
    Search for pop-in by jump in depth rate

    Certainty:
    - deltaSlope: higher is better (difference in elastic - plastic slope). Great indicator
    - prefactor: higher is better (prefactor of elastic curve). Great indicator
    - secondRate: lower is better (height of second largest jump). Nice indicator 0.25*deltaRate
    - covElast: lower is better. bad indicator
    - deltaH: higher is better (delta depth in jump). bad indicator
    - deltaRate: higher is better (depth rate during jump). bad indicator

    Future: iterate over largest, to identify best

    Args:
       correctH: correct depth such that curves aligned
       plot: plot pop-in curve
       removeInitialNM: remove initial nm from data as they have large scatter

    Returns:
       pop-in force, dictionary of certainty
    """
    maxPlasticFit = 150
    minElasticFit = 0.01

    mask = (self.h[self.valid]-np.min(self.h[self.valid]))  >removeInitialNM/1.e3
    h = self.h[self.valid][mask]
    p = self.p[self.valid][mask]

    depthRate = (h[1:]-h[:-1])
    x_        = np.arange(len(depthRate))
    fits      = np.polyfit(x_,depthRate,2)  #substract 2nd order fit b/c depthRate increases over time
    depthRate-= np.polyval(fits,x_)
    iJump     = np.argmax(depthRate)
    iMax      = min(np.argmax(p), iJump+maxPlasticFit)      #max for fit: 150 data-points or max. of curve
    iMin      = np.min(np.where(p>minElasticFit))
    fitPlast  = np.polyfit(h[iJump+1:iMax],p[iJump+1:iMax],2) #does not have to be parabola, just close fit
    slopePlast= np.polyder(np.poly1d(fitPlast))(h[iJump+1] )
    def funct(depth, prefactor, h0):
      diff           = depth-h0
      if type(diff)==np.float64:
        diff = max(diff,0.0)
      else:
        diff[diff<0.0] = 0.0
      return prefactor* (diff)**(3./2.)
    fitElast, pcov = curve_fit(funct, h[iMin:iJump], p[iMin:iJump], p0=[100.,0.])   # pylint warning: Possible unbalanced tuple unpacking with sequence defined at line 837 of scipy.optimize.minpack: left side has 2 label(s), right side has 5 value(s) (389:4) [unbalanced-tuple-unpacking]
    slopeElast= (funct(h[iJump],*fitElast) - funct(h[iJump]*0.9,*fitElast)) / (h[iJump]*0.1)
    fPopIn    = p[iJump]
    certainty = {"deltaRate":depthRate[iJump], "prefactor":fitElast[0], "h0":fitElast[1], \
                 "deltaSlope": slopeElast-slopePlast, 'deltaH':h[iJump+1]-h[iJump],\
                 "covElast":pcov[0,0] }
    listDepthRate = depthRate.tolist()
    iJump2 = np.argmax(listDepthRate)
    while (iJump2-iJump)<3:
      del listDepthRate[iJump2]
      iJump2 = np.argmax(listDepthRate)
    certainty["secondRate"] = np.max(listDepthRate)
    if plot:
      _, ax1 = plt.subplots()
      ax2 = ax1.twinx()
      ax1.plot(self.h,self.p)
      h_ = np.linspace(self.h[iJump+1],self.h[iMax])
      ax1.plot(h_, np.polyval(fitPlast,h_))
      ax1.plot(self.h[iMin:iJump], funct(self.h[iMin:iJump],*fitElast))
      ax2.plot(h[:-1],depthRate,'r')
      ax1.axvline(h[iJump], color='k', linestyle='dashed')
      ax1.axhline(fPopIn, color='k', linestyle='dashed')
      ax1.set_xlim(right=4.*self.h[iJump])
      ax1.set_ylim(top=4.*self.p[iJump], bottom=0)
      plt.show()
    if correctH:
      self.h -= certainty["h0"]
    return fPopIn, certainty


  #@}
  ##
  # @name Calculate YoungsModulus, Hardess and deterimine area function
  # Access to class variables
  #@{
  def calcYoungsModulus(self, minDepth=-1, plot=False):
    """
    Calculate and plot Young's modulus as a function of the depth
    -  use corrected h and stiffness (do not recalculate)

    Args:
       minDepth: minimum depth for fitting horizontal; if negative: no line is fitted
       plot: plot comparison this calculation to data read from file

    Returns:
       average Young's modulus, minDepth>0
    """
    self.modulusRed, self.Ac, self.hc = self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid])
    modulus = self.YoungsModulus(self.modulusRed)
    if minDepth>0:
      #eAve = np.average(       self.modulusRed[ self.h>minDepth ] )
      eAve = np.average( modulus[  np.bitwise_and(modulus>0, self.h[self.valid]>minDepth) ] )
      eStd = np.std(     modulus[  np.bitwise_and(modulus>0, self.h[self.valid]>minDepth) ] )
      print("Average and StandardDeviation of Young's Modulus",round(eAve,1) ,round(eStd,1) ,' [GPa]')
    else:
      eAve, eStd = -1, 0
    if plot:
      h = self.h[self.valid]
      mark = '-' if len(modulus)>1 else 'o'
      if not self.modulus is None:
        plt.plot(h[h>minDepth], self.modulus[h>minDepth], mark+'r', lw=3, label='read')
      plt.plot(  h[h>minDepth], modulus[h>minDepth], mark+'b', label='calc')
      if minDepth>0:
        plt.axhline(eAve, color='k')
        plt.axhline(eAve+eStd, color='k', linestyle='dashed')
        plt.axhline(eAve-eStd, color='k', linestyle='dashed')
        plt.ylim([eAve-4*eStd,eAve+4*eStd])
      plt.xlabel(r'depth [$\mathrm{\mu m}$]')
      plt.ylim(ymin=0)
      plt.ylabel(r'Youngs modulus [GPa]')
      plt.legend(loc=0)
      plt.show()
    self.modulus = modulus
    return eAve


  def calcHardness(self, minDepth=-1, plot=False):
    """
    Calculate and plot Hardness as a function of the depth

    Args:
       minDepth: minimum depth for fitting horizontal; if negative: no line is fitted
       plot: plot comparison this calculation to data read from file
    """
    hardness = self.p[self.valid] / self.OliverPharrMethod(self.slope, self.p[self.valid] , self.h[self.valid])[1] #use area function
    if plot:
      mark = '-' if len(hardness)>1 else 'o'
      plt.plot(self.h[self.valid], hardness, mark+'b', label='calc')
      if not self.hardness is None:
        plt.plot(self.h[self.valid], self.hardness, mark+'r', label='readFromFile')
      if minDepth>0:
        hardnessAve = np.average( hardness[  np.bitwise_and(hardness>0, self.h[self.valid]>minDepth) ] )
        hardnessStd = np.std(     hardness[  np.bitwise_and(hardness>0, self.h[self.valid]>minDepth) ] )
        print("Average and StandardDeviation of hardness",round(hardnessAve,1) ,round(hardnessStd,1) ,' [GPa]')
        plt.axhline(hardnessAve, color='b')
        plt.axhline(hardnessAve+hardnessStd, color='b', linestyle='dashed')
        plt.axhline(hardnessAve-hardnessStd, color='b', linestyle='dashed')
      plt.xlabel(r'depth [$\mathrm{\mu m}]$]')
      plt.ylabel(r'hardness [$\mathrm{GPa}$]')
      plt.legend(loc=0)
      plt.show()
    self.hardness = hardness
    return           # pylint error: useless return


  def calcStiffness2Force(self, minDepth=0.01, plot=True, calibrate=False):
    """
    Calculate and plot stiffness squared over force as a function of the depth

    Args:
       minDepth: minimum depth for fitting line

       plot: plot curve and slope

       calibrate: calibrate additional stiffness and save value
    """
    compliance0 = self.tip.compliance
    prefactors = None
    def errorFunction(compliance):
      stiffness   = 1./(1./self.sRaw-compliance)            # pylint error: sRaw isn't defined
      stiffness2load = np.divide(np.multiply(stiffness,stiffness),self.p)
      h   = self.hRaw-compliance*self.p
      h_ = h[ h>minDepth ]
      stiffness2load  = stiffness2load[ h>minDepth ]
      if len(h_)>4:
        prefactors = np.polyfit(h_,stiffness2load,1)
        print(compliance,"Fit f(x)=",prefactors[0],"*x+",prefactors[1])
        return np.abs(prefactors[0])
      else:     # pylint warning: unnecessary "else" after "return"
        print("*WARNING*: too short vector",len(h_))
        return 9999999.
    if calibrate:
      result = fmin_l_bfgs_b(errorFunction, compliance0, bounds=[(-0.1,0.1)], approx_grad=True, epsilon=0.000001, factr=1e11)
      print("  Best values   ",result[0], "\tOptimum residual:",np.round(result[1],3))
      print('  Number of function evaluations~size of globalData',result[2]['funcalls'])
      self.compliance = result[0]
      compliance0 = self.compliance       #pylint warning:  Attribute 'compliance' defined outside __init__ (524:6) [attribute-defined-outside-init]
      #self.correct_H_S()
    if plot:
      stiffness = 1./(1./self.sRaw-self.compliance)             #vy: AttributeError: 'Indentation' object has no attribute 'sRaw'
      stiffness2load = np.divide(np.multiply(stiffness,stiffness),self.p)
      h   = self.hRaw-compliance0*self.p
      h_ = h[ h>minDepth ]
      stiffness2load_  = stiffness2load[ h>minDepth ]
      prefactors = np.polyfit(h_,stiffness2load_,1)
      plt.plot(h,stiffness2load, 'b-')
      stiffness2loadFit = np.polyval(prefactors,h)
      plt.plot(h, stiffness2loadFit, 'r-', lw=3)
      plt.xlabel(r'depth [$\mathrm{\mu m}$]')
      plt.ylabel(r'stiffness2/load [$\mathrm{GPa}$]')
      plt.show()
    return prefactors


  def tareDepthForce(self, slopeThreshold=100, compareRead=False, plot=False):
    """
    Calculate surface contact (by slope being larger than threshold)
    and offset depth,force,time by the surface

    Future improvements:

    - surface identification in future
    - handle more cases

    Args:
       slopeThreshold: threshold slope in P-h curve for contact: 200,300

       compareRead: compare new results to the ones from the file

       plot: plot comparison new data and data from file
    """
    if self.vendor!=Vendor.Agilent or self.method==Method.CSM:
      print("tareDepthForce only valid for ISO method of Agilent at this moment")
      return
    iSurface = np.min(np.where(self.pVsHSlope>slopeThreshold))#determine point of contact
    h = self.hRaw   - self.hRaw[iSurface]                   #tare to point of contact
    p = self.pRaw   - self.pRaw[iSurface]
    t = self.tTotal - self.tTotal[iSurface]                 #pylint error: "pVsHSlope", "pRaw", "tTotal", "frameStiffness" are not defined
    h-= p/self.frameStiffness                               #compensate depth for instrument deflection
    maskDrift = np.zeros_like(h, dtype=bool)
    maskDrift[self.iDrift[0]:self.iDrift[1]]   =  True
    tMiddle = (t[self.iDrift[1]]+t[self.iDrift[0]])/2
    maskDrift = np.logical_and(maskDrift, t>=tMiddle)
    iDriftS, iDriftE = np.where(maskDrift)[0][0],np.where(maskDrift)[0][-1]
    driftRate        = (h[iDriftE]-h[iDriftS])/(t[iDriftE]-t[iDriftS])  #calc. as rate between last and first point
                                #according to plot shown in J.Hay Univerisity part 3; fitting line would be different
    print("Drift rate: %.3f nm/s"%(driftRate*1e3))
    h-= driftRate*t                                          #compensate thermal drift
    p-= self.slopeSupport*(self.hRaw-self.hRaw[iSurface])    #compensate supporting mechanism (use original data since h changed)   #pylint error: "slopeSupport" is not defined
    if compareRead:
      mask = self.h>0.010                                    #10nm
      error = (h[mask]-self.h[mask])/self.h[mask]
      print("Error in h: {0:.2f}%".format(np.linalg.norm(error)/len(error)*100.) )
      error = (p[mask]-self.p[mask])/self.p[mask]
      print("Error in p: {0:.2f}%".format(np.linalg.norm(error)/len(error)*100.) )
      error = (t[mask]-self.t[mask])/self.t[mask]
      print("Error in t: {0:.2f}%".format(np.linalg.norm(error)/len(error)*100.) )
    if plot:
      fig, ax1 = plt.subplots()    # pylint warning: fig is unused variable
      ax2 = ax1.twinx()
      ax1.plot(t,p, label='new')
      ax1.plot(self.t,self.p, label='read')
      ax1.axhline(0, linestyle='dashed', c='k')
      ax1.axvline(0, linestyle='dashed', c='k')
      ax1.legend(loc=2)
      ax2.plot(self.t, self.pVsHSlope, "C2--", label='pVsHSlope')
      ax1.set_xlabel(r"depth [$\mathrm{\mu m}$]")
      ax1.set_ylabel(r"force [$\mathrm{mN}$]")
      ax2.set_ylabel(r"depth [$\mathrm{mN/\mu m}$]", color='C2')
      plt.show()
    #set newly obtained data
    self.h, self.p, self.t = h, p, t
    return


  def analyse(self):
    """
    update slopes/stiffness, Young's modulus and hardness after displacement correction by:

    - compliance change

    ONLY DO ONCE AFTER LOADING FILE: if this causes issues introduce flag analysed which is toggled during loading and analysing
    """
    self.h -= self.tip.compliance*self.p
    if self.method == Method.CSM:
      self.slope = 1./(1./self.slope-self.tip.compliance)
    else:
      self.slope, self.valid, _, _ , _= self.stiffnessFromUnloading(self.p, self.h)  # pylint warning: Possible unbalanced tuple unpacking with sequence defined at line 279: left side has 5 label(s), right side has 4 value(s) (615:6) [unbalanced-tuple-unpacking]
      self.slope = np.array(self.slope)
    self.k2p = self.slope*self.slope/self.p[self.valid]
    #Calculate Young's modulus
    self.calcYoungsModulus()
    self.calcHardness()
    self.saveToUserMeta()
    return          # pylint warning: useless return


  def analyseDrift(self, plot=True, fraction=None, timeStart=None):
    """
    Analyse drift segment by:

    - Hysitron before the test
    - Micromaterials after the test

    Args:
       plot: plot drift data

       fraction: fraction of data used for fitting (Micromaterials uses last 0.6)
       timeStart: initial timestamp used for drift analysis; e.g. after 20sec;
                  this superseeds fraction

    Results:
       drift in um/s
    """
    drift = None
    if self.vendor == Vendor.Hysitron and self.fileName.endswith('.hld'):
      t = self.dataDrift[:,0]
      h = self.dataDrift[:,1]
      rate = np.zeros_like(t)
      rate[:] = np.nan
      for idxEnd,ti in enumerate(t):
        if ti<20: continue
        idxStart = np.argmin(np.abs( t[:]-(ti-20.) )  )
        rate[idxEnd] = (h[idxEnd]-h[idxStart])/(t[idxEnd]-t[idxStart])
      idxEnd = np.argmin(np.abs( t[:]-(40.) )  )
      drift = rate[idxEnd]
      print("Drift:", round(drift*1.e3,3),"nm/s")
      self.metaUser['drift'] = drift
      if plot:
        _, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(t,rate*1.e3,'r')
        ax1.axhline(0.05,c='r',linestyle='dashed')
        ax2.plot(t,h*1.e3,'b')
        ax1.set_xlabel(r'time [$\mathrm{s}$]')
        ax1.set_ylabel(r'drift rate [$\mathrm{nm/s}$]', color='r')
        ax2.set_ylabel(r'depth [$\mathrm{nm}$]', color='b')
        plt.show()
    elif self.vendor == Vendor.Micromaterials and self.fileName.endswith('hdf5'):
      branch = self.datafile[self.testName]['drift']
      time = np.array(branch['time'])
      depth = np.array(branch['depth'])
      if fraction is None:
        fraction = 0.6
      if timeStart is None:
        timeStart = (1-fraction)*time[-1]+fraction*time[0]
      inc = np.argmin(np.abs(time-timeStart))-1
      drift = np.polyfit(time[inc:],depth[inc:],1)[0]/1000.
    return drift


  def identifyLoadHoldUnload(self,plot=False):
    """
    internal method: identify ALL load - hold - unload segments in data

    Args:
       plot: verify by plotting
    """
    #self.plotTestingMethod() # for debugging
    if self.method==Method.CSM:
      self.identifyLoadHoldUnloadCSM()
      return
    maxIdx   = np.argmax(self.p)       # pylint warning: maxIdx is unused variable
    maxValue = np.max(self.p)
    maxZone  = self.p > 0.98*maxValue
    rate = self.p[maxZone][1:]-self.p[maxZone][:-1]
    #using histogram, define masks for loading and unloading
    hist, bins= np.histogram(rate , bins=200) #TODO this 200 and zeroDelta below need must dependent on vendor
    # ... can user change them, commonHDF blocks automatic identification
    # .... or better algorithm
    binCenter = (bins[1:]+bins[:-1])/2

    peaks = np.where(hist>5)[0]                  #peaks with more than 10 items
    if len(peaks)==0:
      peaks = [np.argmax(hist)]                   #take largest
    try:
      zeroID = np.argmin(np.abs(binCenter[peaks]))  #id which is closest to zero
      zeroValue = binCenter[peaks][zeroID]
    except:     # pylingt warning: No exception type(s) specified (705:4) [bare-except]
      self.iLHU = []
      return False
    ## Better algorithm: look for closest zero historgram-peak to zeroValue; take that to calculate delta
    try:
      zeroPeaks = np.logical_and(hist<0.3, binCenter<zeroValue)
      zeroPeaks = np.where(zeroPeaks)[0]
      firstZero = np.argmin(np.abs(zeroValue-binCenter[zeroPeaks]))
      zeroDelta = abs(binCenter[zeroPeaks][firstZero]-zeroValue)
      if self.vendor==Vendor.Hysitron and self.method==Method.ISO:
        zeroDelta *= 4  #data is noisy, more safety to prevent wrong identification
      rate      = self.p[1:]-self.p[:-1]
      loadMask  = rate>(zeroValue+zeroDelta)
      unloadMask= rate<(zeroValue-zeroDelta)
    except:
      self.identifyLoadHoldUnloadCSM()     #simpler method, less error-prone
      return
    if plot:     # verify visually
      plt.plot(binCenter,hist,'o')#, width=0.001)
      plt.axvline(zeroValue, c='k')
      plt.axvline(binCenter[zeroPeaks][firstZero], c='r')
      plt.axvline(zeroValue+zeroDelta, c='k', linestyle='dashed')
      plt.axvline(zeroValue-zeroDelta, c='k', linestyle='dashed')
      plt.ylabel('count []')
      plt.xlabel(r'rate [$\mathrm{mN/s}$]')
      plt.show()
      plt.plot(rate)
      plt.axhline(zeroValue, c='k')
      plt.axhline(zeroValue+zeroDelta, c='k', linestyle='dashed')
      plt.axhline(zeroValue-zeroDelta, c='k', linestyle='dashed')
      plt.xlabel('time incr. []')
      plt.ylabel(r'rate [$\mathrm{mN/sec}$]')
      plt.show()
    #clean small fluctuations
    if len(loadMask)>100 and len(unloadMask)>100:
      size = 7
      loadMask = ndimage.binary_closing(loadMask, structure=np.ones((size,)) )
      unloadMask = ndimage.binary_closing(unloadMask, structure=np.ones((size,)))
      loadMask = ndimage.binary_opening(loadMask, structure=np.ones((size,)))
      unloadMask = ndimage.binary_opening(unloadMask, structure=np.ones((size,)))
    #find index where masks are changing from true-false
    loadMask  = np.r_[False,loadMask,False] #pad with false on both sides
    unloadMask= np.r_[False,unloadMask,False]
    loadIdx   = np.flatnonzero(loadMask[1:]   != loadMask[:-1])
    unloadIdx = np.flatnonzero(unloadMask[1:] != unloadMask[:-1])
    if plot:     # verify visually
      plt.plot(self.p,'o')
      plt.plot(loadIdx[::2],  self.p[loadIdx[::2]],  'o',label='load',markersize=12)
      plt.plot(loadIdx[1::2], self.p[loadIdx[1::2]], 'o',label='hold',markersize=10)
      plt.plot(unloadIdx[::2],self.p[unloadIdx[::2]],'o',label='unload',markersize=8)
      plt.plot(unloadIdx[1::2],self.p[unloadIdx[1::2]],'o',label='unload-end',markersize=6)
      plt.legend(loc=0)
      plt.title("BEFORE Cleaning")
      plt.xlabel('time incr. []')
      plt.ylabel(r'force [$\mathrm{mN}$]')
      plt.show()
    while len(loadIdx)<len(unloadIdx) and unloadIdx[0]<loadIdx[0]:
      print("*WARNING* identifyLoadHoldUnload: cut two from front of unloadIdx: UNDESIRED")
      unloadIdx = unloadIdx[2:]
    while len(loadIdx)<len(unloadIdx) and unloadIdx[-3]>loadIdx[-1]:
      print("*WARNING* identifyLoadHoldUnload: cut two from end of unloadIdx: UNDESIRED")
      unloadIdx = unloadIdx[:-2]
    while len(loadIdx)>len(unloadIdx) and loadIdx[3]<unloadIdx[1]:
      print("*WARNING* identifyLoadHoldUnload: cut two from front of loadIdx: UNDESIRED")
      loadIdx = loadIdx[2:]
    self.iLHU = []
    for i,_ in enumerate(loadIdx[::2]):
      self.iLHU.append([loadIdx[::2][i],loadIdx[1::2][i],unloadIdx[::2][i],unloadIdx[1::2][i]])
      if loadIdx[::2][i]>loadIdx[1::2][i] or loadIdx[1::2][i]>unloadIdx[::2][i] or \
         unloadIdx[::2][i]>unloadIdx[1::2][i]:
        print("*ERROR* Wrong order in idx",i, \
          [loadIdx[::2][i],loadIdx[1::2][i],unloadIdx[::2][i],unloadIdx[1::2][i]])
        #plot = True #TODO change later
    if len(self.iLHU)>1:
      self.method=Method.MULTI
    if plot:     # verify visually
      plt.plot(self.p)
      plt.plot(loadIdx[::2],  self.p[loadIdx[::2]],  'o',label='load',markersize=12)
      plt.plot(loadIdx[1::2], self.p[loadIdx[1::2]], 'o',label='hold',markersize=10)
      plt.plot(unloadIdx[::2],self.p[unloadIdx[::2]],'o',label='unload',markersize=8)
      plt.plot(unloadIdx[1::2],self.p[unloadIdx[1::2]],'o',label='unload-end',markersize=6)
      plt.legend(loc=0)
      plt.title("AFTER Cleaning")
      plt.xlabel('time incr. []')
      plt.ylabel(r'force [$\mathrm{mN}$]')
      plt.show()
    #drift segments
    iDriftS = unloadIdx[1::2][i]+1    # pylint warning: Using possibly undefined loop variable 'i' (785:30) [undefined-loop-variable]
    iDriftE = len(self.p)-1
    if iDriftS+1>iDriftE:
      iDriftS=iDriftE-1
    self.iDrift = [iDriftS,iDriftE]
    return True     # pylint warning: Either all return statements in a function should return an expression, or none of them should. (680:2) [inconsistent-return-statements]


  def identifyLoadHoldUnloadCSM(self):
    """
    internal method: identify load - hold - unload segment in CSM data

    Backup: if identifyLoadHoldUnload fails
    """
    iSurface = np.min(np.where( self.h>=0                     ))
    iLoad    = np.min(np.where( self.p-np.max(self.p)*0.999>0 ))
    if iLoad<len(self.p)-1:
      iHold    = np.max(np.where( self.p-np.max(self.p)*0.999>0 ))
      if iHold==iLoad:
        iHold += 1
      hist,bins= np.histogram( self.p[iHold:] , bins=1000)
      pDrift   = bins[np.argmax(hist)+1]
      pCloseToDrift = np.logical_and(self.p>pDrift*0.999,self.p<pDrift/0.999)
      pCloseToDrift[:iHold] = False
      if len(pCloseToDrift[pCloseToDrift])>3:
        iDriftS  = np.min(np.where( pCloseToDrift ))
        iDriftE  = np.max(np.where( pCloseToDrift ))
      else:
        iDriftS   = len(self.p)-2
        iDriftE   = len(self.p)-1
      if not (iSurface<iLoad and iLoad<iHold and iHold<iDriftS and iDriftS<iDriftE and iDriftE<len(self.h)):    #pylint warning: Simplify chained comparison between the operands (815:14) [chained-comparison]
        print("*ERROR* identifyLoadHoldUnloadCSM in identify load-hold-unloading cycles")
        print(iSurface,iLoad,iHold,iDriftS,iDriftE, len(self.h))
    else:  #This part is required
      if self.method != Method.CSM:
        print("*WARNING*: no hold or unloading segments in data")
      iHold     = len(self.p)-3
      iDriftS   = len(self.p)-2
      iDriftE   = len(self.p)-1
    self.iLHU   = [[iSurface,iLoad,iHold,iDriftS]]
    self.iDrift = [iDriftS,iDriftE]
    return        # pylint warning: useless return



  #@}
  ##
  # @name FILE HANDLING; PLOTTING
  # Access to class variables
  #@{
  def nextTest(self):
    """
    Wrapper for all next test for all vendors
    """
    if self.vendor == Vendor.Agilent:
      success = self.nextAgilentTest()
    elif self.vendor == Vendor.Micromaterials:
      success = self.nextMicromaterialsTest()
    elif self.vendor == Vendor.FischerScope:
      success = self.nextFischerScopeTest()   #pylint error: Assigning result of a function call, where the function returns None (844:6) [assignment-from-none]
    elif self.vendor == Vendor.CommonHDF5:
      success = self.nextHDF5Test()
    else:
      print("No multiple tests in file")
      success = False
    return success

  def restartFile(self):
    self.testList = list(self.allTestList)
    self.nextTest()
    return    #pylint warning: useless return


  def loadAgilent(self, fileName):
    """
    Initialize G200 excel file for processing

    Args:
       fileName: file name
    """
    self.testList = []
    self.fileName = fileName    #one file can have multiple tests
    self.indicies = {}
    wb = pd.read_excel(fileName,sheet_name='Required Inputs')
    self.metaVendor.update( dict(wb.iloc[-1]) )
    if self.metaVendor['Poissons Ratio']!=self.nuMat:
      print("*WARNING*: your Poisson Ratio is different than in file.",self.nuMat,self.metaVendor['Poissons Ratio'])
    ## TODO check if CSM can be deduced form other sheets
    self.datafile = pd.read_excel(fileName, sheet_name=None)
    tagged = []
    code = {"Load On Sample":"p", "Force On Surface":"p", "LOAD":"p"\
          ,"_Load":"pRaw", "Raw Load":"pRaw","Force":"pRaw"\
          ,"Displacement Into Surface":"h", "DEPTH":"h"\
          ,"_Displacement":"hRaw", "Raw Displacement":"hRaw","Displacement":"hRaw"\
          ,"Time On Sample":"t", "Time in Contact":"t", "TIME":"t", "Time":"tTotal"\
          ,"Contact Area":"Ac", "Contact Depth":"hc"\
          ,"Harmonic Displacement":"hHarmonic", "Harmonic Load":"pHarmonic","Phase Angle":"phaseAngle"\
          ,"Load vs Disp Slope":"pVsHSlope","d(Force)/d(Disp)":"pVsHSlope", "_Column": "Column", "_Frame": "Frame"\
          ,"Support Spring Stiffness":"slopeSupport", "Frame Stiffness": "frameStiffness"\
          ,"Harmonic Stiffness":"slopeInvalid"\
          ,"Harmonic Contact Stiffness":"slope", "STIFFNESS":"slope","Stiffness":"slope" \
          ,"Stiffness Squared Over Load":"k2p","Dyn. Stiff.^2/Load":"k2p"\
          ,"Hardness":"hardness", "H_IT Channel":"hardness","HARDNESS":"hardness"\
          ,"Modulus": "modulus", "E_IT Channel": "modulus","MODULUS":"modulus","Reduced Modulus":"modulusRed"\
          ,"Scratch Distance": "s", "XNanoPosition": "x", "YNanoPosition": "y"\
          ,"X Position": "xCoarse", "Y Position": "yCoarse","X Axis Position":"xCoarse","Y Axis Position":"yCoarse"\
          ,"TotalLateralForce": "L", "X Force": "pX", "_XForce": "pX", "Y Force": "pY", "_YForce": "pY"\
          ,"_XDeflection": "Ux", "_YDeflection": "Uy" }
    self.fullData = ['h','p','t','pVsHSlope','hRaw','pRaw','tTotal','slopeSupport']
    if self.verbose>1: print("=============  "+fileName+"  ============")
    for dfName in self.datafile.keys():
      df    = self.datafile.get(dfName)
      if "Test " in dfName and not "Tagged" in dfName and not "Test Inputs" in dfName:
        self.testList.append(dfName)
        #print "  I should process sheet |",sheet.name,"|"
        if len(self.indicies)==0:               #find index of colums for load, etc
          for cell in df.columns:
            if cell in code:
              self.indicies[code[cell]] = cell
              if self.verbose>1: print("     %-30s : %-20s "%(cell,code[cell]) )
            else:
              if self.verbose>1: print(" *** %-30s NOT USED"%cell)
            if "Harmonic" in cell or "Dyn. Frequency" in cell:
              self.method = Method.CSM
          #reset to ensure default values are set
          if not "p" in self.indicies: self.indicies['p']=self.indicies['pRaw']
          if not "h" in self.indicies: self.indicies['h']=self.indicies['hRaw']
          if not "t" in self.indicies: self.indicies['t']=self.indicies['tTotal']
          #if self.verbose: print("   Found column names: ",sorted(self.indicies))
      if "Tagged" in dfName: tagged.append(dfName)
    if len(tagged)>0 and self.verbose>1: print("Tagged ",tagged)
    if not "t" in self.indicies or not "p" in self.indicies or \
       not "h" in self.indicies or not "slope" in self.indicies:
      print("*WARNING*: INDENTATION: Some index is missing (t,p,h,slope) should be there")
    self.metaUser['measurementType'] = 'MTS, Agilent Indentation XLS'
    self.allTestList =  list(self.testList)
    self.nextAgilentTest()
    return True


  def nextAgilentTest(self, newTest=True):
    """
    Go to next sheet in worksheet and prepare indentation data

    Data: _Raw: without frame stiffness correction, _Frame:  with frame stiffness correction (remove postscript finally)
    - only affects/applies directly depth (h) and stiffness (s)
    - modulus, hardness and k2p always only use the one with frame correction

    Args:
      newTest: take next sheet (default)
    """
    if self.vendor!=Vendor.Agilent: return False #cannot be used
    if len(self.testList)==0: return False   #no sheet left
    if newTest:
      self.testName = self.testList.pop(0)

    #read data and identify valid data points
    df     = self.datafile.get(self.testName)
    h       = np.array(df[self.indicies['h'    ]][1:-1], dtype=np.float64)
    self.validFull = np.isfinite(h)   #pylint warning: Attribute 'validFull' defined outside __init__ (944:4) [attribute-defined-outside-init]
    if 'slope' in self.indicies:
      slope   = np.array(df[self.indicies['slope']][1:-1], dtype=np.float64)
      self.valid =  np.isfinite(slope)
      self.valid[self.valid] = slope[self.valid] > 0.0  #only valid points if stiffness is positiv
    else:
      self.valid = self.validFull
    for index in self.indicies:     #pylint convention: Consider iterating with .items() (951:4) [consider-using-dict-items]
      data = np.array(df[self.indicies[index]][1:-1], dtype=np.float64)
      mask = np.isfinite(data)
      mask[mask] = data[mask]<1e99
      self.valid = np.logical_and(self.valid, mask)                       #adopt/reduce mask continously

    #Run through all items again and crop to only valid data
    for index in self.indicies:       #pylint convention: Consider iterating with .items() (951:4) [consider-using-dict-items]
      data = np.array(df[self.indicies[index]][1:-1], dtype=np.float64)
      if not index in self.fullData:
        data = data[self.valid]
      else:
        data = data[self.validFull]
      setattr(self, index, data)
      # print(index, len(data))
    self.valid = self.valid[self.validFull]
    #  now all fields (incl. p) are full and defined

    success = self.identifyLoadHoldUnload()
    if self.onlyLoadingSegment and self.method==Method.CSM:
      # print("Length test",len(self.valid), len(self.h[self.valid]), len(self.p[self.valid])  )
      iMin, iMax = 2, self.iLHU[0][1]
      self.valid[iMax:] = False
      self.valid[:iMin] = False
      self.slope = self.slope[iMin:np.sum(self.valid)+iMin]

    #correct data and evaluate missing
    self.h /= 1.e3 #from nm in um
    if "Ac" in self.indicies         : self.Ac /= 1.e6  #from nm in um
    if "slope" in self.indicies       : self.slope /= 1.e3 #from N/m in mN/um
    if "slopeSupport" in self.indicies: self.slopeSupport /= 1.e3 #from N/m in mN/um     # pylint error: slopeSupport is not defined
    if 'hc' in self.indicies         : self.hc /= 1.e3  #from nm in um
    if 'hRaw' in self.indicies        : self.hRaw /= 1.e3  #from nm in um
    if not "k2p" in self.indicies and 'slope' in self.indicies:
      self.k2p = self.slope * self.slope / self.p[self.valid]
    return success


  def loadHysitron(self, fileName, plotContact=False):
    """
    Load Hysitron hld or txt file for processing, only contains one test

    Args:
       fileName: file name

       plotContact: plot intial contact identification (use this method for access)
    """
    from io import StringIO
    self.fileName = fileName
    inFile = open(self.fileName, 'r',encoding='iso-8859-1')   # pylint warning: Consider using 'with' for resource-allocating operations (1,000:13) [consider-using-with]
    #### HLD FILE ###
    if self.fileName.endswith('.hld'):
      line = inFile.readline()
      if not "File Version: Hysitron" in line:
        #not a Hysitron file
        inFile.close()
        return False
      if self.verbose>1:
        print("Open Hysitron file: "+self.fileName)

      #read meta-data
      prefact = [0]*6
      segmentTime = []
      segmentDeltaP = []
      segmentPoints = []
      while True:
        line = inFile.readline()
        label = line.split(":")[0]
        try:
          data = line.split(":")[1].split(" ")
          value = float(data[1])
          #if len(data)>2: unit  = data[2]
          #else:           unit  = ""
        except:     # pylint warning: No exception type(s) specified (1,024:8) [bare-except]
          value = line.split(":")[1].rstrip()
          #unit  = ""
        if label == "Sample Approach Data Points": break
        if label == "Machine Comp": self.compliance = value #assume nm/uN = um/mN
        if label == "Tip C0":       prefact[0] = value #nm^2/nm^2
        if label == "Tip C1":       prefact[1] = value #nm^2/nm
        if label == "Tip C2":       prefact[2] = value #nm^2/nm^0.5
        if label == "Tip C3":       prefact[3] = value #nm^2/nm^0.25
        if label == "Tip C4":       prefact[4] = value #nm^2/nm^0.125
        if label == "Tip C5":       prefact[5] = value #nm^2/nm^0.0625
        if label == "Contact Threshold": forceTreshold = value/1.e3 #uN
        if label == "Drift Rate":   self.metaVendor['drift_rate'] = value/1.e3 #um/s
        if label == "Number of Segments"  : numSegments  = value
        if label == "Segment Begin Time"  : segmentTime.append(value)
        if label == "Segment Begin Demand": pStart     = value
        if label == "Segment End Demand"  : segmentDeltaP.append( (value-pStart)/1.e3 ) #to mN
        if label == "Segment Points"      : segmentPoints.append(int(value))
        if label == "Time Stamp"          : self.timeStamp = ":".join(line.rstrip().split(":")[1:])
      self.tip.prefactors = prefact
      self.tip.prefactors.append('iso')
      if (numSegments!=len(segmentTime)) or (numSegments!=len(segmentDeltaP)):
        print("*ERROR*", numSegments,len(segmentTime),len(segmentDeltaP ) )
      segmentDeltaP = np.array(segmentDeltaP)
      segmentPoints = np.array(segmentPoints)
      segmentTime   = np.array(segmentTime)

      #read approach data
      line = inFile.readline() #Time_s  MotorDisp_mm    Piezo Extension_nm"
      data = ""
      for idx in range(int(value)):
        data +=inFile.readline()
      if len(data)>1:
        dataApproach = np.loadtxt( StringIO(str(data))  )     # pylint warning: dataApproach is unused-variable

      #read drift data
      value = inFile.readline().split(":")[1]
      line = inFile.readline()  #Time_s	Disp_nm",value
      data = ""
      for idx in range(int(value)):
        data +=inFile.readline()
      if len(data)>1:
        self.dataDrift = np.loadtxt( StringIO(str(data))  )
        self.dataDrift[:,1] /= 1.e3  #into um

      #read test data
      value = inFile.readline().split(":")[1]
      line = inFile.readline() #Time_s	Disp_nm	Force_uN	LoadCell_nm	PiezoDisp_nm	Disp_V	Force_V	Piezo_LowV
      data = ""
      for idx in range(int(value)):
        data +=inFile.readline()
      dataTest = np.loadtxt( StringIO(str(data))  )
      #store data
      self.t = dataTest[:,0]
      self.h = dataTest[:,1]/1.e3
      self.p = dataTest[:,2]/1.e3

      # create loading-holding-unloading cycles
      listLoading = np.where(segmentDeltaP>0.1 )[0]
      listUnload  = np.where(segmentDeltaP<-0.1)[0]
      segmentPoints  -= 1                     #since the first / last point of each segment are double in both segments
      segmentPoints[0]+=1
      segPnts   = np.cumsum(segmentPoints)
      self.iLHU = []
      for idx in range(len(listLoading)):
        iSurface = segPnts[listLoading[idx]-1]+1
        iLoad    = segPnts[listLoading[idx]]
        iHold    = segPnts[listUnload[idx]-1]+1
        iUnload  = segPnts[listUnload[idx]]
        self.iLHU.append( [iSurface,iLoad,iHold,iUnload] )

    #### TXT FILE ###
    if self.fileName.endswith('.txt'):
      line0 = inFile.readline()
      line1 = inFile.readline()
      line2 = inFile.readline()
      line3 = inFile.readline()
      self.metaUser = {'measurementType': 'Hysitron Indentation TXT', 'dateMeasurement':line0.strip()}
      if line1 != "\n" or "Number of Points" not in line2 or not "Depth (nm)" in line3:
        inFile.close()
        return False #not a Hysitron file
      if self.verbose>1: print("Open Hysitron file: "+self.fileName)
      dataTest = np.loadtxt(inFile)
      #store data
      self.t = dataTest[:,2]
      self.h = dataTest[:,0]/1.e3
      self.p = dataTest[:,1]/1.e3
      #set unknown values
      forceTreshold = 0.25 #250uN
      self.identifyLoadHoldUnload()

    #correct data
    #flatten intial section of retraction
    idxMinH  = np.argmin(self.h)
    self.p[:idxMinH] = self.p[idxMinH]
    self.h[:idxMinH] = self.h[idxMinH]
    idxMask = int( np.where(self.p>forceTreshold)[0][0])
    fractionMinH = 0.5
    hFraction    = (1.-fractionMinH)*self.h[idxMinH]+fractionMinH*self.h[idxMask]
    idxMask = np.argmin(np.abs(self.h-hFraction))
    if idxMask>2:
      mask     = np.zeros_like(self.h, dtype=bool)
      mask[:idxMask] = True
      fit = np.polyfit(self.h[mask],self.p[mask],1)
      self.p -= np.polyval(fit,self.h)

      #use force signal and its threshold to identify surface
      #Option: use lowpass-filter and then evaluate slope: accurate surface identifaction possible, however complicated
      #Option: use lowpass-filter and then use force-threshold: accurate surface identifaction, however complicated
      #Best: use medfilter or wiener on force signal and then use force-threshold: accurate and easy
      #see also Bernado_Hysitron/FirstTests/PhillipRWTH/testSignal.py
      pZero    = np.average(self.p[mask])
      pNoise   = max(pZero-np.min(self.p[mask]), np.max(self.p[mask])-pZero )
      #from initial loading: back-extrapolate to zero force
      maskInitLoad = np.logical_and(self.p>pZero+pNoise*2. , self.p<forceTreshold)
      maskInitLoad[np.argmax(self.p):] = False
      fitInitLoad  = np.polyfit(self.p[maskInitLoad],self.h[maskInitLoad],2)  #inverse h-p plot -> next line easier
      hZero        = np.polyval(fitInitLoad, pZero)
      ## idx = np.where(  self.p>(pZero+pNoise)  )[0][0] OLD SYSTEM NOT AS ACCURATE, better fitInitLoad
      if plotContact:
        """
        attempt to use dp/dt for contact identification
        from scipy import signal
        h = signal.wiener(self.h,5)
        p = signal.wiener(self.p,5)
        dpdt = (p[1:]-p[:-1])/(h[1:]-h[:-1])
        _, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax2.plot(h[:-1],dpdt)
        ax1.plot(h,p,'r')
        ax2.set_ylim([0,1000])
        plt.show()
        """
        plt.axhline(pZero,c='g', label='pZero')
        plt.axhline(pZero+pNoise,c='g',linestyle='dashed', label='pNoise')
        plt.axvline(self.h[idxMinH],c='k')
        plt.axvline(self.h[idxMask],c='k')
        plt.plot(self.h,self.p)
        plt.plot(self.h[mask],self.p[mask], label='used for pNoise')
        plt.plot(self.h[maskInitLoad],self.p[maskInitLoad], label='used for backfit')
        plt.axvline(hZero,c='r',linestyle='dashed',label='Start')
        plt.plot(hZero,pZero, "ro", label="Start")
        plt.legend(loc=0)
        plt.ylim(np.min(self.p), self.p[idx]+forceTreshold )
        plt.xlim(-0.1,self.h[idx]+0.05)
        plt.show()
        print ("Debug pZero and pNoise:",pZero,pNoise)
    else:
      print("Error", forceTreshold,np.where(self.p>forceTreshold)[0][:10])
      pZero = 0
      idx   = 0     #pylint warning: Using a conditional statement with a constant value (1,175:4) [using-constant-test]
    if True:
      ## self.t -= self.t[idx] #do not offset time since segment times are given
      self.h -= hZero
      self.p -= pZero
    inFile.close()
    return True



  def loadMicromaterials(self, fileName, plotContact=False):
    """
    Load Micromaterials txt file for processing, contains only one test

    Args:
       fileName: file name or file-content
       plotContact: plot intial contact identification (use this method for access)
    """
    if isinstance(fileName, io.TextIOWrapper) or fileName.endswith('.txt'):
      try:            #file-content given
        dataTest = np.loadtxt(fileName)  #exception caught
        if not isinstance(fileName, io.TextIOWrapper):
          self.fileName = fileName
          if self.verbose>1: print("Open Micromaterials file: "+self.fileName)
          self.metaUser = {'measurementType': 'Micromaterials Indentation TXT'}
      except:
        if self.verbose>1:
          print("Is not a Micromaterials file")
        return False
      self.t = dataTest[:,0]
      self.h = dataTest[:,1]/1.e3
      self.p = dataTest[:,2]
      self.valid = np.ones_like(self.t, dtype=bool)
      self.identifyLoadHoldUnload()
      return True
    if fileName.endswith('.zip'):
      if self.verbose>1:
        print("Open Micromaterials zip-file: "+fileName)
      self.datafile = ZipFile(fileName)
      self.testList = self.datafile.namelist()
      self.fileName = fileName
      self.nextMicromaterialsTest()
      self.metaUser = {'measurementType': 'Micromaterials Indentation ZIP'}
      return True
    return True


  def nextMicromaterialsTest(self):
    """
    Go to next file in zip or hdf5-file
    """
    if self.vendor!=Vendor.Micromaterials: #cannot be used
      return False
    if len(self.testList)==0: #no sheet left
      return False
    self.testName = self.testList.pop(0)
    myFile = self.datafile.open(self.testName)
    txt = io.TextIOWrapper(myFile, encoding="utf-8")
    success = self.loadMicromaterials(txt)
    return success


  def loadFischerScope(self,fileName):
    """
    Initialize txt-file from Fischer-Scope for processing

    Args:
      fileName: file name
    """
    self.metaVendor = {'date':[], 'shape correction':[], 'coordinate x':[], 'coordinate y':[],
            'work elastic':[], 'work nonelastic':[], 'EIT/(1-vs^2) [GPa]':[], 'HIT [N/mm]':[],
            'HUpl [N/mm]': [], 'hr [um]':[], 'hmax [um]':[], 'Compliance [um/N]':[],
            'epsilon':[], 'fit range': []}
    self.workbook = []
    self.testList = []
    self.fileName = fileName
    block = None
    with open(fileName,'r',encoding='iso-8859-1') as fIn:
      # read initial lines and initialialize
      line = fIn.readline()
      if ".hap	Name of the application" not in line:
        print("Not a Fischer Scope")
        return False
      identifier = line.split()[0]
      temp = fIn.readline()             # pylint warning： "temp" is unused variable
      self.metaVendor['Indent_Type'] = fIn.readline().split()[0]
      self.metaVendor['Indent_F'] = ' '.join( fIn.readline().split()[2:] )
      self.metaVendor['Indent_C'] = ' '.join( fIn.readline().split()[2:] )
      self.metaVendor['Indent_R'] = ' '.join( fIn.readline().split()[2:] )
      #read all lines after initial lines
      for line in fIn:
        pattern = identifier+r"   \d\d\.\d\d\.\d\d\d\d  \d\d:\d\d:\d\d"
        dataInLine = line.replace(',','.').split()
        dataInLine = [float(item) if isfloat(item) else None for item in dataInLine]
        if re.match(pattern, line) is not None:
          ## finish old individual measurement
          if block is not None:
            if np.array(block).shape[1]==5:
              df = pd.DataFrame(np.array(block), columns=['F','h','t','HMu','HM'] )
            else:
              df = pd.DataFrame(np.array(block), columns=['F','h','t'] )
            self.workbook.append(df)
          ## start new  individual measurement
          block = []
          self.metaVendor['date'] += [' '.join(line.split()[-2:])]
          self.testList.append('_'.join(line.split()[-2:]))
        elif line.startswith('Indenter shape correction:'):
          self.metaVendor['shape correction'] += [line.split()[-1]]
        elif 'x=  ' in line and 'y=  ' in line:
          self.metaVendor['coordinate x'] += [float(line.split()[1])]
          self.metaVendor['coordinate y'] += [float(line.split()[3])]
        elif line.startswith('We	['):
          self.metaVendor['work elastic'] += [line.split()[-1]]
        elif line.startswith('Wr	['):
          self.metaVendor['work nonelastic'] += [line.split()[-1]]
        elif line.startswith('EIT/(1-vs^2)	[GPa]') and not line.endswith('------\n'):
          self.metaVendor['EIT/(1-vs^2) [GPa]'] += [float(line.split()[-1])]
        elif line.startswith('HIT	[N/mm') and not line.endswith('------\n'):
          self.metaVendor['HIT [N/mm]'] += [float(line.split()[-1])]
        elif line.startswith('HUpl	[N/mm') and not line.endswith('------\n'):
          self.metaVendor['HUpl [N/mm]'] += [float(line.split()[-1])]
        elif line.startswith('hr	[') and not line.endswith('------\n'):
          self.metaVendor['hr [um]'] += [float(line.split()[-1])]
        elif line.startswith('hmax	[') and not line.endswith('------\n'):
          self.metaVendor['hmax [um]'] += [float(line.split()[-1])]
        elif line.startswith('Compliance	[') and not line.endswith('------\n'):
          self.metaVendor['Compliance [um/N]'] += [float(line.split()[-1])]
        elif 'Epsilon =' in line:
          self.metaVendor['epsilon'] += [float(line.split()[-1])]
          self.metaVendor['fit range'] += [' '.join(line.split()[:-3])]
        elif ( len(dataInLine)==3 or len(dataInLine)==5 ) and not (None in dataInLine): # pylint convention: Unnecessary parens after 'not' keyword (1,305:0) [superfluous-parens]
          block.append( dataInLine )
      ## add last dataframe
      if np.array(block).shape[1]==5:
        df = pd.DataFrame(np.array(block), columns=['F','h','t','HMu','HM'] )
      else:
        df = pd.DataFrame(np.array(block), columns=['F','h','t'] )
      self.workbook.append(df)
    if self.verbose>1:
      print("Meta information:",self.metaVendor)
      print("Number of measurements read:",len(self.workbook))
    self.metaUser['measurementType'] = 'Fischer-Scope Indentation TXT'
    if self.metaVendor['Indent_F'].startswith('ESP'):
      self.method = Method.MULTI
    else:
      self.method = Method.ISO
    self.nextFischerScopeTest()
    return True


  def nextFischerScopeTest(self):
    """
    Go to next dataframe
    """
    df = self.workbook.pop(0)
    self.testName = self.testList.pop(0)
    self.t = np.array(df['t'])
    self.h = np.array(df['h'])
    self.p = np.array(df['F'])
    self.valid = np.ones_like(self.t, dtype=bool)
    self.identifyLoadHoldUnload()
    return


  def loadHDF5(self,fileName):
    """
    Initialize hdf5-file that all converters are producing

    Args:
      fileName: file name
    """
    self.datafile = h5py.File(fileName)
    if self.verbose>1:
      print("Open hdf5-file: "+fileName)
    self.testList = []
    for key in self.datafile:
      if re.match(r'Test \d+',key):
        self.testList.append(key)
    self.fileName = fileName
    self.metaVendor = {}
    for key in self.datafile['metadata'].attrs:
      self.metaVendor[key] = self.datafile['metadata'].attrs[key]
    if 'json' in self.metaVendor:
      metaVendor = json.loads(self.metaVendor['json'])
      if 'SAMPLE' in metaVendor:  #G200X data
        if 'Dynamic' in metaVendor['SAMPLE']['@TEMPLATENAME']:
          self.method = Method.CSM
    converter = self.datafile['converter'].attrs['uri'].split('/')[-1]
    if converter == 'hap2hdf.cwl':
      self.metaUser = {'measurementType': 'Fischer-Scope Indentation HDF5'}
      self.unloadPMax = 0.99
      self.unloadPMin = 0.21
    elif converter == 'Micromaterials2hdf.cwl':
      self.metaUser = {'measurementType': 'Micromaterials Indentation HDF5'}
      self.unloadPMax = 0.99
      self.unloadPMin = 0.5
    elif converter == 'nmd2hdf.cwl':
      self.metaUser = {'measurementType': 'Agilent Indentation HDF5'}
      self.unloadPMax = 0.99
      self.unloadPMin = 0.5
    else:
      print("ERROR UNKNOWN CONVERTER")
    self.nextHDF5Test()
    return True


  def nextHDF5Test(self):
    """
    Go to next branch in HDF5 file
    TODO clean up the if statements after converter
    """
    if len(self.testList)==0: #no sheet left
      return False
    converter = self.datafile['converter'].attrs['uri'].split('/')[-1]
    self.testName = self.testList.pop(0)
    branch = self.datafile[self.testName]
    if 'loading' in branch:  #for Micromaterials Indenter
      self.t = np.hstack((np.array(branch['loading']['time']),
                          np.array(branch['hold at max']['time'])+branch['loading']['time'][-1],
                          np.array(branch['unloading']['time'])))
      self.h = np.hstack((np.array(branch['loading']['displacement']),
                          np.array(branch['hold at max']['displacement']),
                          np.array(branch['unloading']['displacement'])))/1.e3
      self.p = np.hstack((np.array(branch['loading']['force']),
                          np.array(branch['hold at max']['force']),
                          np.array(branch['unloading']['force'])))
      self.valid = np.ones_like(self.t, dtype=bool)
    else:
      if converter == 'nmd2hdf.cwl':   #G200X data has capital letters and is in SI units
        self.t = np.array(branch['Time'])
        self.h = np.array(branch['Displacement'])*1.e6
        self.p = np.array(branch['Force'])*1.e3
        self.p -= np.min(self.p)     #prevent negative forces
        if self.method==Method.CSM:
          self.slope = np.array(branch['DynamicStiffness'])/1.e3
          self.valid = ~np.isnan(self.slope)
          self.slope = self.slope[self.valid]
        else:
          self.valid = np.ones_like(self.t, dtype=bool)
      else:
        self.t = np.array(branch['time'])
        self.h = np.array(branch['displacement'])
        self.p = np.array(branch['force'])
        self.valid = np.ones_like(self.t, dtype=bool)
      if converter == 'hap2hdf.cwl':
        #Fischer-Scope reset the time multiple times
        resetPoints = np.where((self.t[1:]-self.t[:-1])<0)[0]
        self.t = self.t[resetPoints[-1]:]
        self.h = self.h[resetPoints[-1]:]
        self.p = self.p[resetPoints[-1]:]
        self.valid = np.ones_like(self.t, dtype=bool)
    self.identifyLoadHoldUnload()
    return True


  #@}
  ##
  # @name Output and plotting
  #@{
  def saveToUserMeta(self):
    """
    save results to user-metadata
    """
    if self.method == Method.CSM or len(self.slope)==1:
      i = -1 # only last value is saved
      meta = {"S_mN/um":self.slope[i], "hMax_um":self.h[self.valid][i], "pMax_mN":self.p[self.valid][i],\
                "modulusRed_GPa":self.modulusRed[i], "A_um2":self.Ac[i], "hc_um":self.hc[i], "E_GPa":self.modulus[i],\
                "H_GPa":self.hardness[i],"segment":str(i+1)}
    else:
      segments = [str(i+1) for i in range(len(self.slope))]
      meta = {"S_mN/um":self.slope, "hMax_um":self.h[self.valid], "pMax_mN":self.p[self.valid],\
              "modulusRed_GPa":self.modulusRed, "A_um2":self.Ac, "hc_um":self.hc, "E_GPa":self.modulus,\
              "H_GPa":self.hardness,"segment":segments}
    self.metaUser.update(meta)
    self.metaUser['code'] = __file__.split('/')[-1]
    return        #pylint warning: useless return


  def plotTestingMethod(self, saveFig=False, show=True):
    """
    plot testing method

    Args:
      saveFig: save plot to file [use known filename plus extension png]
      show: show figure, else do not show
    """
    fig, ax1 = plt.subplots()         # pylint warning: "fig" is unused variable
    ax2 = ax1.twinx()
    ax1.plot(self.t, self.p,'C0')
    ax2.plot(self.t, self.h,'C1')
    for mask in self.iLHU:
      ax1.plot(self.t[mask][0], self.p[mask][0], 'C0s')
      ax1.plot(self.t[mask][1], self.p[mask][1], 'C0x')
      ax1.plot(self.t[mask][2], self.p[mask][2], 'C0+')
      ax1.plot(self.t[mask][3], self.p[mask][3], 'C0o')
    ax1.plot(self.t[self.iDrift], self.p[self.iDrift], 'k.')
    ax1.axhline(0,color='C0', linestyle='dashed')
    ax2.axhline(0,color='C1', linestyle='dashed')
    ax1.set_xlabel(r"time [$\mathrm{s}$]")
    ax2.set_ylabel(r"depth [$\mathrm{\mu m}$]", color='C1', fontsize=14)
    ax1.set_ylabel(r"force [$\mathrm{mN}$]", color='C0', fontsize=14)
    plt.grid()
    plt.show()
    if saveFig:
      plt.savefig(self.fileName.split('.')[0]+".png", dpi=150, bbox_inches='tight')
    if show:
      plt.show()
    return ax1


  def plot(self, saveFig=False, show=True):
    """
    Plot force-depth curve with all data

    Args:
      saveFig: save plot to file [use known filename plus extension png]
      show: show figure, else do not show
    """
    if len(self.slope)==1 and self.verbose>1:
      print("Stiffness:"+str(round(self.slope[0],1))     +"mN/um   hMax:"+str(round(self.h[self.valid][0],4))+"um    pMax:"+str(round(self.p[self.valid][0],2))+"mN")
      print("E*:       "+str(round(self.modulusRed[0],1))+"GPa     A:   "+str(round(self.Ac[0],4))+          "um2    hc: "+str(round(self.hc[0],4))+"um")
      print("E:        "+str(round(self.modulus[0],1))   +"GPa     H:   "+str(round(self.hardness[0],1))+     "GPa")
    f, ax = plt.subplots()    #pylint warning: unused variable "f"
    ax.axhline(0,ls="dashed",c='k')
    ax.axvline(0,ls="dashed",c='k')
    ax.plot(self.h,self.p)
    if self.method != Method.CSM:
      _, _, maskUnload, optPar, _ = self.stiffnessFromUnloading(self.p, self.h)
      h_, p_ = self.h[maskUnload], self.p[maskUnload]
      ax.plot(self.h[maskUnload], self.UnloadingPowerFunc(self.h[maskUnload],*optPar), 'C1', label='fit powerlaw' )
      ax.plot(self.h[self.valid],self.p[self.valid],"or",label="max", markersize=10)
      ax.plot(self.hc, np.zeros_like(self.hc),"ob", label="hc", markersize=10)
      if len(self.hc)<2:
        ax.plot(h_[0],p_[0],'og',)
        ax.plot(h_[-1],p_[-1],'og', label="fit domain")
        Sn= self.p[self.valid]-self.slope*self.h[self.valid]
        h_ = np.linspace(self.hc,self.h[self.valid],10)
        ax.plot(h_,   self.slope*h_+Sn, 'r--', lw=2, label='stiffness')
      ax.legend(loc=0, numpoints=1)
    else:
      ax.plot(self.h[self.iLHU[0]],self.p[self.iLHU[0]],"or",label="specific", markersize=10)
    ax.set_xlim(left=-0.03)
    ax.set_xlabel(r"depth [$\mathrm{\mu m}$]")
    ax.set_ylabel(r"force [$\mathrm{mN}$]")
    if saveFig:
      plt.savefig(self.fileName.split('.')[0]+".png", dpi=150, bbox_inches='tight')
    if show:
      plt.show()
    return ax


  def plotAsDepth(self, property, saveFig=False, hvline=None):
    """
    Plot as function of depth either Young's modulus, hardness,
    stiffnessSquaredForce, ContactDepth, Contact Area, reducedModulus

    Args:
      property: what to plot on y-axis [E,H,K,K2P,hc,Ac,modulusRed]
      saveFig: save plot to file [use known filename plus extension png]
    """
    if not isinstance(property, str):
      print("**ERROR plotAsDepth: property=[E,H,K,K2P,hc,Ac,modulusRed]")
      return
    if hvline is not None:
      plt.axhline(hvline, c='k')
    if   property == "E":
      plt.plot(self.h[self.valid], self.modulus, "o")
      plt.ylabel("Young's modulus [GPa]")
    elif property == "modulusRed":
      plt.plot(self.h[self.valid], self.modulusRed, "o")
      plt.ylabel("reduced Young's modulus [GPa]")
    elif property == "H":
      plt.plot(self.h[self.valid], self.hardness, "o")
      plt.ylabel("Hardness [GPa]")
    elif property == "K":
      plt.plot(self.h[self.valid], self.slope, "o")
      plt.ylabel("Stiffness [kN/m]")
    elif property == "K2P":
      if not hasattr(self, 'k2p'):
        self.k2p = np.array(self.slope)*np.array(self.slope)/np.array(self.p[self.valid])
      plt.plot(self.h[self.valid], self.k2p, "C0o")
      mask = self.h[self.valid]>0.1
      fit = np.polyfit(self.h[self.valid][mask], self.k2p[mask],1)
      print('Fit: K2P='+str(round(fit[1]))+'+ '+str(round(fit[0]))+'*h')
      plt.plot(self.h[self.valid], np.polyval(fit,self.h[self.valid]), 'C1-')
      plt.axvline(0.1, linestyle='dashed',color='C1')
      plt.ylabel(r"Stiffness Squared Over Load [$\mathrm{GPa}$]")
    elif property == "hc":
      plt.plot(self.h[self.valid], self.hc, "o")
      plt.ylabel(r"Contact depth [$\mathrm{\mu m}$]")
    elif property == "Ac":
      plt.plot(self.h[self.valid], self.Ac, "o")
      plt.ylabel(r"Contact area [$\mathrm{\mu m^2}$]")
    else:
      print("Unknown property")
      return
    plt.xlabel(r"depth "+r'[$\mathrm{\mu m}$]')
    plt.show()
    return


  #@}
  ##
  # @name CALIBRATION METHOD
  #@{
  def calibration(self,eTarget=72.0,numPolynomial=3,critDepth=1.0,critForce=0.01,plotStiffness=False,plotTip=False, **kwargs):
    """
    Calibrate by first frame-stiffness and then area-function calibration

    Args:
       eTarget: target Young's modulus (not reduced), nu is known
       numPolynomial: number of area function polynomial; if None: return interpolation function
       critDepth: frame stiffness: what is the minimum depth of data used; area function: what is the maximum depth of data used
                  (if deep data is used for area function, this data can scew the area function)
       critForce: frame stiffness: what is the minimum force used for fitting
       plotStiffness: plot stiffness graph with compliance
       pltTip: plot tip shape after fitting
    """
    constantTerm = kwargs.get('constantTerm', False)
    frameCompliance, res = self.calibrateStiffness(critDepth=critDepth,critForce=critForce,plotStiffness=plotStiffness)

    ## re-create data-frame of all files
    temp = {'method': self.method, 'onlyLoadingSegment': self.onlyLoadingSegment}
    self.restartFile()
    self.tip.compliance = frameCompliance
    for item in temp:
      setattr(self, item, temp[item])
    if self.method==Method.CSM:
      self.nextAgilentTest(newTest=False)  #rerun to ensure that onlyLoadingSegment used
      slope = None
      while True:
        self.analyse()
        if slope is None:
          slope = self.slope
          h     = self.h[self.valid]
          p     = self.p[self.valid]
        else:
          slope = np.hstack((slope, self.slope))
          h     = np.hstack((h,     self.h[self.valid]))
          p     = np.hstack((p,     self.p[self.valid]))
        if not self.testList: break
        self.nextTest()
    else:
      dfNew = pd.DataFrame()
      while True:
        self.analyse()
        dfNew = dfNew.append(self.getDataframe())    # pylint error: "getDataframe" is not defined
        if len(self.testList)==0: break
        self.nextTest()
      slope = np.array(dfNew['S_mN/um'])
      ## verify (only makes sense for non-CSM because CSM calculates stiffness like this)
      totalCompliance = 1./dfAll['S_mN/um']      #error: dfAll is used before assignment
      contactStiffness = 1./(totalCompliance-frameCompliance) #mN/um
      print("Info: difference direct-indirect stiffness %",round(np.linalg.norm((slope-contactStiffness)/slope)*100,2),"%. Should be small")
      slope = np.array(dfNew['S_mN/um'])
      h     = dfNew['hMax_um']
      p     = dfNew['pMax_mN']

    ## fit shape function
    #reverse OliverPharrMethod to determine area function
    modulusRedGoal = self.ReducedModulus(eTarget, self.nuMat)
    Ac = np.array( np.power( slope  / (2.0*modulusRedGoal/np.sqrt(np.pi))  ,2))
    hc = np.array( h - self.beta*p/slope )
    #calculate shape function as interpolation of 30 points (log-spacing)
    #  first calculate the  savgol-average using a adaptive window-size
    if numPolynomial is None:
      # use interpolation function using random points
      data = np.vstack((hc,Ac))
      data = data[:, data[0].argsort()]
      windowSize = int(len(Ac)/20) if int(len(Ac)/20)%2==1 else int(len(Ac)/20)-1
      output = savgol_filter(data,windowSize,3)
      interpolationFunct = interpolate.interp1d(output[0,:],output[1,:])
      hc_ = np.logspace(np.log(0.0001),np.log(np.max(output[0,:])),num=30,base=np.exp(1))
      Ac_ = interpolationFunct(hc_)
      interpolationFunct = interpolate.interp1d(hc_, Ac_)
      del output, data
    else:
      #It is possible to crop only interesting contact depth: hc>1nm
      # Ac = Ac[hc>0.001]
      # hc = hc[hc>0.001]
      if constantTerm:
        appendix = 'isoPlusConstant'
      else:
        appendix = 'iso'
      def fitFunct(params):     #error function
        self.tip.prefactors = [params[x].value for x in params]+[appendix]
        A_temp = self.tip.areaFunction(hc)                #use all datapoints as critDepth is for compliance plot
        residual     = np.abs(Ac-A_temp)/len(Ac)             #normalize by number of points
        return residual
      # Parameters, 'value' = initial condition, 'min' and 'max' = boundaries
      params = lmfit.Parameters()
      params.add('m0', value= 24.3, min=10.0, max=60.0)
      for idx in range(1,numPolynomial):
        startVal = np.power(100,idx)
        params.add('m'+str(idx), value= startVal/1000, min=-startVal*100, max=startVal*100)
      if constantTerm:
        params.add('c',  value= 20, min=0.5, max=300.0) ##all prefactors are in nm, this has to be too
      # do fit, here with leastsq model; args=(hc, Ac)
      result = lmfit.minimize(fitFunct, params, max_nfev=10000)
      self.tip.prefactors = [result.params[x].value for x in result.params]+[appendix]
      print("\nTip shape:")
      print("  iterated prefactors",[round(i,1) for i in self.tip.prefactors[:-1]])
      stderr = [result.params[x].stderr for x in result.params]
      print("    standard error",['NaN' if x is None else round(x,2) for x in stderr])
      res['tip prefact factors and std.error'] = [self.tip.prefactors[:-1],stderr]

    if plotTip:
      if numPolynomial is None:
        self.tip.setInterpolationFunction(interpolationFunct)
      rNonPerfect = np.sqrt(Ac/np.pi)
      plt.plot(rNonPerfect, hc,'.')
      self.tip.plotIndenterShape(maxDepth=1.5)
      #Error plot
      plt.plot(hc,(Ac-self.tip.areaFunction(hc))/Ac,'o',markersize=2)
      plt.axhline(0,color='k',linewidth=2)
      plt.xlabel(r"Depth [$\mathrm{\mu m}$]")
      plt.ylabel("Relative area error")
      plt.ylim([-0.1,0.1])
      plt.xlim(left=0)
      plt.yticks([-0.1,-0.05,0,0.05,0.1])
      plt.show()

    #rerun everything with calibrated area function to see
    self.restartFile()
    for item in temp:
      setattr(self, item, temp[item])
    if self.method==Method.CSM:
      self.nextAgilentTest(newTest=False)  #rerun to ensure that onlyLoadingSegment used
    else:
      ## create data-frame of all files
      dfAll = pd.DataFrame()
      while True:
        self.analyse()
        dfAll = dfAll.append(self.getDataframe())   #error: undefined getDataframe
        if not self.testList: break
        self.nextTest()
      ## output representative values
      maskPrint = dfAll['pMax_mN'] > 0.95*np.max(dfAll['pMax_mN'])
      res['End Max depth: ave,stderr']=[dfAll['hMax_um'][maskPrint].mean(),dfAll['hMax_um'][maskPrint].std()/dfAll['hMax_um'][maskPrint].count()]
      res['End MeasStiff: ave,stderr']=[dfAll['S_mN/um'][maskPrint].mean(),dfAll['S_mN/um'][maskPrint].std()/dfAll['S_mN/um'][maskPrint].count()]
      res['End Ac: ave,stderr']=[      dfAll['A_um2'][maskPrint].mean(),  dfAll['A_um2'][maskPrint].std()/  dfAll['A_um2'][maskPrint].count()]
      res['End hc: ave,stderr']=[      dfAll['hc_um'][maskPrint].mean(),  dfAll['hc_um'][maskPrint].std()/  dfAll['hc_um'][maskPrint].count()]
      res['End E: ave,stderr']=[  dfAll['E_GPa'].mean(),   dfAll['E_GPa'].std()/   dfAll['E_GPa'].count()]
      res['End E_r: ave,stderr']=[dfAll['modulusRed_GPa'].mean(),dfAll['modulusRed_GPa'].std()/dfAll['modulusRed_GPa'].count()]
      res['End H: ave,stderr']=[  dfAll['H_GPa'].mean(),   dfAll['H_GPa'].std()/   dfAll['H_GPa'].count()]
    if numPolynomial is None:
      return res, interpolationFunct
    return res


  def calibrateStiffness(self,critDepth=1.0,critForce=0.0001,plotStiffness=True, returnAxis=False, returnData=False):
    """
    Calibrate by first frame-stiffness from K^2/P of individual measurement

    Args:
       critDepth: frame stiffness: what is the minimum depth of data used

       critForce: frame stiffness: what is the minimum force used for fitting

       plotStiffness: plot stiffness graph with compliance

       returnAxis: return axis of plot

       returnData: return data for external plotting
    """
    print("Start compliance fitting")
    ## output representative values
    res = {}
    if self.method==Method.CSM:
      x, y, h = None, None, None
      while True:
        self.analyse()
        if x is None:
          x = 1./np.sqrt(self.p[self.valid]-np.min(self.p[self.valid])+0.001) #add 1nm to prevent runtime error
          y = 1./self.slope
          h = self.h[self.valid]
        else:
          x = np.hstack((x,    1./np.sqrt(self.p[self.valid]-np.min(self.p[self.valid])+0.001) ))
          y = np.hstack((y,    1./self.slope))
          h = np.hstack((h, self.h[self.valid]))
        if not self.testList:
          break
        self.nextTest()
      mask = np.logical_and(h>critDepth, x<1./np.sqrt(critForce))
      if len(mask[mask])==0:
        print("WARNING too restrictive filtering, no data left. Use high penetration data: 50% of force and depth")
        mask = np.logical_and(h>np.max(h)*0.5, x<np.max(x)*0.5)
      maskPrint = []
    else:
      ## create data-frame of all files
      pAll, hAll, sAll = [], [], []
      while True:
        self.analyse()
        pAll = pAll+list(self.metaUser['pMax_mN'])
        hAll = hAll+list(self.metaUser['hMax_um'])
        sAll = sAll+list(self.metaUser['S_mN/um'])
        if not self.testList:
          break
        self.nextTest()
      pAll = np.array(pAll)
      hAll = np.array(hAll)
      sAll = np.array(sAll)
      maskPrint = pAll > 0.95*pAll
      res['Input Max force: ave,stderr'] = [pAll[maskPrint].mean(),pAll[maskPrint].std()/len(pAll[maskPrint])]
      res['Input Max depth: ave,stderr'] = [hAll[maskPrint].mean(),hAll[maskPrint].std()/len(hAll[maskPrint])]
      res['Input MeasStiff: ave,stderr'] = [sAll[maskPrint].mean(),sAll[maskPrint].std()/len(sAll[maskPrint])]
      ## determine compliance by intersection of 1/sqrt(p) -- compliance curve
      x = 1./np.sqrt(pAll)
      y = 1./sAll
      mask = hAll > critDepth
      mask = np.logical_and(mask, pAll>critForce)
    if len(mask[mask])==0:
      print("ERROR too much filtering, no data left. Decrease critForce and critDepth")
      return None

    param, covM = np.polyfit(x[mask],y[mask],1, cov=True)
    print("fit f(x)=",round(param[0],5),"*x+",round(param[1],5))
    frameStiff = 1./param[1]
    frameCompliance = param[1]
    print("  frame compliance: %8.4e um/mN = %8.4e m/N"%(frameCompliance,frameCompliance/1000.))
    stderrPercent = np.abs( np.sqrt(np.diag(covM)[1]) / param[1] * 100. )
    print("  compliance and stiffness standard error in %:",round(stderrPercent,2) )
    res['Stiffness and error in %']=[frameStiff,stderrPercent]
    print("  frame stiffness: %6.0f mN/um = %6.2e N/m"%(frameStiff,1000.*frameStiff))
    self.tip.compliance = frameCompliance

    #end of function
    if returnData:
      return x,y
    if plotStiffness:
      f, ax = plt.subplots()    # pylint warning: unused "f"
      ax.plot(x[~mask], y[~mask], 'o', color='#165480', fillstyle='none', markersize=1, label='excluded')
      ax.plot(x[mask], y[mask],   'C0o', markersize=5, label='for fit')
      x_ = np.linspace(0, np.max(x)*1.1, 50)
      y_ = np.polyval(param, x_)
      ax.plot(x_,y_,'w-')
      ax.plot(x_,y_,'C0--')
      ax.plot([0,np.min(x)/2],[frameCompliance,frameCompliance],'k')
      ax.text(np.min(x)/2,frameCompliance,'frame compliance')
      ax.set_xlabel(r"1/sqrt(p) [$\mathrm{mN^{-1/2}}$]")
      ax.set_ylabel(r"meas. compliance [$\mathrm{\mu m/mN}$]")
      ax.legend(loc=4)
      ax.set_ylim([0,np.max(y[mask])*1.5])
      ax.set_xlim([0,np.max(x[mask])*1.5])
      if returnAxis:
        return ax
      plt.show()
    return [frameCompliance, res]


  def isFusedSilica(self, bounds=[[610,700],[71,73],[8.9,10.1]], numPoints=50):     # pylint warning: Dangerous default value [] as argument (1,796:2) [dangerous-default-value]
    """
    Plot K2P, Modulus, Hardness plot to determine, if test if made on fused silica

    Args:
      bounds: min,max boundaries to determine if K2P,E,H are correct

      numPoints: number of points plotted in depth, used for interpolation
    """
    value      = ['k2p',      'modulus',   'hardness']
    plotBounds = [ [j-(j-i)*4,i+(j-i)*4] for [i,j] in bounds]
    fig, ax = plt.subplots(1,3,figsize=(10,5))        # pylint warning: unused "fig"
    result = {'vendor':{ 'average':[],'in boundaries':[]},\
      'recalibration':{ 'average':[],'in boundaries':[]} }

    #vendor data
    x, y = [],[[],[],[]]
    while True:
      for j in range(3):
        ax[j].plot(self.h[self.valid],     getattr(self,value[j]), c='C0', alpha=0.3)
        y[j] = np.concatenate((y[j], getattr(self,value[j])))
      x    = np.concatenate((x,self.h[self.valid]))
      if len(self.testList)==0: break
      self.nextTest()
    # create interpolating function
    f1 = []
    for j in range(3):
      # use interpolation function smoothing
      data = np.vstack((x,y[j]))
      data = data[:, data[0].argsort()]
      windowSize = int(len(x)/numPoints) if int(len(x)/numPoints)%2==1 else int(len(x)/numPoints)-1
      output = savgol_filter(data,windowSize,3)
      # save to array
      f1.append(interpolate.interp1d(output[0,:],output[1,:] ,'linear', fill_value="extrapolate"))
    # calculate statistics
    x1   = np.linspace(np.min(x), np.max(x), numPoints)
    mask = x1 > np.max(x1)/2
    print('\nVendor data (last 50%):')
    for j in range(3):
      average = round(np.average(f1[j](x1)[mask]),2)
      result['vendor']['average'].append(average)
      inBounds= np.logical_and( bounds[j][0]<=f1[j](x1)[mask], f1[j](x1)[mask]<=bounds[j][1] )
      inBounds= round(inBounds.sum()*1.0 / len(inBounds),2)
      result['vendor']['in boundaries'].append(inBounds)
      success = bounds[j][0]<=average and average<=bounds[j][1]   #pylint warning: Simplify chained comparison between the operands (1,840:16) [chained-comparison]
      result['vendor']['success'] = success
      print('  Average '+value[j]+':',average,'[GPa]   in boundary:',round(inBounds*100),'%',' success:',success)
    print()

    #new calibration
    self.restartFile()
    result['calibration'] = self.calibration(critDepth=0.5, plotStiffness=False, plotTip=False)
    self.restartFile()
    x, y = [],[[],[],[]]
    while True:
      self.analyse()
      for j in range(3):
        ax[j].plot(self.h[self.valid], getattr(self,value[j]), c='C1', alpha=0.3)
        y[j] = np.concatenate((y[j],   getattr(self,value[j])))
      x    = np.concatenate((x, self.h[self.valid]))
      if len(self.testList)==0: break
      self.nextTest()
    # create interpolating function
    f2 = []
    for j in range(3):
      # use interpolation function smoothing
      data = np.vstack((x,y[j]))
      data = data[:, data[0].argsort()]
      windowSize = int(len(x)/numPoints) if int(len(x)/numPoints)%2==1 else int(len(x)/numPoints)-1
      output = savgol_filter(data,windowSize,3)
      # save to array
      f2.append(interpolate.interp1d(output[0,:],output[1,:] ,'linear', fill_value="extrapolate"))
    # calculate statistics
    x2   = np.linspace(np.min(x), np.max(x), numPoints)
    mask = x2 > np.max(x2)/2
    print('\nRecalibration data (last 50%):')
    for j in range(3):
      average = round(np.average(f2[j](x2)[mask]),2)
      result['recalibration']['average'].append(average)
      inBounds= np.logical_and( bounds[j][0]<=f2[j](x2)[mask], f2[j](x2)[mask]<=bounds[j][1] )
      inBounds= round(inBounds.sum()*1.0 / len(inBounds),2)
      result['recalibration']['in boundaries'].append(inBounds)
      success = bounds[j][0]<=average and average<=bounds[j][1]
      result['recalibration']['success'] = success
      print('  Average '+value[j]+':',average,'[GPa]   in boundary:',round(inBounds*100),'%',' success:',success)
    print('\n')

    # add fake lines for legend
    ax[1].plot(0,-10, color='C0',label='vendor')
    ax[1].plot(0,-10, color='C1',label='re-calibrate')
    ax[1].plot(0,-10, color='k', label='boundary')
    ax[1].legend(loc=4)
    #plot avarages, bounds, format axis
    for j in range(3):
      ax[j].plot(x1,f1[j](x1), linewidth=3,c='C0')
      ax[j].plot(x2,f2[j](x2), linewidth=3,c='C1')
      ax[j].axhline(bounds[j][0] ,color='k',linewidth=2)
      ax[j].axhline(bounds[j][1], color='k',linewidth=2)
      ax[j].yaxis.tick_right()
      ax[j].tick_params(axis="y",direction="in", pad=-22)
      ax[j].tick_params(axis="x",direction="in", pad=-15)
      ax[j].text(.5,.95,value[j].upper(), horizontalalignment='center', transform=ax[j].transAxes, fontsize=14)
      if j==0:
        ax[j].text(.5,.05,r'depth [$\mathrm{\mu m}$]',horizontalalignment='center', transform=ax[j].transAxes, fontsize=10)
      ax[j].set_ylim(plotBounds[j])
      ax[j].set_xlim(left=0)
    #finalize
    plt.subplots_adjust(left=0.0,right=1,bottom=0.0,top=1.,wspace=0.)
    return result


  #@}
  ##
  # @name VERIFY METHODS
  #@{
  def verifyOneData(self):
    """
    Test one data set to ensure everything still working: OliverPharrMethod and area functions (normal and inverse)
    """
    self.tip.prefactors = [32.9049, -6418.303798, 288484.8518, -989287.0625, 103588.5588, 675977.3345, "iso"]
    print("Test CSM method, and area functions (normal and inverse)")
    #values from time=78.47sec of Cu_500muN_Creep_Vergleich
    harmStiff   = 159111.704268288/1000.   #  159111.704268288N/m
    load        = 0.491297865144331        #  0.491297865144331mN
    totalDepth  = 111.172457420282/1000.   #  111.901346020458nm
    print("   Set Poisson's ratio 0.35")
    self.nuMat = 0.35
    print("   From Agilent software")
    print("      harmStiff   = 159111.704268288 N/m")
    print("      load        = 0.49129786514433 mN")
    print("      totalDepth  = 111.901346020458 nm")
    print("      H           = 0.82150309678705 GPa")
    print("      E           = 190.257729329881 GPa")
    print("      modulusRed  = 182.338858733495 GPa")
    print("      Stiffness Squared Over Load=51529.9093101531 GPa")
    print("      ContactArea = 598047.490101769 nm^2")
    [modulusRed, Ac, _]  = self.OliverPharrMethod(np.array([harmStiff]), np.array([load]), np.array([totalDepth]))
    print("   Evaluated by this python method")
    print("      reducedModulus [GPa] =",round(modulusRed[0],4),"  with error=", round((modulusRed[0]-182.338858733495)*100/182.338858733495,4),'%')
    print("      ContactArea    [um2] =",round(Ac[0],4),"  with error=", round((Ac[0]-598047.490101769/1.e6)*100/598047.490101769/1.e6,4),'%')
    modulus = self.YoungsModulus(modulusRed)
    print("      Youngs Modulus [GPa] =",round(modulus[0],4),"  with error=", round((modulus[0]-190.257729329881)*100/190.257729329881,4),'%')
    totalDepth2 = self.inverseOliverPharrMethod(np.array([harmStiff]), np.array([load]), modulusRed)
    print("      By using inverse methods: total depth h=",totalDepth2[0], "[um]  with error=", round((totalDepth2[0]-totalDepth)*100/totalDepth,4),'%')
    print("End Test")
    return

  def verifyOneData1(self):
    """
    Test one data set to ensure everything still working: OliverPharrMethod and area functions (normal and inverse)
    """
    self.tip.prefactors = [24.8204,402.507,-3070.91,3699.87,"iso" ]
    self.tip.compliance = 1000.0/9.2358e6
    print("Test CSM method, and area functions (normal and inverse)")
    #values from time=78.47sec of FS.xls in 5Materials
    harmStiff   = 25731.8375827836/1000.   #  25731.8375827836 N/m
    load        = 0.987624311132669        #  0.987624311132669 mN
    totalDepth  = 88.2388854303261/1000.   #  88.2388854303261 nm
    print("   Set Poisson's ratio 0.18")
    self.nuMat = 0.18
    print("   From Agilent software")
    print("      harmContactStiff = 25731.8375827836 N/m")
    print("      load             = 0.987624311132669 mN")
    print("      totalDepth       = 88.2388854303261 nm")
    print("      H           = 10.0514655820034 GPa")
    print("      E           = 75.1620054287519 GPa")
    print("      Stiffness Squared Over Load=670.424429535749 GPa")
    [modulusRed, _, _]  = self.OliverPharrMethod(np.array([harmStiff]), np.array([load]), np.array([totalDepth]))
    modulus = self.YoungsModulus(modulusRed)
    print("      Youngs Modulus [GPa] =",modulus[0],"  with error=", round((modulus[0]-75.1620054287519)*100/75.1620054287519,4),'%'  )
    totalDepth2 = self.inverseOliverPharrMethod(np.array([harmStiff]), np.array([load]), modulusRed)
    print("      By using inverse methods: total depth h=",totalDepth2[0], "[um]  with error=", round((totalDepth2[0]-totalDepth)*100/totalDepth,4), '%')
    print("End Test")
    return

  def verifyReadCalc(self, plot=True):
    modulusRed,Ac,hc = self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid])
    modulus = self.YoungsModulus(modulusRed)
    hardness = self.p[self.valid] / Ac
    if self.method==Method.CSM:
      if plot:
        plt.plot(self.t[self.valid],self.hc,'o',label='read')
        plt.plot(self.t[self.valid],hc,label='calc')
        plt.legend(loc=0)
        plt.xlim(left=0)
        plt.ylim([0,np.max(self.hc)])
        plt.title("Error in hc: {0:.2e}".format(np.linalg.norm(hc-self.hc)) )
        plt.show()
      else:
        print("Error in hc: {0:.2e}".format(np.linalg.norm(hc-self.hc)) )
    else:
      print("Error in hc: %.3e %% between %.3e and %.3e" %(abs(hc-self.hc)*100./hc, hc, self.hc) )
    if self.method==Method.CSM:
      if plot:
        plt.plot(self.t[self.valid],self.Ac,'o',label='read')
        plt.plot(self.t[self.valid],Ac,label='calc')
        plt.legend(loc=0)
        plt.xlim(left=0)
        plt.ylim([0,np.max(self.Ac)])
        plt.title("Error in Ac: {0:.2e}".format(np.linalg.norm((Ac-self.Ac))) )
        plt.show()
      else:
        print("Error in Ac: {0:.2e}".format(np.linalg.norm((Ac-self.Ac))))
    else:
      print("Error in Ac: %.3e %% between %.3e and %.3e" %(abs(Ac-self.Ac)*100./Ac,Ac,self.Ac) )
    if self.method==Method.CSM:
      if plot:
        plt.plot(self.t[self.valid],self.modulusRed,'o',label='read')
        plt.plot(self.t[self.valid],modulusRed,label='calc')
        plt.legend(loc=0)
        plt.xlim(left=0)
        plt.ylim([0,np.max(self.modulusRed)])
        plt.title("Error in modulusRed: {0:.2e}".format(np.linalg.norm((modulusRed-self.modulusRed))) )
        plt.show()
      else:
        print("Error in modulusRed: {0:.2e}".format(np.linalg.norm((modulusRed-self.modulusRed))))
    else:
      print("Error in modulusRed: %.3e %% between %.3e and %.3e" %(abs(modulusRed-self.modulusRed)*100./modulusRed,modulusRed,self.modulusRed) )
    if self.method==Method.CSM:
      if plot:
        plt.plot(self.t[self.valid],self.modulus,'o',label='read')
        plt.plot(self.t[self.valid],modulus,label='calc')
        plt.legend(loc=0)
        plt.xlim(left=0)
        plt.ylim([0,np.max(self.modulus)])
        plt.title("Error in modulus: {0:.2e}".format(np.linalg.norm((modulus-self.modulus))) )
        plt.show()
      else:
        print("Error in modulus: {0:.2e}".format(np.linalg.norm((modulus-self.modulus))))
    else:
      print("Error in modulus:  %.3e %% between %.3e and %.3e" %(abs(modulus-self.modulus)*100./modulus, modulus,self.modulus) )
    if self.method==Method.CSM:
      if plot:
        plt.plot(self.t[self.valid],self.hardness,'o',label='read')
        plt.plot(self.t[self.valid],hardness,label='calc')
        plt.legend(loc=0)
        plt.xlim(left=0)
        plt.ylim([0,np.max(self.hardness)])
        plt.title("Error in hardness: {0:.2e}".format(np.linalg.norm((hardness-self.hardness))) )
        plt.show()
      else:
        print("Error in hardness: {0:.2e}".format(np.linalg.norm((hardness-self.hardness))))
    else:
      print("Error in hardness:  %.3e %% between %.3e and %.3e" %(abs(hardness-self.hardness)*100./hardness, hardness,self.hardness) )
    return
  #@}


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


class Tip:
  """
  The main class to define indenter shape and other default values.

  Initialize indenter shape

  Args:
    shape: list of prefactors (defualt = "perfect");

    interpFunction: tip-shape function Ac = f(hc), when it is given, other information are superseeded;

    compliance: additional compliance in test [um/mN] (sensible values: 0.0001..0.01);

    plot: plot indenter shape;

    verbose: output;
  """
  def __init__(self, shape="perfect", interpFunction=None, compliance=0.0, plot=False, verbose=0):

    #define indenter shape: could be overwritten
    if callable(interpFunction):
      self.prefactors = None
      self.interpFunction = interpFunction
    elif shape[-1]=="sphere" or shape[-1]=="iso":
      self.prefactors = shape
    elif type(shape)==list:  #assume iso      # pylint convention: Use isinstance() rather than type() for a typecheck. (2,077:9) [unidiomatic-typecheck]
      self.prefactors = shape
      self.prefactors.append("iso")
    else:
      self.prefactors = ["perfect"]
    self.compliance = compliance

    #verify and set default values
    if self.compliance > 0.01 or self.compliance < 0.0000001:
      if compliance == 0:
        if verbose>1:
          print("*WARNING*: stiffness outside domain 1e5...1e10 N/m: infinite")
      else:
        if verbose>1:
          print("*WARNING*: stiffness outside domain 1e5...1e10 N/m:",round(1000./self.compliance) )
    if plot:
      self.plotIndenterShape()
    return

  def __repr__(self):
    outString = 'compliance: '+str(self.compliance)+';   '
    if self.prefactors is None:
      outString+= 'with interpolation function with '+str(len(self.interpFunction.x))+' points'
    else:
      outString+= 'prefactors: '+str(self.prefactors)
    return outString


  def setInterpolationFunction(self,interpFunction):
    """
    The interpolation of tip-shape function Ac = f(hc).

    From Oliver-Pharr Method, projected area of contact Ac can be obtained by measuring contact depth hc.

    When the interpolation function is given, other information are superseeded.
    """
    self.interpFunction = interpFunction
    self.prefactors = None
    return

  def areaFunction(self, h):
    """
    AREA FUNCTION: from contact depth hc calculate area

    all functions inside are using [nm]; the outside of this function uses [um];

    hence at the start and end there is conversion

    prefactors:
    - "iso" type area function A=ax^2+bx^1+cx^0.5..., [nm]
    - "perfect" type area function of a perfect Berkovich A=3*sqrt(3)*tan(65.27)^2 hc^2 = 24.494 hc^2
    - "sphere" type: A=pi(2Rh-h^2), h=depth, R indenter radius; for small h-> h^2=0
               prefactors [-pi, 2piR], R in nm
               does not account for cone at top

   Args:
       h [array]: contact depth in um

    Returns:
       area: projected contact area [um^2]
    """
    h = h* 1000.   #starting here: all is in nm
    threshH = 1.e-3 #1pm
    h[h< threshH] = threshH
    area = np.zeros_like(h)
    if self.prefactors is None:
      self.interpFunction.bounds_error=False
      self.interpFunction.fill_value='extrapolate'
      return self.interpFunction(h/1000.)
    elif self.prefactors[-1]=='iso':      # pylint warning: Unnecessary "elif" after "return" (2,142:4) [no-else-return]
      for i in range(0, len(self.prefactors)-1):
        exponent = 2./math.pow(2,i)
        area += self.prefactors[i]*np.power(h,exponent)
        #print(i, self.prefactors[i], h,exponent, area)
    elif self.prefactors[-1]=='isoPlusConstant':
      h += self.prefactors[-2]
      for i in range(0, len(self.prefactors)-2):
        exponent = 2./math.pow(2,i)
        area += self.prefactors[i]*np.power(h,exponent)
    elif self.prefactors[-1]=='perfect':
      area = 24.494*np.power(h,2)
    elif self.prefactors[-1]=='sphere':
      radius = self.prefactors[0]*1000.
      openingAngle = self.prefactors[1]
      cos      = math.cos(openingAngle/180.0*math.pi)
      sin      = math.sin(openingAngle/180.0*math.pi)
      tan      = math.tan(openingAngle/180.0*math.pi)
      mask     = radius-h > radius*sin
      rA       = np.zeros_like(h)
      rA[mask] = np.sqrt(radius**2 - (radius-h[mask])**2 )  #spherical section
      deltaY = radius / cos			 #tapered section
      deltaX = radius-h[~mask]
      rA[~mask] = deltaY - tan*deltaX
      area = math.pi * rA * rA
    else:
      print("*ERROR*: prefactors last value does not contain type")
    area[area<0] = 0.0
    return area/1.e6 # conversion of unit from nm^2 to um^2


  def areaFunctionInverse(self, area, hc0=70):
    """
    INVERSE AREA FUNCTION: from area calculate contact depth hc

    using Newton iteration with initial guess contact depth hc0

    prefactors:
    -  "iso" type area function A=ax^2+bx^1+cx^0.5..., [nm]
    -  "perfect" type area function of a perfect Berkovich A=3*sqrt(3)*tan(65.27)^2 hc^2 = 24.494 hc^2

    Args:
       area: projected contact area

       hc0: initial Guess contact depth

    Returns:
       h: total penetration depth
    """
    ## define function in form f(x)-y=0
    def function(height):
      return self.areaFunction(np.array([height]))-area
    ## solve
    if self.prefactors[-1]=="iso":
      h = newton(function, hc0)
    elif self.prefactors[-1]=="perfect":
      h = math.sqrt(area / 24.494)
    else:
      print("*ERROR*: prefactors last value does not contain type")
    return h


  def plotIndenterShape(self, maxDepth=1, steps=2000, show=True, tipLabel=None, fileName=None):
    """
    check indenter shape: plot shape function against perfect Berkovich

    analytical: perfect shape is 2.792254*x

    Args:
       maxDepth: maximum depth [um] to plot; default=10um

       steps: number of steps for plotting

       show: show figure

       tipLabel: label for this tip

       fileName: if given, save to file
    """
    zoom = 0.5
    hc = np.linspace(0, maxDepth, steps)
    rNonPerfect = np.sqrt( self.areaFunction(hc)/math.pi)
    rPerfect  = 2.792254*hc
    if tipLabel is None:  tipLabel = 'this tip'
    plt.plot(rNonPerfect, hc, '-', label=tipLabel)
    plt.plot(rPerfect,hc, '-k', label='Berkovich')
    plt.plot(np.tan(np.radians(60.0))*hc,hc, '--k', label='$60^o$')
    plt.legend(loc="best")
    plt.ylabel(r'contact depth [$\mathrm{\mu m}$]')
    plt.xlabel(r'contact radius [$\mathrm{\mu m}$]')
    plt.xlim([0,maxDepth*4./3./zoom])
    plt.ylim([0,maxDepth/zoom])
    if show:
      plt.grid()
      if fileName is not None:
        plt.savefig(fileName, dpi=150, bbox_inches='tight')
      plt.show()
    return
