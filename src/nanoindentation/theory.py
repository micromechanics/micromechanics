"""CONVENTIONAL NANOINDENTATION FUNCTIONS: area, E,."""
import math, traceback
import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
from .definitions import Method
#import definitions

def YoungsModulus(self, modulusRed, nuThis=-1):
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
  modulus = (1.0-nu*nu) / ( 1.0/modulusRed - (1.0-self.nuTip*self.nuTip)/self.modulusTip)
  return modulus


def ReducedModulus(self, modulus, nuThis=-1):
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
  modulusRed =  1.0/(  (1.0-nu*nu)/modulus + (1.0-self.nuTip*self.nuTip)/self.modulusTip)
  return modulusRed


def OliverPharrMethod(self, stiffness, pMax, h):
  """
  Conventional Oliver-Pharr indentation method to calculate reduced Modulus modulusRed

  The following equations are used in that order:

    hc = h-beta pMax/stiffness

    Ac = hc(prefactors)

    stiffness = 2/sqrt(pi) sqrt(Ac) modulusRed

    Ac the contact area, hc the contact depth

  Args:
      stiffness (float): stiffness = slope dP/dh

      pMax (float): maximal force

      h (float): total penetration depth

  Returns:
      list: modulusRed, Ac, hc
  """
  threshAc = 1.e-12  #units in um: threshold = 1pm^2
  hc = h - self.beta*pMax/stiffness
  Ac   = self.tip.areaFunction(hc)
  Ac[Ac< threshAc] = threshAc  # prevent zero or negative area that might lock sqrt
  modulus   = stiffness / (2.0*np.sqrt(Ac)/np.sqrt(np.pi))
  return [modulus, Ac, hc]


def inverseOliverPharrMethod(self, stiffness, pMax, modulusRed):
  """
  Inverse Oliver-Pharr indentation method to calculate contact area Ac

  - equations and variable definitions given above; order in reverse order
  - only used for verification of the Oliver-Pharr Method

  Args:
      stiffness (float): slope dP/dh at the maximum load pMax

      pMax (float): maximal force

      modulusRed (float): modulusRed

  Returns:
      float: h penetration depth
  """
  Ac = math.pow( stiffness / (2.0*modulusRed/math.sqrt(math.pi))  ,2)
  hc0 = math.sqrt(Ac / 24.494)           # first guess: perfect Berkovich
  hc = self.tip.areaFunctionInverse(Ac, hc0=hc0)
  h = hc + self.beta*pMax/stiffness
  return h.flatten()


@staticmethod
def unloadingPowerFunc(h,B,hf,m):
  """
  internal function describing the unloading regime
  - function: p = B*(h-hf)^m
  - B:  scaling factor (no physical meaning)
  - m:  exponent       (no physical meaning)
  - hf: final depth = depth where force becomes 0
  """
  value = B*np.power(h-hf,m)
  return value


def stiffnessFromUnloading(self, p, h, plot=False):
  """
  Calculate single unloading stiffness from Unloading
  see G200 manual, p7-6

  Args:
      p (np.array): vector of forces

      h (np.array): vector of depth

      plot (bool): plot results

  Returns:
      list: stiffness, validMask, mask, optimalVariables, powerlawFit-success
        validMask is [values of p,h where stiffness is determined]
  """
  if self.method== Method.CSM:
    print("*ERROR* Should not land here: CSM method")
    return None, None, None, None, None
  if self.verbose>2:
    print("Number of unloading segments:"+str(len(self.iLHU))+"  Method:"+str(self.method))
  stiffness, mask, opt, powerlawFit = [], None, None, []
  validMask = np.zeros_like(p, dtype=bool)
  if plot:
    plt.plot(h,p,'-k')
  for cycleNum, cycle in enumerate(self.iLHU):
    loadStart, loadEnd, unloadStart, unloadEnd = cycle
    if loadStart>loadEnd or loadEnd>unloadStart or unloadStart>unloadEnd:
      print('*ERROR* stiffnessFromUnloading: indicies not in order:',cycle)
    maskSegment = np.zeros_like(h, dtype=bool)
    maskSegment[unloadStart:unloadEnd+1] = True
    maskForce   = np.logical_and(p<p[loadEnd]*self.unloadPMax, p>p[loadEnd]*self.unloadPMin)
    mask        = np.logical_and(maskSegment,maskForce)
    if len(mask[mask])==0:
      print('*ERROR* mask of unloading is empty. Cannot fit\n')
      return None, None, None, None, None
    if plot:
      plt.plot(h[mask],p[mask],'ob')
    #initial values of fitting
    hf0    = h[mask][-1]/2.0
    m0     = 2
    B0     = max(abs(p[0] / np.power(h[0]-hf0,m0)), 0.001)  #prevent neg. or zero
    bounds = [[0,0,0.8],[np.inf, max(np.min(h[mask]),hf0), 10]]
    if self.verbose>2:
      print("Initial fitting values", hf0, m0, B0)
      print("Bounds", bounds)
    # Old linear assumptions
    # B0  = (P[mask][-1]-P[mask][0])/(h[mask][-1]-h[mask][0])
    # hf0 = h[mask][0] - P[mask][0]/B0
    # m0  = 1.5 #to get of axis
    try:
      opt, _ = curve_fit(self.unloadingPowerFunc, h[mask],p[mask],      # pylint: disable=unbalanced-tuple-unpacking
                         p0=[B0,hf0,m0], bounds=bounds,
                         ftol=1e-4, maxfev=3000 )#set ftol to 1e-4 if accept more and fail less
      if self.verbose>2:
        print("Optimal values", opt)
      B,hf,m = opt
      if np.isnan(B):
        raise ValueError("NAN after fitting")
      powerlawFit.append(True)
    except:
      #if fitting fails: often the initial bounds and initial values do not match
      print(traceback.format_exc())
      if self.verbose>0:
        print("stiffnessFrommasking: #",cycleNum," Fitting failed. use linear")
      B  = (p[mask][-1]-p[mask][0])/(h[mask][-1]-h[mask][0])
      hf = h[mask][0] -p[mask][0]/B
      m  = 1.
      opt= (B,hf,m)
      powerlawFit.append(False)


    if self.evaluateStiffnessAtMax:
      stiffnessPlot = B*m*math.pow( (h[unloadStart]-hf), m-1)
      stiffnessValue= p[unloadStart]-stiffnessPlot*h[unloadStart]
      validMask[unloadStart]=True
    else:
      stiffnessPlot = B*m*math.pow( (h[mask][0]-hf), m-1)
      stiffnessValue= p[mask][0]-stiffnessPlot*h[mask][0]
      validMask[ np.where(mask)[0][0] ]=True
    stiffness.append(stiffnessPlot)
    if plot:
      plt.plot(h[mask],   self.unloadingPowerFunc(h[mask],B,hf,m),'m-')
      plt.plot(h[mask],   stiffnessPlot*h[mask]+stiffnessValue, 'r--', lw=3)
  if plot:
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.title('magenta: power function, red: linear slope')
    plt.xlabel(r'depth [$\mathrm{\mu m}$]')
    plt.ylabel(r'force [$\mathrm{mN}$]')
    plt.show()
  return stiffness, validMask, mask, opt, powerlawFit
