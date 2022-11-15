"""Plotting of nanoindentation data"""
import numpy as np
import matplotlib.pyplot as plt
from .definitions import Method
#import definitions

def plotTestingMethod(self, saveFig=False, show=True, double=False):
  """
  plot testing method

  Args:
    saveFig: save plot to file [use known filename plus extension png]
    show: show figure, else do not show
    double: show also stiffness and phase an function of time
  """
  if double:
    _, [ax1, ax2] = plt.subplots(2, sharex=True, figsize=(6,6))
  else:
    _, ax1, = plt.subplots()
  ax1b = ax1.twinx()
  ax1.plot(self.t, self.p,'C0')
  ax1b.plot(self.t, self.h,'C1')
  for mask in self.iLHU:
    ax1.plot(self.t[mask][0], self.p[mask][0], 'C0s')
    ax1.plot(self.t[mask][1], self.p[mask][1], 'C0x')
    ax1.plot(self.t[mask][2], self.p[mask][2], 'C0+')
    ax1.plot(self.t[mask][3], self.p[mask][3], 'C0o')
  ax1.plot(self.t[self.iDrift], self.p[self.iDrift], 'k.')
  ax1.axhline(0,color='C0', linestyle='dashed')
  ax1b.axhline(0,color='C1', linestyle='dashed')
  ax1.set_xlabel(r"time [$\mathrm{s}$]")
  ax1b.set_ylabel(r"depth [$\mathrm{\mu m}$]", color='C1', fontsize=14)
  ax1.set_ylabel(r"force [$\mathrm{mN}$]", color='C0', fontsize=14)
  if double:
    ax2b = ax2.twinx()
    ax2.plot(self.t[self.valid], self.slope,'C0')
    ax2b.plot(self.t[self.valid], self.phase,'C1')
    ax2.set_xlabel(r"time [$\mathrm{s}$]")
    ax2b.set_ylabel(r"phase [$\mathrm{rad}$]", color='C1', fontsize=14)
    ax2.set_ylabel(r"stiffness [$\mathrm{mN/\mu m}$]", color='C0', fontsize=14)
  plt.grid()
  plt.subplots_adjust(hspace=0)
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
    print("Stiffness:"+str(round(self.slope[0],1))     +"mN/um   "+\
      "hMax:"+str(round(self.h[self.valid][0],4))+"um    pMax:"+str(round(self.p[self.valid][0],2))+"mN")
    print("E*:       "+str(round(self.modulusRed[0],1))+"GPa     "+\
      "A:   "+str(round(self.Ac[0],4))+          "um2    hc: "+str(round(self.hc[0],4))+"um")
    print("E:        "+str(round(self.modulus[0],1))   +"GPa     "+\
      "H:   "+str(round(self.hardness[0],1))+     "GPa")
  _, ax = plt.subplots()
  ax.axhline(0,ls="dashed",c='k')
  ax.axvline(0,ls="dashed",c='k')
  ax.plot(self.h,self.p)
  if self.method != Method.CSM:
    _, _, maskUnload, optPar, _ = self.stiffnessFromUnloading(self.p, self.h)
    h_, p_ = self.h[maskUnload], self.p[maskUnload]
    if maskUnload is not None:
      ax.plot(self.h[maskUnload], self.unloadingPowerFunc(self.h[maskUnload],*optPar),\
        'C1', label='fit powerlaw')
    ax.plot(self.h[self.valid],self.p[self.valid],"or",label="max", markersize=10)
    ax.plot(self.hc, np.zeros_like(self.hc),"ob", label="hc", markersize=10)
    if len(self.hc)<2:
      ax.plot(h_[0],p_[0],'og',)
      ax.plot(h_[-1],p_[-1],'og', label="fit domain")
      h_ = np.linspace(self.hc,self.h[self.valid],10)
      if self.evaluateStiffnessAtMax:
        stiffnessLineInterceptY = self.p[self.valid]-self.slope*self.h[self.valid]
      else:
        stiffnessLineInterceptY = self.p[maskUnload][0]-self.slope*self.h[maskUnload][0]
      ax.plot(h_,   self.slope*h_+stiffnessLineInterceptY, 'r--', lw=2, label='stiffness')
    ax.legend(loc=0, numpoints=1)
  else:
    ax.plot(self.h[self.iLHU[0]],self.p[self.iLHU[0]],"or",label="specific", markersize=10)
  ax.set_xlim(left=-0.03)
  ax.set_xlabel(r"depth [$\mathrm{\mu m}$]")
  ax.set_ylabel(r"force [$\mathrm{mN}$]")
  if saveFig:
    plt.savefig(self.fileName.split('.')[0]+".png", dpi=150, bbox_inches='tight')
  if isinstance(show,bool):
    if show:
      plt.show()
  elif isinstance(show,int):
    plt.show(block = False)
    plt.pause(show)
    plt.close()
  return ax


