"""All functions relating to the Hertz equation for contact of sphere and flat surface"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def hertzFit(self):
  """
  Fit the initial force displacement curve to the Hertzian curve
  """
  print(np.sum(self.h))
  return


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
  fitElast, pcov = curve_fit(funct, h[iMin:iJump], p[iMin:iJump], p0=[100.,0.])
  # pylint warning: Possible unbalanced tuple unpacking with sequence defined at line 837 of
  # scipy.optimize.minpack: left side has 2 label(s), right side has 5 value(s) (389:4)
  # [unbalanced-tuple-unpacking]
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
