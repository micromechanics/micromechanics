"""Most central functions for nanoindentation"""

import traceback
from typing import TYPE_CHECKING
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import fmin_l_bfgs_b
from .definitions import Vendor, Method
from .theory import _dictToFloat

if TYPE_CHECKING:
  from .core import Indentation

class IndentationMainMixin:
  """
  Main analysis workflow methods for :class:`Indentation`.
  """
  def _restoreRaw(self:'Indentation') -> None: # type: ignore[misc]
    """
    Restore working arrays from the raw package-unit snapshot.
    """
    for name in ('h', 'p', 't', 'valid', 'slope', 'phase'):
      value = getattr(self.raw, name)
      if isinstance(value, np.ndarray) and len(value)>0:
        setattr(self, name, value.copy())
    self._setWorkingProvenance('raw')
    return


  def _setWorkingProvenance(self:'Indentation', state:str) -> None: # type: ignore[misc]
    """
    Record whether working arrays are raw or analysis-derived.
    """
    self.provenance.setdefault('working', {})['state'] = state
    return


  def _workingIsAnalysisResult(self:'Indentation') -> bool: # type: ignore[misc]
    """
    Check whether working arrays currently contain analyse()-derived changes.
    """
    return self.provenance.get('working', {}).get('state') == 'analysed'


  def _rawIsEmpty(self:'Indentation') -> bool: # type: ignore[misc]
    """
    Check if no input path has populated raw data yet.
    """
    return len(self.raw.h)==0 and len(self.raw.p)==0 and len(self.raw.t)==0


  def _workingDataDiffersFromRaw(self:'Indentation') -> bool: # type: ignore[misc]
    """
    Check whether direct assignments on self have replaced the raw snapshot.
    """
    for name in ('h', 'p', 't', 'valid'):
      value = getattr(self, name)
      rawValue = getattr(self.raw, name)
      if not isinstance(value, np.ndarray) or not isinstance(rawValue, np.ndarray):
        continue
      if value.shape != rawValue.shape:
        return True
      if bool in (value.dtype, rawValue.dtype):
        if not np.array_equal(value, rawValue):
          return True
      elif not np.allclose(value, rawValue, equal_nan=True):
        return True
    if isinstance(self.slope, np.ndarray) and len(self.raw.slope)>0:
      if self.slope.shape != self.raw.slope.shape:
        return True
      if not np.allclose(self.slope, self.raw.slope, equal_nan=True):
        return True
    return False


  def _snapshotWorkingAsRaw(self:'Indentation', source:str='manual_self') -> None: # type: ignore[misc]
    """
    Store the current working arrays as raw data for manual/synthetic objects.
    """
    self.raw.h = self.h.copy()
    self.raw.p = self.p.copy()
    self.raw.t = self.t.copy()
    self.raw.valid = self.valid.copy()
    self.raw.slope = self.slope.copy()
    self.raw.phase = self.phase.copy()
    self.provenance = {
      'raw': {'state': 'manual_snapshot'},
      'working': {'state': 'raw'},
      'h': {'source': f'{source}_h', 'surface': False, 'drift': False, 'frameCompliance': False},
      'p': {'source': f'{source}_p', 'tare': False},
      'slope': {'source': f'{source}_slope', 'frameCompliance': False}
    }
    return


  def correctThermalDrift(self:'Indentation') -> None: # type: ignore[misc]
    """
    Apply configured thermal drift correction to working depth.
    """
    self.h -= _dictToFloat(self.model['driftRate'], 0.0) * self.t
    return


  def correctStiffness(self:'Indentation') -> None: # type: ignore[misc]
    """
    Apply frame compliance correction to working depth and CSM stiffness.
    """
    self.h -= self.tip.compliance * self.p
    if self.method == Method.CSM and len(self.slope)>0:
      self.slope = 1./(1./self.slope-self.tip.compliance)
    return


  def applySurfaceCorrection(self:'Indentation', surfaceIndex:int, usesValid:bool=False, tareLoad:bool=False) -> bool: # type: ignore[misc]
    """
    Apply the selected surface offset to the working arrays.
    """
    if surfaceIndex < 0:
      return True
    if usesValid:
      if surfaceIndex >= len(self.h[self.valid]):
        print('**ERROR** surface index out of bounds for valid data:', surfaceIndex)
        return False
      depthOffset = self.h[self.valid][surfaceIndex]
      loadOffset = self.p[self.valid][surfaceIndex]
    else:
      if surfaceIndex >= len(self.h):
        print('**ERROR** surface index out of bounds:', surfaceIndex)
        return False
      depthOffset = self.h[surfaceIndex]
      loadOffset = self.p[surfaceIndex]
    self.h -= depthOffset
    if tareLoad:
      self.p -= loadOffset
    return True


  def findAndApplySurfaceCorrection(self:'Indentation', plotSurface:bool=False) -> bool: # type: ignore[misc]
    """
    Find and apply surface correction on the current working arrays.
    """
    thresValue:float|None = None
    thresValues:np.ndarray|None = None
    surface = -1

    if self.testName in self.surface:
      surfaceConfig = self.surface[self.testName]
      if 'surfaceIdx' in surfaceConfig:
        return self.applySurfaceCorrection(int(surfaceConfig['surfaceIdx']))

    found = False
    if 'load' in self.surface:
      surfaceValue = self.surface['load']
      if isinstance(surfaceValue, (int, float)):
        thresValues = self.p.copy()
        thresValue  = float(surfaceValue)
        found = True
    elif 'stiffness' in self.surface:
      surfaceValue = self.surface['stiffness']
      if isinstance(surfaceValue, (int, float)):
        thresValues = self.slope.copy()
        thresValue  = float(surfaceValue)
        found = True
    elif 'phase angle' in self.surface:
      surfaceValue = self.surface['phase angle']
      if isinstance(surfaceValue, (int, float)):
        thresValues = self.phase.copy()
        thresValue  = float(surfaceValue)
        found = True
    elif 'abs(dp/dh)' in self.surface:
      surfaceValue = self.surface['abs(dp/dh)']
      if isinstance(surfaceValue, (int, float)):
        thresValues = np.abs(np.gradient(self.p,self.h))
        thresValue  = float(surfaceValue)
        found = True
    elif 'dp/dt' in self.surface:
      surfaceValue = self.surface['dp/dt']
      if isinstance(surfaceValue, (int, float)):
        thresValues = np.gradient(self.p,self.t)
        thresValue  = float(surfaceValue)
        found = True

    if found:
      if thresValues is None or thresValue is None:
        print('**ERROR** invalid surface threshold configuration')
        return False
      nans = np.isnan(thresValues)
      if np.any(nans):
        def tempX(z:np.ndarray) -> np.ndarray:
          return z.nonzero()[0]
        thresValues[nans]= np.interp(tempX(nans), tempX(~nans), thresValues[~nans])

      if 'median filter' in self.surface:
        thresValues = signal.medfilt(thresValues, self.surface['median filter']) # type: ignore[call-overload]
      elif 'gauss filter' in self.surface:
        thresValues = gaussian_filter1d(thresValues, self.surface['gauss filter']) # type: ignore[call-overload]
      elif 'butterfilter' in self.surface:
        valueB, valueA = signal.butter(*self.surface['butterfilter']) # type: ignore[call-overload]
        thresValues = signal.filtfilt(valueB, valueA, thresValues)
      if 'phase angle' in self.surface:
        surfaceMatches = np.where(thresValues<thresValue)[0]
      else:
        surfaceMatches = np.where(thresValues>thresValue)[0]
      if len(surfaceMatches)==0:
        print('**ERROR** could not identify surface for threshold', thresValue)
        return False

      # APPLY SURFACE CORRECTION AFTER IDENTIFICATION
      surface = int(surfaceMatches[0])
      if not self.applySurfaceCorrection(surface, usesValid=not 'load' in self.surface, tareLoad='tare load' in self.surface):
        return False

    if plotSurface or 'plot' in self.surface:
      _, ax1 = plt.subplots()
      if thresValues is None:
        ax1.plot(self.h,self.p, 'C0o-')
      elif 'load' in self.surface:
        ax1.plot(self.h,thresValues, 'C0o-')
        if surface >= 0:
          ax1.plot(self.h[surface], thresValues[surface], 'C9o', markersize=14)
      else:
        ax1.plot(self.h[self.valid],thresValues, 'C0o-')
        if surface >= 0:
          ax1.plot(self.h[self.valid][surface], thresValues[surface], 'C9o', markersize=14)
      ax1.axhline(0,linestyle='dashed')
      if thresValue is not None:
        ax1.set_ylim(bottom=0, top=thresValue*5)
      ax1.set_xlabel(r'depth [$\mu m$]')
      ax1.set_ylabel(r'threshold value [different units]', color='C0')
      ax1.grid()
      plt.show()
    return True

  def calcYoungsModulus(self:'Indentation', minDepth:float=-1, plot:bool=False) -> float: # type: ignore[misc]
    """
    Calculate and plot Young's modulus as a function of the depth |br|
    use corrected h and stiffness (do not recalculate)

    Args:
        minDepth (float): minimum depth for fitting horizontal; if negative: no line is fitted
        plot (bool): plot comparison this calculation to data read from file

    Returns:
        float: average Young's modulus, minDepth>0
    """
    self.modulusRed, self.Ac, self.hc = \
      self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid], _dictToFloat(self.model['nonMetal'], 1.0))
    modulus = np.asarray(self.YoungsModulus(self.modulusRed))
    eAve, eStd = -1.0, 0.0
    if minDepth>0:
      #eAve = np.average(       self.modulusRed[ self.h>minDepth ] )
      eAve = np.average( modulus[  np.bitwise_and(modulus>0, self.h[self.valid]>minDepth) ] )
      eStd = np.std(     modulus[  np.bitwise_and(modulus>0, self.h[self.valid]>minDepth) ] )
      print("Average and StandardDeviation of Young's Modulus",round(eAve,1) ,round(eStd,1) ,' [GPa]')
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


  def calcHardness(self:'Indentation', minDepth:float=-1, plot:bool=False) -> None: # type: ignore[misc]
    """
    Calculate and plot Hardness as a function of the depth

    Args:
        minDepth (float): minimum depth for fitting horizontal; if negative: no line is fitted
        plot (bool): plot comparison this calculation to data read from file
    """
    #use area function
    hardness=self.p[self.valid]/self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid], \
      _dictToFloat(self.model['nonMetal'], 1.0))[1]
    if plot:
      mark = '-' if len(hardness)>1 else 'o'
      plt.plot(self.h[self.valid], hardness, mark+'b', label='calc')
      if not self.hardness is None:
        plt.plot(self.h[self.valid], self.hardness, mark+'r', label='readFromFile')
      if minDepth>0:
        hardnessAve = np.average( hardness[  np.bitwise_and(hardness>0, self.h[self.valid]>minDepth) ] )
        hardnessStd = np.std(     hardness[  np.bitwise_and(hardness>0, self.h[self.valid]>minDepth) ] )
        print("Average and StandardDeviation of hardness",round(hardnessAve,1),round(hardnessStd,1) ,' [GPa]')
        plt.axhline(hardnessAve, color='b')
        plt.axhline(hardnessAve+hardnessStd, color='b', linestyle='dashed')
        plt.axhline(hardnessAve-hardnessStd, color='b', linestyle='dashed')
      plt.xlabel(r'depth [$\mathrm{\mu m}]$]')
      plt.ylabel(r'hardness [$\mathrm{GPa}$]')
      plt.legend(loc=0)
      plt.show()
    self.hardness = hardness
    return


  def calcStiffness2Force(self:'Indentation', minDepth:float=0.01, plot:bool=True, calibrate:bool=False) -> np.ndarray|None: # type: ignore[misc]
    """
    Calculate and plot stiffness squared over force as a function of the depth

    Args:
        minDepth (float): minimum depth for fitting line
        plot (bool): plot curve and slope
        calibrate (bool): calibrate additional stiffness and save value
    Returns:
        list: prefactors
    """
    compliance0:float = self.tip.compliance
    prefactors:np.ndarray|None = None

    def errorFunction(complianceArray:np.ndarray) -> float:
      compliance = float(complianceArray[0])
      stiffness   = 1./(1./self.sRaw-compliance) # type: ignore[attr-defined]
      stiffness2load = np.divide(np.multiply(stiffness,stiffness),self.p)
      h   = self.hRaw-compliance*self.p
      h_ = h[ h>minDepth ]
      stiffness2load  = stiffness2load[ h>minDepth ]
      if len(h_)>4:
        prefactors = np.polyfit(h_,stiffness2load,1)
        print(compliance,"Fit f(x)=",prefactors[0],"*x+",prefactors[1])
        return float(np.abs(prefactors[0]))
      print("*WARNING*: too short vector",len(h_))
      return 9999999.
    if calibrate:
      result = fmin_l_bfgs_b(errorFunction, np.array([compliance0], dtype=float), bounds=[(-0.1,0.1)], \
                              approx_grad=True, epsilon=0.000001, factr=1e11)
      print("  Best values   ",result[0], "\tOptimum residual:",np.round(result[1],3))
      print('  Number of function evaluations~size of globalData',result[2]['funcalls'])
      compliance0 = float(result[0][0])
      #self.correct_H_S()
    if plot:
      stiffness = 1./(1./self.sRaw-compliance0) # type: ignore[attr-defined]
      stiffness2load = np.divide(np.multiply(stiffness,stiffness),self.p)
      h   = self.hRaw-compliance0*self.p
      h_ = h[ h>minDepth ]
      prefactors = np.polyfit(h_, stiffness2load[ h>minDepth ],1)
      plt.plot(h,stiffness2load, 'b-')
      stiffness2loadFit = np.polyval(prefactors,h)
      plt.plot(h, stiffness2loadFit, 'r-', lw=3)
      plt.xlabel(r'depth [$\mathrm{\mu m}$]')
      plt.ylabel(r'stiffness2/load [$\mathrm{GPa}$]')
      plt.show()
    return prefactors


  def analyse(self:'Indentation') -> None: # type: ignore[misc]
    """
    update slopes/stiffness, Young's modulus and hardness after displacement correction by:

    - drift correction
    - compliance change

    The correction step is repeatable because it restores the loaded/prepared raw
    arrays before applying drift and compliance corrections.
    """
    if self._rawIsEmpty() or (not self._workingIsAnalysisResult() and len(self.iLHU)==0 and self._workingDataDiffersFromRaw()):
      # Backward compatibility for synthetic/manual objects that assign arrays
      # directly on self instead of going through an input reader.
      self._snapshotWorkingAsRaw()
    self._restoreRaw()
    self._setWorkingProvenance('analysed')
    self.correctThermalDrift()
    self.correctStiffness()
    if not self.findAndApplySurfaceCorrection():
      return
    try:
      if not self.identifyLoadHoldUnload():
        return
    except:
      print('**ERROR** could not identify load-hold-unload. Suggestion: try next test')
      print(traceback.format_exc())
      return

    if self.method == Method.CSM:
      if self.model['cropSlopeToLoading'] and len(self.iLHU)>0 and len(self.iLHU[0])>=2 and len(self.slope)==len(self.h[self.valid]):
        iSurface, iLoad = self.iLHU[0][0], self.iLHU[0][1]
        slopeFull = np.zeros_like(self.h)
        slopeFull[self.valid] = self.slope
        self.valid = np.zeros_like(self.h, dtype=bool)
        self.valid[iSurface:iLoad] = True
        self.slope = slopeFull[self.valid]
    else:
      unloadingSlope, unloadingValid, _, _ , _= self.stiffnessFromUnloading(self.p, self.h)
      if unloadingSlope is None or unloadingValid is None:
        self.slope = np.array([])
        self.valid = np.zeros_like(self.p, dtype=bool)
        return
      self.slope = np.array(unloadingSlope)
      self.valid = unloadingValid
    # verify in one location that the length of valid makes sense
    if len(self.slope) != len(self.h[self.valid]):
      print('**ERROR**: length of slope and valid do not match.')
      return
    try:
      self.k2p = self.slope*self.slope/self.p[self.valid]
    except:
      print('**ERROR**: could not calculate k2p. SKIP ANALYSE')
      print(traceback.format_exc())
      return
    #Calculate Young's modulus
    self.calcYoungsModulus()
    self.calcHardness()
    self.saveToUserMeta()
    return


  def identifyLoadHoldUnload(self:'Indentation', plot:bool=False) -> bool: # type: ignore[misc]
    """
    internal method: identify ALL load - hold - unload segments in data

    Args:
        plot (bool): verify by plotting

    Returns:
        bool: success of identifying the load-hold-unload
    """
    if self.method==Method.CSM:
      success = self.identifyLoadHoldUnloadCSM(plot)
      return success
    #use force-rate to identify load-hold-unload
    if self.model['relForceRateNoiseFilter']=='median':
      p = signal.medfilt(self.p, 5)
    else:
      p = gaussian_filter1d(self.p, 5)
    relForceRateNoise = _dictToFloat(self.model['relForceRateNoise'], 0.02)
    forceNoise        = _dictToFloat(self.model['forceNoise'],        0.001)
    rate = np.gradient(p, self.t)
    rate /= np.max(rate)
    loadMask  = np.logical_and(rate >  relForceRateNoise, p>forceNoise)
    unloadMask= np.logical_and(rate < -relForceRateNoise, p>forceNoise)
    if plot:     # verify visually
      plt.plot(rate)
      plt.axhline(0, c='k')
      plt.axhline( relForceRateNoise, c='k', linestyle='dashed')
      plt.axhline(-relForceRateNoise, c='k', linestyle='dashed')
      if plot:
        plt.ylim([-8*relForceRateNoise, 8*relForceRateNoise])
      plt.xlabel('time incr. []')
      plt.ylabel(r'rate [$\mathrm{mN/sec}$]')
      plt.title('Identify load, hold, unload: loading and unloading segments - prior to cleaning')
      plt.show()
    #try to clean small fluctuations
    loadMaskTry = loadMask
    unloadMaskTry = unloadMask
    if len(loadMask)>100 and len(unloadMask)>100:
      size = int(_dictToFloat(self.model['maxSizeFluctuations'], 10.0))
      structure = np.ones((size,), dtype=bool)
      loadMaskTry = ndimage.binary_closing(loadMask,        structure=structure)
      unloadMaskTry = ndimage.binary_closing(unloadMask,    structure=structure)
      loadMaskTry = ndimage.binary_opening(loadMaskTry,     structure=structure)
      unloadMaskTry = ndimage.binary_opening(unloadMaskTry, structure=structure)
    if np.any(loadMaskTry) and np.any(unloadMaskTry):
      loadMask = loadMaskTry
      unloadMask = unloadMaskTry
    # verify visually
    if plot or self.output['plotLoadHoldUnload']:
      if self.output['ax'] is None:
        fig, ax = plt.subplots(2,1, sharex=True, gridspec_kw={'hspace':0})
      else:
        ax = self.output['ax']
      ax[0].plot(rate)
      ax[0].axhline(0, c='k')
      x_ = np.arange(len(rate))[loadMask]
      y_ = np.zeros_like(rate)[loadMask]
      ax[0].plot(x_, y_, 'C1.', label='load mask')
      x_ = np.arange(len(rate))[unloadMask]
      y_ = np.zeros_like(rate)[unloadMask]
      ax[0].plot(x_, y_, 'C2.', label='unload mask')
      ax[0].axhline( relForceRateNoise, c='k', linestyle='dashed')
      ax[0].axhline(-relForceRateNoise, c='k', linestyle='dashed')
      ax[0].set_ylim([-8*relForceRateNoise, 8*relForceRateNoise])
      ax[0].legend()
      ax[0].set_ylabel(r'rate [$\mathrm{mN/sec}$]')
    #find index where masks are changing from true-false
    loadMask  = np.r_[False,loadMask,False] #pad with false on both sides
    unloadMask= np.r_[False,unloadMask,False]
    loadIdx   = np.flatnonzero(loadMask[1:]   != loadMask[:-1])
    unloadIdx = np.flatnonzero(unloadMask[1:] != unloadMask[:-1])
    if len(unloadIdx) == len(loadIdx)+2 and np.all(unloadIdx[-4:]>loadIdx[-1]):
      #for drift: partial unload-hold-full unload
      unloadIdx = unloadIdx[:-2]
    while len(loadIdx)>2 and len(unloadIdx)>0 and len(unloadIdx) < len(loadIdx) and loadIdx[2]<unloadIdx[0]:
      #clean loading front
      loadIdx = loadIdx[2:]

    if plot or self.output['plotLoadHoldUnload']:     # verify visually
      ax[1].plot(self.p,'o')
      ax[1].plot(p, 's')
      ax[1].plot(loadIdx[::2],  self.p[loadIdx[::2]],  'o',label='load',markersize=12)
      ax[1].plot(loadIdx[1::2], self.p[loadIdx[1::2]], 'o',label='hold',markersize=10)
      ax[1].plot(unloadIdx[::2],self.p[unloadIdx[::2]],'o',label='unload',markersize=8)
      try:
        ax[1].plot(unloadIdx[1::2],self.p[unloadIdx[1::2]],'o',label='unload-end',markersize=6)
      except IndexError:
        pass
      ax[1].legend(loc=0)
      ax[1].set_xlabel(r'time incr. []')
      ax[1].set_ylabel(r'force [$\mathrm{mN}$]')
      fig.tight_layout()
      if self.output['ax'] is None:
        plt.show()
    #store them in a list [[loadStart1, loadEnd1, unloadStart1, unloadEnd1], [loadStart2, loadEnd2, unloadStart2, unloadEnd2],.. ]
    self.iLHU = []
    if len(loadIdx) != len(unloadIdx):
      print("**ERROR** Load-Hold-Unload identification did not work",loadIdx, unloadIdx  )
    else:
      self.output['successTest'].append(self.testName)
    try:
      for i,_ in enumerate(loadIdx[::2]):
        if loadIdx[::2][i] < loadIdx[1::2][i] <= unloadIdx[::2][i] < unloadIdx[1::2][i]:
          newEntry = [loadIdx[::2][i],loadIdx[1::2][i],unloadIdx[::2][i],unloadIdx[1::2][i]]
          if np.min(newEntry)>0 and np.max(newEntry)<len(self.h):
            self.iLHU.append(newEntry)
          else:
            print("**ERROR** iLHU values out of bounds", newEntry,' with length',len(self.h))
            if len(self.iLHU)>0:
              self.iLHU.append([])
        else:
          print("**ERROR** some segment not found", loadIdx[::2][i], loadIdx[1::2][i], unloadIdx[::2][i], unloadIdx[1::2][i])
          if len(self.iLHU)>0:
            self.iLHU.append([])
    except:
      print("**ERROR** load-unload-segment not found")
      self.iLHU = []
    if len(self.iLHU)>1:
      self.method=Method.MULTI
    #drift segments: only add if it makes sense
    try:
      iDriftS = unloadIdx[1::2][-1]+1
      iDriftE = len(self.p)-1
      if iDriftS+1>iDriftE:
        iDriftS=iDriftE-1
      self.iDrift = [iDriftS,iDriftE]
    except:
      self.iDrift = [-1,-1]
    return True


  def identifyLoadHoldUnloadCSM(self:'Indentation', plot:bool=False) -> bool: # type: ignore[misc]
    """
    internal method: identify load - hold - unload segment in CSM data |br|
    Backup: if identifyLoadHoldUnload fails

    Args:
      plot (bool): plot values

    Returns:
      bool: success of identifying hold-load-unload sequence
    """
    iSurface = int(np.min(np.where( self.h>=0                     )))
    unloadPMax = _dictToFloat(self.model['unloadPMax'], 0.99)
    iLoad    = int(np.min(np.where( self.p-np.max(self.p)*unloadPMax>0 )))
    if iLoad<len(self.p)-1:
      iHold  = int(np.max(np.where( self.p-np.max(self.p)*unloadPMax>0 )))
      if iHold==iLoad:
        iHold += 1
      try:
        hist,bins= np.histogram( self.p[iHold:] , bins=1000)
      except:
        print('**ERROR** identifyLoadHoldUnloadCSM: 1')
        self.iLHU = []
        self.iDrift = []
        return False
      pDrift   = bins[np.argmax(hist)+1]
      pCloseToDrift = np.logical_and(self.p>pDrift*unloadPMax, self.p<pDrift/unloadPMax)
      pCloseToDrift[:iHold] = False
      if len(pCloseToDrift[pCloseToDrift])>3:
        iDriftS  = int(np.min(np.where( pCloseToDrift )))
        iDriftE  = int(np.max(np.where( pCloseToDrift )))
      else:
        iDriftS   = len(self.p)-2
        iDriftE   = len(self.p)-1
      if not iSurface < iLoad < iHold < iDriftS < iDriftE < len(self.h):
        if self.output['verbose']>1:
          print("Warning: identifyLoadHoldUnloadCSM could not identify load-hold-unloading cycle. Only loading?")
          print(iSurface,iLoad,iHold,iDriftS,iDriftE, len(self.h))
        iLoad     = len(self.p)-4
        iHold     = len(self.p)-3
        iDriftS   = len(self.p)-2
        iDriftE   = len(self.p)-1
    else:  #This part is required
      if self.method != Method.CSM:
        print("*WARNING*: no hold or unloading segments in data")
      iHold     = len(self.p)-3
      iDriftS   = len(self.p)-2
      iDriftE   = len(self.p)-1
    self.iLHU   = [[iSurface,iLoad,iHold,iDriftS]]
    self.iDrift = [iDriftS,iDriftE]

    if plot or self.output['plotLoadHoldUnload']:
      plt.plot(self.h, self.p)
      plt.plot(self.h[iSurface], self.p[iSurface], 'o', markersize=10, label='surface')
      plt.plot(self.h[iLoad], self.p[iLoad], 'o', markersize=10, label='load')
      plt.plot(self.h[iHold], self.p[iHold], 'o', markersize=10, label='hold')
      plt.plot(self.h[iDriftS], self.p[iDriftS], 'o', markersize=10, label='drift start')
      plt.plot(self.h[iDriftE], self.p[iDriftE], 'o', markersize=10, label='drift end')
      plt.legend(loc=0)
      plt.title('Identify Load, Hold, Unload for CSM measurements')
      plt.show()
    return True


  def nextTest(self:'Indentation', newTest:bool=True, plotSurface:bool=False) -> bool: # type: ignore[misc]
    """
    Wrapper for all next test for all vendors

    Args:
      newTest (bool): go to next test; false=redo this one
      plotSurface (bool): plot surface area

    Returns:
      bool: success of going to next sheet
    """
    if newTest:
      if self.vendor == Vendor.Agilent:
        success = self.nextAgilentTest(newTest)
      elif self.vendor == Vendor.Micromaterials:
        success = self.nextMicromaterialsTest()
      elif self.vendor == Vendor.FischerScope:
        success = self.nextFischerScopeTest()
      elif self.vendor > Vendor.Hdf5:
        success = self.nextHDF5Test()
      else:
        print("No multiple tests in file")
        success = False
    else:
      success = True
    if not success:
      return success

    if self._rawIsEmpty() or (not self._workingIsAnalysisResult() and len(self.iLHU)==0 and self._workingDataDiffersFromRaw()):
      self._snapshotWorkingAsRaw()
    self._restoreRaw()
    if not newTest:
      self.iLHU = []
      self.iDrift = [-1,-1]
      for name in ('k2p', 'hc', 'Ac', 'modulus', 'modulusRed', 'hardness'):
        setattr(self, name, np.array([], dtype=float))
    if plotSurface or 'plot' in self.surface:
      print('Run analyse() to show the full data.')
    return success


  def saveToUserMeta(self:'Indentation') -> None: # type: ignore[misc]
    """
    save results to user-metadata
    """
    if self.method == Method.CSM:
      if len(self.slope)>0:
        i = -1 # only last value is saved
        meta = {"S_mN/um":[self.slope[i]], "hMax_um":[self.h[self.valid][i]], "pMax_mN":[self.p[self.valid][i]],\
                "modulusRed_GPa":[self.modulusRed[i]], "A_um2":[self.Ac[i]], "hc_um":[self.hc[i]],\
                "E_GPa":[self.modulus[i]],"H_GPa":[self.hardness[i]],"segment":[str(i+1)] }
      else:
        meta = {}
    else:
      segments = [str(i+1) for i in range(len(self.slope))]
      meta = {"S_mN/um":list(self.slope), "hMax_um":list(self.h[self.valid]), \
              "pMax_mN":list(self.p[self.valid]),"modulusRed_GPa":list(self.modulusRed),"A_um2":list(self.Ac),\
              "hc_um":list(self.hc), "E_GPa":list(self.modulus),"H_GPa":list(self.hardness),"segment":segments}
    self.metaUser.update(meta)
    self.metaUser['code'] = __file__.rsplit('/', maxsplit=1)[-1]
    return