def plotAll(self, saveFig=False, show=True):
  """
  Plot force-depth curves of all tests in the file

  Args:
    saveFig: save plot to file [use known filename plus extension png]
    show: show figure, else do not show
  """
  _, ax = plt.subplots()
  ax.axhline(0,ls="dashed",c='k')
  ax.axvline(0,ls="dashed",c='k')
  for testName in self:
    ax.plot(self.h,self.p, label=testName)
  plt.legend()
  ax.set_xlim(left=-0.03)
  ax.set_xlabel(r"depth [$\mathrm{\mu m}$]")
  ax.set_ylabel(r"force [$\mathrm{mN}$]")
  if saveFig:
    plt.savefig(self.fileName.split('.')[0]+".png", dpi=150, bbox_inches='tight')
  if isinstance(show,bool):
    if show:
      plt.show()
  elif isinstance(show,int):
    plt.show(block = False)
    plt.pause(show)
    plt.close()
  return ax




def plotAsDepth(self, entity, hvline=None):
  """
  Plot as function of depth either Young's modulus, hardness,
  stiffnessSquaredForce, ContactDepth, Contact Area, reducedModulus

  Makes only sense for CSM measurements

  Args:
    entity: what to plot on y-axis [E,H,K,K2P,hc,Ac,modulusRed]
  """
  if not isinstance(entity, str):
    print("**ERROR plotAsDepth: entity=[E,H,K,K2P,hc,Ac,modulusRed]")
    return
  if hvline is not None:
    plt.axhline(hvline, c='k')
  if   entity == "E":
    plt.plot(self.h[self.valid], self.modulus, "o")
    plt.ylabel("Young's modulus [GPa]")
  elif entity == "modulusRed":
    plt.plot(self.h[self.valid], self.modulusRed, "o")
    plt.ylabel("reduced Young's modulus [GPa]")
  elif entity == "H":
    plt.plot(self.h[self.valid], self.hardness, "o")
    plt.ylabel("Hardness [GPa]")
  elif entity == "K":
    plt.plot(self.h[self.valid], self.slope, "o")
    plt.ylabel("Stiffness [kN/m]")
  elif entity == "K2P":
    if not hasattr(self, 'k2p'):
      self.k2p = np.array(self.slope)*np.array(self.slope)/np.array(self.p[self.valid])
    plt.plot(self.h[self.valid], self.k2p, "C0o")
    mask = self.h[self.valid]>0.1
    fit = np.polyfit(self.h[self.valid][mask], self.k2p[mask],1)
    print('Fit: K2P='+str(round(fit[1]))+'+ '+str(round(fit[0]))+'*h')
    plt.plot(self.h[self.valid], np.polyval(fit,self.h[self.valid]), 'C1-')
    plt.axvline(0.1, linestyle='dashed',color='C1')
    plt.ylabel(r"Stiffness Squared Over Load [$\mathrm{GPa}$]")
  elif entity == "hc":
    plt.plot(self.h[self.valid], self.hc, "o")
    plt.ylabel(r"Contact depth [$\mathrm{\mu m}$]")
  elif entity == "Ac":
    plt.plot(self.h[self.valid], self.Ac, "o")
    plt.ylabel(r"Contact area [$\mathrm{\mu m^2}$]")
  else:
    print("Unknown entity")
    return
  plt.xlabel(r"depth "+r'[$\mathrm{\mu m}$]')
  plt.show()
  return
