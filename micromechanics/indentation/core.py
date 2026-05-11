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
import copy
from pathlib import Path
from collections.abc import Callable
from types import SimpleNamespace
from typing import cast, Any
from typing_extensions import TypedDict
import numpy as np
from matplotlib.axes import Axes
from .calibration import IndentationCalibrationMixin
from .definitions import (FileType, Method, Vendor, _DefaultModel, _DefaultOutput, _DefaultSurface, _DefaultVendorDependent)
from .hertz import IndentationHertzMixin
from .input import IndentationInputMixin
from .main import IndentationMainMixin
from .plot import IndentationPlotMixin
from .theory import IndentationTheoryMixin
from .tip import Tip
from .verification import IndentationVerificationMixin




class Indentation(IndentationInputMixin, IndentationMainMixin, IndentationTheoryMixin, IndentationHertzMixin, IndentationPlotMixin,
                  IndentationCalibrationMixin, IndentationVerificationMixin):
  """
  Main class of indentation
  """
  def __init__(self, fileName:str='', nuMat:float= 0.3, tip:Tip|None=None, surface:dict[str, dict[str, Any]]|None=None,
               model:dict[str, float|bool|str]|None=None, output:dict[str, Any]|None=None) -> None:
    """
    Initialize indentation experiment data

    Args:
       fileName (str): fileName to open (.xls, .hld)
       nuMat (float): material's Poisson ratio.
       tip (tip):  tip class to use; None=perfect
       surface (dict): dictionary describing the surface find
       model (dict): numerical parameters that determine the evaluation
       output (dict): links that describe the output (graphs and print-to-screen)
    """
    np.seterr(divide='ignore', invalid='ignore')
    self.nuMat   = nuMat                            # nuMat: material's Poisson ratio
    self.method  = Method.ISO                       # iso default: csm uses different methods
    self.vendor:Vendor
    self.fileType:FileType
    self.tip:Tip = Tip() if tip is None else tip    # nanoindenter tip and compliance
    self.surface:dict[str, dict[str, Any]]         = copy.deepcopy(_DefaultSurface) if surface is None else \
                                                     copy.deepcopy(_DefaultSurface)|surface
    self.modelUserChoice:dict[str, float|bool|str] = {} if model is None else model
    self.model:dict[str, float|bool|str]           = copy.deepcopy(_DefaultModel) if model is None else \
                                                     copy.deepcopy(_DefaultModel)|model
    self.output:dict[str, Any]                     = copy.deepcopy(_DefaultOutput) if output is None else \
                                                     copy.deepcopy(_DefaultOutput)|output

    self.newFileRead               = True                # file was just loaded
    self.iLHU:list[list[int]]      = []                  # indices of Load-Hold-Unload cycles
                                                         # (start load, start hold, start unload, end unload)
    self.metaVendor:dict[str, Any] = {}                  # some results come from input file
    self.metaUser: dict[str, float|list[float]|str] = {} # type: ignore[assignment]  #metadata added by analysis
    self.raw = SimpleNamespace(                          # loaded/prepared input arrays in package units
      h=np.array([], dtype=float),
      p=np.array([], dtype=float),
      t=np.array([], dtype=float),
      valid=np.array([], dtype=bool),
      slope=np.array([], dtype=float),
      phase=np.array([], dtype=float))
    self.provenance:dict[str, dict[str, Any]] = {}       # raw and working array source/correction state

    # define all attributes
    self.testName              = ''
    self.testList:list[str]    = []
    self.allTestList:list[str] = []
    self.h         :np.ndarray = np.array([], dtype=float)
    self.t         :np.ndarray = np.array([], dtype=float)
    self.p         :np.ndarray = np.array([], dtype=float)
    self.valid     :np.ndarray = np.array([], dtype=bool)
    self.hRaw      :np.ndarray = np.array([], dtype=float)
    self.slope     :np.ndarray = np.array([], dtype=float)
    self.phase     :np.ndarray = np.array([], dtype=float)
    self.k2p       :np.ndarray = np.array([], dtype=float)
    self.hc        :np.ndarray = np.array([], dtype=float)
    self.Ac        :np.ndarray = np.array([], dtype=float)
    self.modulus   :np.ndarray = np.array([], dtype=float)
    self.modulusRed:np.ndarray = np.array([], dtype=float)
    self.hardness  :np.ndarray = np.array([], dtype=float)

    #initialize and load first data set
    #set default parameters
    success = False
    recognized = False
    if not fileName:
      fileName = str(Path(__file__).parent/'data/Example.xls')
    if not os.path.exists(fileName):
      if fileName!='':
        print("**ERROR** __init__: file does not exist",fileName)
        return
      else:
        recognized = True
        success = True
    if fileName.endswith(".xls") or fileName.endswith(".xlsx"):
      # KLA, Agilent, Keysight, MTS
      recognized = True
      self.vendor = Vendor.Agilent
      self.fileType = FileType.Multi
      self.fillVendorDefaults()
      success = self.loadAgilent(fileName)
    if (fileName.endswith(".hld") or fileName.endswith(".txt")) and not success:
      # Hysitron
      recognized = True
      self.vendor = Vendor.Hysitron
      self.fileType = FileType.Single
      self.fillVendorDefaults()
      success = self.loadHysitron(fileName)
    if (fileName.endswith(".txt") or
        fileName.endswith(".zip")) and not success:
      # Micromaterials
      recognized = True
      self.vendor = Vendor.Micromaterials
      self.fillVendorDefaults()
      if fileName.endswith(".txt"):
        self.fileType = FileType.Single
      else:
        self.fileType = FileType.Multi
      success = self.loadMicromaterials(fileName)
    if fileName.endswith(".txt") and not success:
      # Fischer Scope
      recognized = True
      self.vendor = Vendor.FischerScope
      self.fileType = FileType.Multi
      self.fillVendorDefaults()
      success = self.loadFischerScope(fileName)
    if fileName.endswith(".hdf5") and not success:
      # Common hdf5 file: refined later
      recognized = True
      self.vendor = Vendor.Hdf5
      self.fileType = FileType.Multi
      self.fillVendorDefaults()
      success = self.loadHDF5(fileName)
    if not success:
      if recognized:
        print('**ERROR** __init__: file recognized but could not be loaded',fileName)
      else:
        print('**ERROR** __init__: file type not recognized or not supported',fileName)
    return


  def fillVendorDefaults(self) -> None:
    """
    fill defaults depending on vendor, if information is not yet present
    """
    if self.vendor in _DefaultVendorDependent:
      self.model = self.model|_DefaultVendorDependent[self.vendor]|self.modelUserChoice
    else:
      print('**ERROR** defaults not defined for',self.vendor)
    return


  #defining an iterator for cleaner usage
  #https://www.programiz.com/python-programming/iterator
  #Building Custom Iterators
  def __iter__(self) -> 'Indentation':
    """
    Python iterator

    Returns:
      indentation: iterator
    """
    self.restartFile()
    self.newFileRead = True                                 #just read the file
    return self


  def __next__(self) -> str:
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
