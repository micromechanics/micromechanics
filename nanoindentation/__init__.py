"""
Classes to evaluate indentation data and indenter tip

Indentation data: indentation experiment
- Methods: iso (can have multiple unloading segments), csm
- Vendor: Agilent, Hysitron

Indenter tip: shape of indenter tip and gantry stiffness (that what you calibrate)

UNITS: one should use mSB units in this code, since Agilent area function is unit-dependent
mSB: [mN], [um], [GPa] (force, length, stress)


#### Variables: differentiate different length ########
array of full length: force, time, depth, validMask, ...  [used for plotting]
array of valid length: E,H,Ac,hc, ... [only has the length where these values are valid]
   force[validMask] = pMax
   all these are vectors: OliverPharr et al methods are only vector functions

Coding rules:
- Change all variables: do not keep original-depth as can be reread and makes code less readable
"""
import os
from .definitions import Method, Vendor, FileType
from .tip import Tip

class Indentation:
  """
  Main class of indentation
  """
  #pylint: disable=import-outside-toplevel
  from .calibration import calibration, calibrateStiffness
  from .input import loadAgilent, nextAgilentTest, loadHysitron, loadMicromaterials, nextMicromaterialsTest, \
    loadFischerScope, nextFischerScopeTest, loadHDF5, nextHDF5Test
  from .main import popIn, calcYoungsModulus, calcHardness, calcStiffness2Force, analyse, \
    identifyLoadHoldUnload, identifyLoadHoldUnloadCSM, nextTest, saveToUserMeta
  from .plot import plotTestingMethod, plot, plotAsDepth
  from .theory import YoungsModulus, ReducedModulus, OliverPharrMethod, inverseOliverPharrMethod,\
    stiffnessFromUnloading, unloadingPowerFunc
  from .verification import verifyOneData, verifyOneData1, verifyReadCalc
  #pylint: enable=import-outside-toplevel

  def __init__(self, fileName, nuMat= 0.3, tip=None, surfaceFind={}, verbose=2):
    """
    Initialize indentation experiment data

    Args:
       fileName: fileName to open (.xls, .hld)
       nuMat: material's Poisson ratio.
       tip:  tip class to use; None=perfect
       verbose: the higher, the more information printed: 2=default, 1=minimal, 0=print nothing
    """
    self.nuMat = nuMat                                      #nuMat: material's Posson ratio
    self.nuTip      = 0.07
    self.modulusTip = 1140                                    #GPa from Oliver,Pharr Method paper
    self.beta = 0.75                                        #beta: contact depth coefficient
    self.verbose = verbose
    self.method    = Method.ISO                             #iso default: csm uses different methods
    self.onlyLoadingSegment = False                         #use all data by default

    if tip is None:
      tip = Tip()
    self.tip = tip
    self.surfaceFind = surfaceFind
    self.iLHU   = [ [-1,-1,-1,-1] ]                         #indicies of Load-Hold-Unload cycles
                                                            #(StartLoad-StartHold-StartUnload-EndLoad)
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
