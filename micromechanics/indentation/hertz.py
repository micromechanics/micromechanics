"""All functions relating to the Hertz equation for contact of sphere and flat surface"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def hertzEquation(h,h0,E,R=1):
  """
  calculate the force for a given reduced Youngsmodulus, tip-radius and penetration depth

  Args:
    h: depth of indent (possibly array)
    h0: depth offset
    E: reduced Young's modulus
    R: radius of tip in um (default=1 for parameter fitting)
  """
  h -= h0
  h[h<0] = 0
  return 4./3. * E * np.sqrt(R*h**3)


def hertzFit(self, forceRange=(1, 25), correctH=True, plot=True):
  """
  Fit the initial force displacement curve to the Hertzian curve
  """
  fitMask = np.logical_and(forceRange[0]<self.p, self.p<forceRange[1])
  fitMask[np.argmax(self.p):] = False
  depthRange = [self.h[fitMask].min(), self.h[fitMask].max()]
  para0 = [0., 5000.]
  bounds = [[-depthRange[0],0],[depthRange[0], 50000.]]
  fitElast, _ = curve_fit(hertzEquation, self.h[fitMask], self.p[fitMask], p0=para0, bounds=bounds) # pylint: disable=unbalanced-tuple-unpacking
  if self.verbose>1:
    print('Depth range', depthRange)
    print('Optimal parameters (h0,prefactor)',fitElast)
  if plot:
    plt.plot(self.h,self.p)
    h_ = np.linspace(depthRange[0], depthRange[1])
    plt.plot(h_, hertzEquation(h_,*para0))
    plt.ylim([0,forceRange[1]*1.2])
    plt.xlim([depthRange[0]-0.01,depthRange[1]+0.01])
    plt.show()
  if correctH:
    self.h -= fitElast[0]
  return fitElast



def popIn(self, correctH=True, plot=True, removeInitialNM=2.):
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
      correctH: correct depth such that curves aligned
      plot: plot pop-in curve
      removeInitialNM: remove initial nm from data as they have large scatter

  Returns:
      pop-in force, dictionary of certainty
  """
  maxPlasticFit = 150
  minElasticFit = 0.01

  mask = (self.h[self.valid]-np.min(self.h[self.valid]))  >removeInitialNM/1.e3
  h = self.h[self.valid][mask]
  p = self.p[self.valid][mask]

  depthRate = (h[1:]-h[:-1])
  x_        = np.arange(len(depthRate))
  fits      = np.polyfit(x_,depthRate,2)  #substract 2nd order fit b/c depthRate increases over time
  depthRate-= np.polyval(fits,x_)
  iJump     = np.argmax(depthRate)
  iMax      = min(np.argmax(p), iJump+maxPlasticFit)      #max for fit: 150 data-points or max. of curve
  iMin      = np.min(np.where(p>minElasticFit))
  fitPlast  = np.polyfit(h[iJump+1:iMax],p[iJump+1:iMax],2) #does not have to be parabola, just close fit
  slopePlast= np.polyder(np.poly1d(fitPlast))(h[iJump+1] )
  def funct(depth, prefactor, h0):
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
