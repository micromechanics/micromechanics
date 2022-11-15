"""Most central functions for nanoindentation"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import scipy.signal as signal
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import fmin_l_bfgs_b
from .definitions import Vendor, Method


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
  self.modulusRed, self.Ac, self.hc = \
    self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid])
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
  #use area function
  hardness=self.p[self.valid]/self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid])[1]
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
    stiffness   = 1./(1./self.sRaw-compliance)
    stiffness2load = np.divide(np.multiply(stiffness,stiffness),self.p)
    h   = self.hRaw-compliance*self.p
    h_ = h[ h>minDepth ]
    stiffness2load  = stiffness2load[ h>minDepth ]
    if len(h_)>4:
      prefactors = np.polyfit(h_,stiffness2load,1)
      print(compliance,"Fit f(x)=",prefactors[0],"*x+",prefactors[1])
      return np.abs(prefactors[0])
    print("*WARNING*: too short vector",len(h_))
    return 9999999.
  if calibrate:
    result = fmin_l_bfgs_b(errorFunction, compliance0, bounds=[(-0.1,0.1)], \
                            approx_grad=True, epsilon=0.000001, factr=1e11)
    print("  Best values   ",result[0], "\tOptimum residual:",np.round(result[1],3))
    print('  Number of function evaluations~size of globalData',result[2]['funcalls'])
    compliance0 = result[0]
    #self.correct_H_S()
  if plot:
    stiffness = 1./(1./self.sRaw-compliance0)
    #vy: AttributeError: 'Indentation' object has no attribute 'sRaw'
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


def analyse(self):
  """
  update slopes/stiffness, Young's modulus and hardness after displacement correction by:

  - compliance change

  ONLY DO ONCE AFTER LOADING FILE: if this causes issues introduce flag analysed
    which is toggled during loading and analysing
  """
  self.h -= self.tip.compliance*self.p
  if self.method == Method.CSM:
    self.slope = 1./(1./self.slope-self.tip.compliance)
  else:
    self.slope, self.valid, _, _ , _= self.stiffnessFromUnloading(self.p, self.h)
    self.slope = np.array(self.slope)
  try:
    self.k2p = self.slope*self.slope/self.p[self.valid]
  except:
    print('**WARNING SKIP ANALYSE')
    return
  #Calculate Young's modulus
  self.calcYoungsModulus()
  self.calcHardness()
  self.saveToUserMeta()
  return


def identifyLoadHoldUnload(self,plot=False):
  """
  internal method: identify ALL load - hold - unload segments in data

  Args:
      plot: verify by plotting
  """
  if self.method==Method.CSM:
    self.identifyLoadHoldUnloadCSM()
    return False
  #identify point in time, which are too close (~0) to eachother
  gradTime = np.diff(self.t)
  maskTooClose = gradTime < np.percentile(gradTime,80)/1.e3
  self.t     = self.t[1:][~maskTooClose]
  self.p     = self.p[1:][~maskTooClose]
  self.h     = self.h[1:][~maskTooClose]
  self.valid = self.valid[1:][~maskTooClose]
  #use force-rate to identify load-hold-unload
  if self.zeroGradFilter=='median':
    p = signal.medfilt(self.p, 5)
  else:
    p = gaussian_filter1d(self.p, 5)
  rate = np.gradient(p, self.t)
  rate /= np.max(rate)
  loadMask  = rate >  self.zeroGradDelta
  unloadMask= rate < -self.zeroGradDelta
  if plot:     # verify visually
    plt.plot(rate)
    plt.axhline(0, c='k')
    plt.axhline( self.zeroGradDelta, c='k', linestyle='dashed')
    plt.axhline(-self.zeroGradDelta, c='k', linestyle='dashed')
    plt.ylim([-8*self.zeroGradDelta, 8*self.zeroGradDelta])
    plt.xlabel('time incr. []')
    plt.ylabel(r'rate [$\mathrm{mN/sec}$]')
    plt.show()
  #clean small fluctuations
  if len(loadMask)>100 and len(unloadMask)>100:
    size = 10
    loadMask = ndimage.binary_closing(loadMask, structure=np.ones((size,)) )
    unloadMask = ndimage.binary_closing(unloadMask, structure=np.ones((size,)))
    loadMask = ndimage.binary_opening(loadMask, structure=np.ones((size,)))
    unloadMask = ndimage.binary_opening(unloadMask, structure=np.ones((size,)))
  #find index where masks are changing from true-false
  loadMask  = np.r_[False,loadMask,False] #pad with false on both sides
  unloadMask= np.r_[False,unloadMask,False]
  loadIdx   = np.flatnonzero(loadMask[1:]   != loadMask[:-1])
  unloadIdx = np.flatnonzero(unloadMask[1:] != unloadMask[:-1])
  if len(unloadIdx) == len(loadIdx)+2 and np.all(unloadIdx[-4:]>loadIdx[-1]):
    #for drift: partial unload-hold-full unload
    unloadIdx = unloadIdx[:-2]
  while len(unloadIdx) < len(loadIdx) and loadIdx[2]<unloadIdx[0]:
    #clean loading front
    loadIdx = loadIdx[2:]

  if plot:     # verify visually
    plt.plot(self.p,'o')
    plt.plot(loadIdx[::2],  self.p[loadIdx[::2]],  'o',label='load',markersize=12)
    plt.plot(loadIdx[1::2], self.p[loadIdx[1::2]], 'o',label='hold',markersize=10)
    plt.plot(unloadIdx[::2],self.p[unloadIdx[::2]],'o',label='unload',markersize=8)
    try:
      plt.plot(unloadIdx[1::2],self.p[unloadIdx[1::2]],'o',label='unload-end',markersize=6)
    except IndexError:
      pass
    plt.legend(loc=0)
    plt.xlabel(r'time incr. []')
    plt.ylabel(r'force [$\mathrm{mN}$]')
    plt.show()
  #store them in a list [[loadStart1, loadEnd1, unloadStart1, unloadEnd1], [loadStart2, loadEnd2, unloadStart2, unloadEnd2],.. ]
  self.iLHU = []
  if len(loadIdx) != len(unloadIdx):
    print("**ERROR: Load-Hold-Unload identification did not work",loadIdx, unloadIdx  )
  try:
    for i,_ in enumerate(loadIdx[::2]):
      if loadIdx[::2][i] < loadIdx[1::2][i] <= unloadIdx[::2][i] < unloadIdx[1::2][i]:
        self.iLHU.append([loadIdx[::2][i],loadIdx[1::2][i],unloadIdx[::2][i],unloadIdx[1::2][i]])
      else:
        print("**ERROR: some segment not found", loadIdx[::2][i], loadIdx[1::2][i], unloadIdx[::2][i], unloadIdx[1::2][i])
        if len(self.iLHU)>0:
          self.iLHU.append([])
  except:
    print("**ERROR: load-unload-segment not found")
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


def identifyLoadHoldUnloadCSM(self, plot=False):
  """
  internal method: identify load - hold - unload segment in CSM data

  Backup: if identifyLoadHoldUnload fails

  Args:
    plot: plot values
  """
  iSurface = np.min(np.where( self.h>=0                     ))
  iLoad    = np.min(np.where( self.p-np.max(self.p)*self.unloadPMax>0 ))
  if iLoad<len(self.p)-1:
    iHold    = np.max(np.where( self.p-np.max(self.p)*self.unloadPMax>0 ))
    if iHold==iLoad:
      iHold += 1
    try:
      hist,bins= np.histogram( self.p[iHold:] , bins=1000)
    except:
      print('**ERROR identifyLoadHoldUnloadCSM: 1')
      self.iLHU = []
      self.iDrift = []
      return
    pDrift   = bins[np.argmax(hist)+1]
    pCloseToDrift = np.logical_and(self.p>pDrift*self.unloadPMax,self.p<pDrift/self.unloadPMax)
    pCloseToDrift[:iHold] = False
    if len(pCloseToDrift[pCloseToDrift])>3:
      iDriftS  = np.min(np.where( pCloseToDrift ))
      iDriftE  = np.max(np.where( pCloseToDrift ))
    else:
      iDriftS   = len(self.p)-2
      iDriftE   = len(self.p)-1
    if not iSurface < iLoad < iHold < iDriftS < iDriftE < len(self.h):
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

  if plot:
    plt.plot(self.h, self.p)
    plt.plot(self.h[iSurface], self.p[iSurface], 'o', markersize=10, label='surface')
    plt.plot(self.h[iLoad], self.p[iLoad], 'o', markersize=10, label='load')
    plt.plot(self.h[iHold], self.p[iHold], 'o', markersize=10, label='hold')
    plt.plot(self.h[iDriftS], self.p[iDriftS], 'o', markersize=10, label='drift start')
    plt.plot(self.h[iDriftE], self.p[iDriftE], 'o', markersize=10, label='drift end')
    plt.legend(loc=0)
    plt.show()
  return


def nextTest(self, newTest=True, plotSurface=False):
  """
  Wrapper for all next test for all vendors
  """
  if newTest:
    if self.vendor == Vendor.Agilent:
      success = self.nextAgilentTest(newTest)
    elif self.vendor == Vendor.Micromaterials:
      success = self.nextMicromaterialsTest()
    elif self.vendor == Vendor.FischerScope:
      success = self.nextFischerScopeTest()
    elif self.vendor == Vendor.CommonHDF5:
      success = self.nextHDF5Test()
    else:
      print("No multiple tests in file")
      success = False
  else:
    success = True

  #SURFACE FIND
  if self.testName in self.config and 'surfaceIdx' in self.config[self.testName]:
    surface = self.config[self.testName]['surfaceIdx']
    self.h -= self.h[surface]  #only change surface, not force
  else:
    found = False
    if 'load' in self.surfaceFind:
      thresValues = self.p
      thresValue  = self.surfaceFind['load']
      found = True
    elif 'stiffness' in self.surfaceFind:
      thresValues = self.slope
      thresValue  = self.surfaceFind['stiffness']
      found = True
    elif 'phase angle' in self.surfaceFind:
      thresValues = self.phase
      thresValue  = self.surfaceFind['phase angle']
      found = True
    elif 'abs(dp/dh)' in self.surfaceFind:
      thresValues = np.abs(np.gradient(self.p,self.h))
      thresValue  = self.surfaceFind['abs(dp/dh)']
      found = True
    elif 'dp/dt' in self.surfaceFind:
      thresValues = np.gradient(self.p,self.t)
      thresValue  = self.surfaceFind['dp/dt']
      found = True

    if found:
      #interpolate nan with neighboring values
      nans, tempX = np.isnan(thresValues), lambda z: z.nonzero()[0]
      thresValues[nans]= np.interp(tempX(nans), tempX(~nans), thresValues[~nans])

      #filter this data
      if 'median filter' in self.surfaceFind:
        thresValues = signal.medfilt(thresValues, self.surfaceFind['median filter'])
      elif 'gauss filter' in self.surfaceFind:
        thresValues = gaussian_filter1d(thresValues, self.surfaceFind['gauss filter'])
      elif 'butterfilter' in self.surfaceFind:
        valueB, valueA = signal.butter(*self.surfaceFind['butterfilter'])
        thresValues = signal.filtfilt(valueB, valueA, thresValues)
      if 'phase angle' in self.surfaceFind:
        surface  = np.where(thresValues<thresValue)[0][0]
      else:
        surface  = np.where(thresValues>thresValue)[0][0]
      if plotSurface or 'plot' in self.surfaceFind:
        _, ax1 = plt.subplots()
        ax1.plot(self.h,thresValues, 'C0o-')
        ax1.plot(self.h[surface], thresValues[surface], 'C9o', markersize=14)
        ax1.axhline(0,linestyle='dashed')
        ax1.set_ylim(bottom=0, top=np.percentile(thresValues,80))
        ax1.set_xlabel(r'depth [$\mu m$]')
        ax1.set_ylabel(r'gradient [mN]', color='C0')
        ax1.grid()
        plt.show()
      self.h -= self.h[surface]  #only change surface, not force
  return success


def saveToUserMeta(self):
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
  self.metaUser['code'] = __file__.split('/')[-1]
  return
