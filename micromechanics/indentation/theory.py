"""CONVENTIONAL NANOINDENTATION FUNCTIONS: area, E,."""
from typing import TYPE_CHECKING
import math
import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
from .definitions import Method

if TYPE_CHECKING:
  from .core import Indentation

UnloadingFitResult = tuple[list[float], np.ndarray, np.ndarray|None, np.ndarray|tuple[float, float, float]|None, list[bool]]
UnloadingFitError = tuple[None, None, None, None, None]

def _dictToFloat(value:object, fallback:float) -> float:
  if isinstance(value, bool):
    return fallback
  if isinstance(value, int|float):
    return float(value)
  return fallback

class IndentationTheoryMixin:
  """
  Contact mechanics and fitting methods for :class:`Indentation`.
  """

  def YoungsModulus(self:'Indentation', modulusRed:float|np.ndarray, nuThis:float=-1) -> float|np.ndarray:# type: ignore[misc]
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
    nuTip      = _dictToFloat(self.model['nuTip'],      0.07)
    modulusTip = _dictToFloat(self.model['modulusTip'], 1140.0)
    modulus = (1.0-nu*nu) / ( 1.0/modulusRed - (1.0-nuTip**2)/modulusTip)
    return modulus


  def ReducedModulus(self:'Indentation', modulus:float|np.ndarray, nuThis:float=-1) -> float|np.ndarray:# type: ignore[misc]
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
    nuTip      = _dictToFloat(self.model['nuTip'],      0.07)
    modulusTip = _dictToFloat(self.model['modulusTip'], 1140.0)
    modulusRed =  1.0/(  (1.0-nu*nu)/modulus + (1.0-nuTip**2)/modulusTip)
    return modulusRed


  def OliverPharrMethod(self:'Indentation', stiffness:np.ndarray, pMax:np.ndarray, h:np.ndarray, nonMetal:float=1.) -> list[np.ndarray]:# type: ignore[misc]
    """
    Conventional Oliver-Pharr indentation method to calculate reduced Modulus modulusRed

    The following equations are used in that order:

    - hc = h-beta pMax/stiffness
    - Ac = hc(prefactors)
    - stiffness = 2/sqrt(pi) sqrt(Ac) modulusRed
    - Ac the contact area, hc the contact depth

    Args:
        stiffness (float): stiffness = slope dP/dh
        pMax (float): maximal force
        h (float): total penetration depth
        nonMetal (float): ability to change between metal=0 and nonMetal=1

    Returns:
        list: modulusRed, Ac, hc
    """
    threshAc = 1.e-12  #units in um: threshold = 1pm^2
    beta = _dictToFloat(self.model['beta'], 0.75)
    hc = h - nonMetal*beta*pMax/stiffness
    Ac   = self.tip.areaFunction(hc)
    Ac[Ac< threshAc] = threshAc  # prevent zero or negative area that might lock sqrt
    modulus   = stiffness / (2.0*np.sqrt(Ac)/np.sqrt(np.pi))
    return [modulus, Ac, hc]


  def inverseOliverPharrMethod(self:'Indentation', stiffness:np.ndarray, pMax:np.ndarray, modulusRed:np.ndarray, nonMetal:float=1.) -> np.ndarray:# type: ignore[misc]
    """
    Inverse Oliver-Pharr indentation method to calculate contact area Ac

    - equations and variable definitions given above; order in reverse order
    - only used for verification of the Oliver-Pharr Method

    Args:
        stiffness (float): slope dP/dh at the maximum load pMax
        pMax (float): maximal force
        modulusRed (float): modulusRed
        nonMetal (float): ability to change between metal=0 and nonMetal=1

    Returns:
        float: h penetration depth
    """
    Ac = np.power(stiffness / (2.0*modulusRed/np.sqrt(np.pi)), 2)
    hc0 = np.sqrt(Ac / 24.494)           # first guess: perfect Berkovich
    hc = self.tip.areaFunctionInverse(Ac, hc0=hc0)
    beta = _dictToFloat(self.model['beta'], 0.75)
    h = hc + nonMetal*beta*pMax/stiffness
    return h.flatten()


  @staticmethod
  def unloadingPowerFunc(h:np.ndarray, B:float, hf:float, m:float) -> np.ndarray:
    """
    internal function describing the unloading regime

    - function: p = B*(h-hf)^m
    - B:  scaling factor (no physical meaning)
    - m:  exponent       (no physical meaning)
    - hf: final depth = depth where force becomes 0
    """
    value = B*np.power(h-hf,m)
    return value


  def stiffnessFromUnloading(self:'Indentation', p:np.ndarray, h:np.ndarray, plot:bool=False) -> UnloadingFitResult|UnloadingFitError:# type: ignore[misc]
    """
    Calculate single unloading stiffness from Unloading; see G200 manual, p7-6

    Args:
        p (np.array): vector of forces
        h (np.array): vector of depth
        plot (bool): plot results

    Returns:
        list: stiffness, validMask, mask, optimalVariables, powerlawFit-success |br|
          validMask is [values of p,h where stiffness is determined]
    """
    if self.method== Method.CSM:
      print("**ERROR** Should not land here: CSM method")
      return None, None, None, None, None
    if self.output['verbose']>2:
      print("Number of unloading segments:"+str(len(self.iLHU))+"  Method:"+str(self.method))
    stiffness: list[float] = []
    mask: np.ndarray|None = None
    opt: np.ndarray|tuple[float, float, float]|None = None
    powerlawFit: list[bool] = []
    validMask = np.zeros_like(p, dtype=bool)
    if plot:
      if self.output['ax'] is not None:
        ax = self.output['ax']
      else:
        ax = plt.subplots()[1]
      ax.plot(h,p, '--k', label='data')
    for cycleNum, cycle in enumerate(self.iLHU):
      loadStart, loadEnd, unloadStart, unloadEnd = cycle
      if loadStart>loadEnd or loadEnd>unloadStart or unloadStart>unloadEnd:
        print('**ERROR** stiffnessFromUnloading: indicies not in order:',cycle)
      maskSegment = np.zeros_like(h, dtype=bool)
      maskSegment[unloadStart:unloadEnd+1] = True
      unloadPMax = _dictToFloat(self.model['unloadPMax'], 0.99)
      unloadPMin = _dictToFloat(self.model['unloadPMin'], 0.5)
      maskForce   = np.logical_and(p<p[loadEnd]*unloadPMax, p>p[loadEnd]*unloadPMin)
      mask        = np.logical_and(maskSegment,maskForce)
      if len(mask[mask])==0:
        print('**ERROR** mask of unloading is empty. Cannot fit\n')
        return None, None, None, None, None
      if plot:
        if cycleNum==0:
          ax.plot(h[mask],p[mask],'-b', label='this cycle')
        else:
          ax.plot(h[mask],p[mask],'-b')
      #initial values of fitting
      # It would be great to be able to linearize the equation p=B(h-hf)^m. Linearization is possible for p=Bh^m with the log-rules
      #   log p=logB+m*logh   one could argue that h>hf and that this is a great approximation and use it to get initial B,m
      #   but that might not be so great and still cumbersome
      # Easier: try a few values of m, find the one that is best for the middle point and stick with that going into the fitting
      unloadInitialM = _dictToFloat(self.model['unloadInitialM'], -1.0)
      if unloadInitialM < 0:
        m0Values  = np.logspace(0.1, 1, 5)
        hf0Values = (h[mask][0]/p[mask][0]**(1/m0Values) - h[mask][-1]/p[mask][-1]**(1/m0Values))/(1/p[mask][0]**(1/m0Values) -1/p[mask][-1]**(1/m0Values))
        B0Values  = p[mask][0]/(h[mask][0]-hf0Values)**m0Values
        pMid = B0Values*(h[mask][int(len(h[mask])/2)]-hf0Values)**m0Values
        idxBest = np.abs(pMid-p[mask][int(len(h[mask])/2)]).argmin()
        m0, hf0, B0 = float(m0Values[idxBest]), float(hf0Values[idxBest]), float(B0Values[idxBest])
      else:
        m0  = unloadInitialM
        hf0 = float((h[mask][0]/p[mask][0]**(1/m0) - h[mask][-1]/p[mask][-1]**(1/m0))/(1/p[mask][0]**(1/m0) -1/p[mask][-1]**(1/m0)))
        B0  = float(p[mask][0]/(h[mask][0]-hf0)**m0)
      # elif self.model['unloadInitialValues']=='metal': # Assuming a more linear unloading curve
      #   B0  = (p[mask][-1]-p[mask][0])/(h[mask][-1]-h[mask][0])
      #   hf0 = h[mask][0] - p[mask][0]/B0
      #   m0  = 1.5 #to get of axis
      # elif self.model['unloadInitialValues']=='polymere': # Assuming more curvature in the unloading curve
      #   hf0    = h[mask][-1]/2.0
      #   m0     = 2
      #   B0     = max(abs(p[mask][0] / np.power(h[mask][0]-hf0,m0)), 0.001)  #prevent neg. or zero
      xFit = np.asarray(h[mask], dtype=float)
      yFit = np.asarray(p[mask], dtype=float)
      bounds = (np.array([0.0, 0.0, 0.8], dtype=float),
                np.array([np.inf, max(np.min(xFit), hf0), 10.0], dtype=float))
      B0  = min( max(B0,  bounds[0][0]), bounds[1][0])  #ensure parameters are in bounds
      hf0 = min( max(hf0, bounds[0][1]), bounds[1][1])  #ensure parameters are in bounds
      m0  = min( max(m0,  bounds[0][2]), bounds[1][2])  #ensure parameters are in bounds
      p0 = np.array([B0, hf0, m0], dtype=float)
      if self.output['verbose']>2:
        print("Initial fitting values B,hf,m", B0,hf0,m0)
        print("  Bounds", bounds)
      try:
        opt, _ = curve_fit(self.unloadingPowerFunc, xFit, yFit,      # pylint: disable=unbalanced-tuple-unpacking
                          p0=p0, bounds=bounds, ftol=1e-4, maxfev=3000 )#set ftol to 1e-4 if accept more and fail less
                          # sigma=np.arange(len(mask[mask]))+1, weights that decrease from beginning to end
        if self.output['verbose']>2:
          print("  Optimal values B,hf,m", opt[0], opt[1], opt[2])
        B,hf,m = opt
        if np.isnan(B):
          raise ValueError("NAN after fitting")
        powerlawFit.append(True)
      except:
        #if fitting fails: often the initial bounds and initial values do not match
        if self.output['verbose']>0:
          print("stiffnessFrommasking: #",cycleNum," Fitting powerlaw failed. use linear fit")
        B  = (p[mask][-1]-p[mask][0])/(h[mask][-1]-h[mask][0])
        hf = h[mask][0] -p[mask][0]/B
        m  = 1.
        opt= (B,hf,m)
        powerlawFit.append(False)
      if self.model['evaluateSAtMax']:
        stiffnessPlot = B*m*math.pow( h[unloadStart]-hf, m-1)
        stiffnessValue= p[unloadStart]-stiffnessPlot*h[unloadStart]
        validMask[unloadStart]=True
      else:
        stiffnessPlot = B*m*math.pow( (h[mask][0]-hf), m-1)
        stiffnessValue= p[mask][0]-stiffnessPlot*h[mask][0]
        validMask[ np.where(mask)[0][0] ]=True
      stiffness.append(stiffnessPlot)
      if plot:
        x_ = np.linspace(0.5*h[mask].max(), h[mask].max(), 10)
        if cycleNum==0:
          ax.plot(x_,   self.unloadingPowerFunc(x_,B,hf,m),'m-', label='final fit')
          ax.plot(x_,   self.unloadingPowerFunc(x_,B0,hf0,m0),'g-', label='initial fit')
          ax.plot(x_,   stiffnessPlot*x_+stiffnessValue, 'r--', lw=3, label='linear at max')
        else:
          ax.plot(x_,   self.unloadingPowerFunc(x_,B,hf,m),'m-')
          ax.plot(x_,   self.unloadingPowerFunc(x_,B0,hf0,m0),'g-')
          ax.plot(x_,   stiffnessPlot*x_+stiffnessValue, 'r--', lw=3)
    if plot:
      ax.legend()
      ax.set_xlim(left=0)
      ax.set_ylim(bottom=0)
      ax.set_xlabel(r'depth [$\mathrm{\mu m}$]')
      ax.set_ylabel(r'force [$\mathrm{mN}$]')
    if plot and not self.output['ax']:
      plt.show()
    return stiffness, validMask, mask, opt, powerlawFit
