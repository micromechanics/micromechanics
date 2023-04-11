"""Definitions used in the nanoindent functions"""
from enum import IntEnum

# enum classes: make code more readable
class Method(IntEnum):
  """
  Nanoindentation method: e.g. one unloading, multiple,...
  """
  ISO = 1    #one unloading
  MULTI = 2  #multiple ISO unloadings in one loading curve
  CSM = 3    #CSM method: number of unloadings ~ all data-points


class Vendor(IntEnum):
  """
  HDF5 files are converted
  TXT, XLS files are exported
  """
  Agilent            = 1  #Agilent, KLA, MTS: XLS file format                    # pylint: disable=invalid-name
  Hysitron           = 2  #Hysitron HLD or TXT file format                       # pylint: disable=invalid-name
  Micromaterials     = 3  #Micromaterials TXT, ZIP of TXT file format            # pylint: disable=invalid-name
  FischerScope       = 4  #FischerScope TXT file format                          # pylint: disable=invalid-name
  Hdf5               = 10 #This hdf5 should work for all indenters               # pylint: disable=invalid-name
  AgilentHDF5        = 11 #Agilent, KLA, MTS: HDF5 file format                   # pylint: disable=invalid-name
  HysitronHDF5       = 12 #Hysitron HDF5 file format                             # pylint: disable=invalid-name
  MicromaterialsHDF5 = 13 #Micromaterials HDF5 file format                       # pylint: disable=invalid-name
  FischerScopeHDF5   = 14 #FischerScope HDF5 file format                         # pylint: disable=invalid-name
  KLAHDF5            = 15 #Micromaterials HDF5 file format                       # pylint: disable=invalid-name


class FileType(IntEnum):
  """
  Type of file: containing one or multiple tests
  """
  Single = 1  #single test in file                                              # pylint: disable=invalid-name
  Multi  = 2  #multiple tests in file                                           # pylint: disable=invalid-name

#TODO_P1 defaults to documentation
_DefaultModel = {
  'nuTip':      0.07,
  'modulusTip': 1140,       # GPa from Oliver,Pharr Method paper
  'beta':       0.75,       # beta: contact depth coefficient
  'nonMetal':   1,          # switch between metal=0 and nonMetal=amorphous=default=1.
  'driftRate':  0,          # drift rate in [um/s]

  'unloadPMax':0.99,        # upper end of fitting domain of unloading stiffness: Vendor-specific change
  'unloadPMin':0.5,         # lower end of fitting domain of unloading stiffness: Vendor-specific change
  'relForceRateNoise':0.02, # threshold of dp/dt use to identify start of loading: Vendor-specific change
  'relForceRateNoiseFilter': 'median',
  'forceNoise': 0.001,      # threshold force to identify start of loading
  'evaluateSAtMax': True,   # evaluate stiffness at maximum or at end of power-law fit domain
  'maxSizeFluctuations': 10 # maximum size of small fluctuations that are removed in identifyLoadHoldUnload
}

_DefaultVendorDependent = {
  Vendor.Agilent:           {'unloadPMax':0.999,'unloadPMin':0.5, 'relForceRateNoise':0.02},
  Vendor.Hysitron:          {'unloadPMax':0.95, 'unloadPMin':0.4, 'relForceRateNoise':0.2},
  Vendor.Micromaterials:    {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceRateNoise':0.02},
  Vendor.FischerScope:      {'unloadPMax':0.95, 'unloadPMin':0.21,'relForceRateNoise':0.01},
  Vendor.Hdf5:              {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceRateNoise':0.02},
  Vendor.AgilentHDF5:       {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceRateNoise':0.02},
  Vendor.KLAHDF5:           {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceRateNoise':0.007},#enhanced accuracy
  Vendor.FischerScopeHDF5:  {'unloadPMax':0.99, 'unloadPMin':0.21, 'relForceRateNoise':0.02},#reduced accuracy
  Vendor.MicromaterialsHDF5:{'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceRateNoise':0.02},
  Vendor.HysitronHDF5:      {'unloadPMax':0.99, 'unloadPMin':0.5, 'relForceRateNoise':0.04}
}


_DefaultOutput = {
  'verbose': 2,          # the higher, the more information printed: 2=default, 1=minimal, 0=print nothing
  'plotAll': False,      # plot intermediate steps; helpful for debugging
  'ax': None,            # matplotlib axis to use for plotting
  'plotWithLabel': False,# plot legend
  'progressBar': None,   # callback function to use for plotting progress bar f(value, location)
  'successTest': []      # list of all test with valid load-hold-unload sequence
}

_DefaultSurface = {
  'surfaceIdx': {}
}
