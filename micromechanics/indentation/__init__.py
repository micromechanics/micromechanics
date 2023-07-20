"""
Classes to evaluate indentation data and indenter tip

- Methods: iso, multiple unloading segments, csm
- Vendor: Agilent, Hysitron, FischerScope, Micromaterials
- Indenter tip: shape of indenter tip and gantry stiffness (that what you calibrate)

UNITS: one should use mSI units in this code, since Agilent area function is unit-dependent |br|
[mN], [um], [GPa] (force, length, stress)

Variables: differentiate different length

- array of full length: force, time, depth, validMask, ...  [used for plotting]
- array of valid length: E,H,Ac,hc, ... [only has the length where these values are valid]
- force[validMask] = pMax
- all these are vectors: OliverPharr et al methods are only vector functions

Coding rules:

- Change all variables: do not keep original-depth as can be reread and makes code less readable
"""
import os
from pathlib import Path
import numpy as np
from .definitions import Method, Vendor, FileType
from .tip import Tip

class Indentation:
  """
  Main class of indentation
  """
  #pylint: disable=import-outside-toplevel
  from .input import loadAgilent, nextAgilentTest, loadHysitron, loadMicromaterials, nextMicromaterialsTest, \
    loadFischerScope, nextFischerScopeTest, loadHDF5, nextHDF5Test, restartFile
  from .main import calcYoungsModulus, calcHardness, calcStiffness2Force, analyse, \
    identifyLoadHoldUnload, identifyLoadHoldUnloadCSM, nextTest, saveToUserMeta, correctThermalDrift
  from .theory import YoungsModulus, ReducedModulus, OliverPharrMethod, inverseOliverPharrMethod,\
    stiffnessFromUnloading, unloadingPowerFunc
  from .hertz import popIn, hertzFit
  from .plot import plotTestingMethod, plot, plotAsDepth, plotAll
  from .calibration import calibration, calibrateStiffness
  from .verification import verifyOneData, verifyOneData1, verifyReadCalc
  from .definitions import _DefaultModel, _DefaultOutput, _DefaultSurface, _DefaultVendorDependent
  from .seldomUsedFunctions import tareDepthForce, analyseDrift

  def __init__(self, fileName=None, nuMat= 0.3, tip=None, surface={}, model={}, output={}):
    """
    Initialize indentation experiment data

    Args:
       fileName (str): fileName to open (.xls, .hld)
       nuMat (float): material's Poisson ratio.
       tip (tip):  tip class to use; None=perfect
       surface (dict): dictionary describing the surface find
       model (dict): numerical parameters that determine the evaluation
       output (dict): links that descripe the output (graphs and print-to-screen)
    """
    np.seterr(divide='ignore', invalid='ignore')
    self.nuMat   = nuMat                            # nuMat: material's Posson ratio
    self.method  = Method.ISO                       # iso default: csm uses different methods
    self.tip     = Tip() if tip is None else tip    # nanoindenter tip and compliance
    self.surface = dict(self._DefaultSurface)       # dictionary describing the surface find
    self.surface.update(surface)
    self.model   = self._DefaultModel               # dictionary for all numerical parameters that determine the results
    self.modelUserChoice = model
    self.model.update(self.modelUserChoice)
    self.output  = self._DefaultOutput              # dictionary for all output parameters, axis
    self.output.update(output)

    self.newFileRead = True                                 #file was just loaded
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
    if fileName is None:
      fileName = str(Path(__file__).parent/'data/Example.xls')
    if not os.path.exists(fileName) and fileName!='':
      print("*ERROR* __init__: file does not exist",fileName)
      return
    if fileName.endswith(".xls") or fileName.endswith(".xlsx"):
      # KLA, Agilent, Keysight, MTS
      self.vendor = Vendor.Agilent
      self.fileType = FileType.Multi
      self.fillVendorDefaults()
      success = self.loadAgilent(fileName)
    if (fileName.endswith(".hld") or fileName.endswith(".txt")) and not success:
      # Hysitron
      self.vendor = Vendor.Hysitron
      self.fileType = FileType.Single
      self.fillVendorDefaults()
      success = self.loadHysitron(fileName)
    if (fileName.endswith(".txt") or
        fileName.endswith(".zip")) and not success:
      # Micromaterials
      self.vendor = Vendor.Micromaterials
      self.fillVendorDefaults()
      if fileName.endswith(".txt"):
        self.fileType = FileType.Single
      else:
        self.fileType = FileType.Multi
      success = self.loadMicromaterials(fileName)
    if fileName.endswith(".txt") and not success:
      # Fischer Scope
      self.vendor = Vendor.FischerScope
      self.fileType = FileType.Multi
      self.fillVendorDefaults()
      success = self.loadFischerScope(fileName)
    if fileName.endswith(".hdf5") and not success:
      # Common hdf5 file: refined later
      self.vendor = Vendor.Hdf5
      self.fileType = FileType.Multi
      self.fillVendorDefaults()
      success = self.loadHDF5(fileName)
    return


  def fillVendorDefaults(self):
    """
    fill defaults depending on vendor, if information is not yet present
    """
    if self.vendor in self._DefaultVendorDependent:
      for key, valueDefault in self._DefaultVendorDependent[self.vendor].items():
        if key in self.modelUserChoice:
          self.model[key] =  self.modelUserChoice[key]
        elif key not in self.model:
          self.model[key]=valueDefault
    else:
      print('**ERROR defaults not defined for',self.vendor)
    return


  #defining an iterator for cleaner usage
  #https://www.programiz.com/python-programming/iterator
  #Building Custom Iterators
  def __iter__(self):
    """
    Python iterator

    Returns:
      indentation: iterator
    """
    self.restartFile()
    self.newFileRead = True                                 #just read the file
    return self


  def __next__(self):
    """
    Go to next iterator

    Returns:
      str: test name
    """
    if self.testList and len(self.testList)>0:
      if self.newFileRead:                                  #skip/redo first run through
        self.newFileRead=False
      else:
        reply = self.nextTest()
        if not reply:
          raise StopIteration
    else:
      raise StopIteration
    return self.testName
