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


_DefaultModel = {
  'nuTip':      0.07,
  'modulusTip': 1140,    #GPa from Oliver,Pharr Method paper
  'beta':       0.75,    #beta: contact depth coefficient
  'nonMetal':   1,       #switch between metal=0 and nonMetal=amorphous=default=1.
  'driftRate':  0,       #drift rate in [um/s]
}

_DefaultVendorDependent = {
  Vendor.Agilent:         {'unloadPMax':0.999,'unloadPMin':0.5, 'relForceNoise':0.02},
  Vendor.Hysitron:        {'unloadPMax':0.95, 'unloadPMin':0.4, 'relForceNoise':0.2},
  Vendor.Micromaterials:  {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceNoise':0.02},
  Vendor.FischerScope:    {'unloadPMax':0.95, 'unloadPMin':0.21,'relForceNoise':0.01},
  Vendor.CommonHDF5:      {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceNoise':0.02},

  'hap2hdf.py':           {'unloadPMax':0.99, 'unloadPMin':0.21, 'relForceNoise':0.02},#reduced accuracy
  'Micromaterials2hdf.py':{'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceNoise':0.02},
  'nmd2hdf.py':           {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceNoise':0.007},#enhanced accuracy
  'xls2hdf.py':           {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceNoise':0.02},
  'converter_tdm.py':     {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceNoise':0.04}
}


_DefaultOutput = {
  'verbose': 2,          #the higher, the more information printed: 2=default, 1=minimal, 0=print nothing
  'plotAll': False       #plot intermediate steps; helpful for debugging
}

_DefaultSurface = {
  'surfaceIdx': {}
}
