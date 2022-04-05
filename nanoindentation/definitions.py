"""Definitions used in the nanoindent functions"""
from enum import Enum

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
