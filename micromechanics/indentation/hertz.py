"""All functions relating to the Hertz equation for contact of sphere and flat surface"""
from typing import Any, TYPE_CHECKING
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

if TYPE_CHECKING:
  from .core import Indentation


def hertzEquation(h:np.ndarray, h0:float, E:float, R:float=1) -> np.ndarray:
  """
  calculate the force for a given reduced Youngsmodulus, tip-radius and penetration depth

  Args:
    h (numpy.array): depth of indent (possibly array)
    h0 (numpy.array): depth offset
    E (numpy.array): reduced Young's modulus
    R (float): radius of tip in um (default=1 for parameter fitting)

  Returns:
    numpy.array: force
  """
  h = np.asarray(h, dtype=float) - h0
  h = np.maximum(h, 0.0)
  return 4./3. * E * np.sqrt(R*h**3)


class IndentationHertzMixin:
  """
  Hertzian contact and pop-in methods for :class:`Indentation`.
  """
  def hertzFit(self:'Indentation', forceRange:tuple[float,float]=(1, 25), correctH:bool=True, plot:bool=True) -> list[float]:# type: ignore[misc]
    """
    Fit the initial force displacement curve to the Hertzian curve

    Args:
      forceRange (list): force range used for fitting in mN
      correctH (bool): correct the depth
      plot (bool): plot the result

    Returns:
      list: parameters determined by fitting
    """
    fitMask = np.logical_and(forceRange[0]<self.p, self.p<forceRange[1])
    fitMask[np.argmax(self.p):] = False
    if np.count_nonzero(fitMask)<3:
      raise ValueError("hertzFit: not enough data points in forceRange before maximum load")
    xFit = np.asarray(self.h[fitMask], dtype=np.float64)
    yFit = np.asarray(self.p[fitMask], dtype=np.float64)
    depthRange = (float(xFit.min()), float(xFit.max()))
    para0 = np.array([0.0, 5000.0], dtype=np.float64)
    bounds = (np.array([-depthRange[0], 0.0], dtype=np.float64),
              np.array([depthRange[0], 50000.0], dtype=np.float64))
    fitElast, _ = curve_fit(hertzEquation, xFit, yFit, p0=para0, bounds=bounds) # pylint: disable=unbalanced-tuple-unpacking
    if self.output['verbose']>1:
      print('Depth range', depthRange)
      print('Optimal parameters (h0,prefactor)',fitElast)
    if plot:
      plt.plot(self.h,self.p)
      h_ = np.linspace(depthRange[0], depthRange[1])
      plt.plot(h_, hertzEquation(h_, para0[0], para0[1]))
      plt.ylim([0,forceRange[1]*1.2])
      plt.xlim([depthRange[0]-0.01,depthRange[1]+0.01])
      plt.show()
    if correctH:
      self.h -= fitElast[0]
    return fitElast



  def popIn(self:'Indentation', correctH:bool=True, plot:bool=True, removeInitialNM:float=2.) -> tuple[float, dict[str,Any]]:# type: ignore[misc]
    """
    Search for pop-in by jump in depth rate

    Certainty:

    - deltaSlope: higher is better (difference in elastic - plastic slope). Great indicator
    - prefactor: higher is better (prefactor of elastic curve). Great indicator
    - secondRate: lower is better (height of second largest jump). Nice indicator 0.25*deltaRate
    - covElast: lower is better. bad indicator
    - deltaH: higher is better (delta depth in jump). bad indicator
    - deltaRate: higher is better (depth rate during jump). bad indicator

    Future: iterate over largest, to identify best

    Args:
        correctH (bool): correct depth such that curves aligned
        plot (bool): plot pop-in curve
        removeInitialNM (float): remove initial nm from data as they have large scatter

    Returns:
        list: pop-in force, dictionary of certainty
    """
    maxPlasticFit = 150
    minElasticFit = 0.01

    mask = (self.h[self.valid]-np.min(self.h[self.valid]))  >removeInitialNM/1.e3
    h = self.h[self.valid][mask]
    p = self.p[self.valid][mask]
    if len(h)<6:
      raise ValueError("popIn: not enough valid data after removing initial depth")

    depthRate = h[1:]-h[:-1]
    x_        = np.arange(len(depthRate))
    fits      = np.polyfit(x_,depthRate,2)  #substract 2nd order fit b/c depthRate increases over time
    depthRate-= np.polyval(fits,x_)
    iJump     = np.argmax(depthRate)
    iMax      = min(np.argmax(p), iJump+maxPlasticFit)      #max for fit: 150 data-points or max. of curve
    elasticCandidates = np.where(p>minElasticFit)[0]
    if len(elasticCandidates)==0:
      raise ValueError("popIn: no data above minimum elastic fit force")
    iMin      = np.min(elasticCandidates)
    if iMin>=iJump or iJump+2>=iMax:
      raise ValueError("popIn: not enough points around detected jump for fitting")
    fitPlast  = np.polyfit(h[iJump+1:iMax],p[iJump+1:iMax],2) #does not have to be parabola, just close fit
    slopePlast= np.polyder(np.poly1d(fitPlast))(h[iJump+1] )

    def funct(depth:np.ndarray, prefactor:float, h0:float) -> np.ndarray:
      diff           = depth-h0
      if isinstance(diff, np.float64):
        diff = max(diff,0.0)
      else:
        diff[diff<0.0] = 0.0
      return prefactor* (diff)**(3./2.)
    fitElast, pcov = curve_fit(funct, h[iMin:iJump], p[iMin:iJump], p0=[100.,0.])    # pylint: disable=unbalanced-tuple-unpacking
    slopeElast= (funct(h[iJump],*fitElast) - funct(h[iJump]*0.9,*fitElast)) / (h[iJump]*0.1)
    fPopIn    = p[iJump]
    certainty = {"deltaRate":depthRate[iJump], "prefactor":fitElast[0], "h0":fitElast[1], \
                  "deltaSlope": slopeElast-slopePlast, 'deltaH':h[iJump+1]-h[iJump],\
                  "covElast":pcov[0,0] }
    listDepthRate = depthRate.tolist()
    iJump2 = np.argmax(listDepthRate)
    while (iJump2-iJump)<3:
      del listDepthRate[iJump2]
      iJump2 = np.argmax(listDepthRate)
    certainty["secondRate"] = np.max(listDepthRate)
    if plot:
      _, ax1 = plt.subplots()
      ax2 = ax1.twinx()
      ax1.plot(self.h,self.p)
      h_ = np.linspace(self.h[iJump+1],self.h[iMax])
      ax1.plot(h_, np.polyval(fitPlast,h_))
      ax1.plot(self.h[iMin:iJump], funct(self.h[iMin:iJump],*fitElast))
      ax2.plot(h[:-1],depthRate,'r')
      ax1.axvline(h[iJump], color='k', linestyle='dashed')
      ax1.axhline(fPopIn, color='k', linestyle='dashed')
      ax1.set_xlim(right=4.*self.h[iJump])
      ax1.set_ylim(top=4.*self.p[iJump], bottom=0)
      plt.show()
    if correctH:
      self.h -= certainty["h0"]
    return fPopIn, certainty
