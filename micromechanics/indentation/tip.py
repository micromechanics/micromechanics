"""Nanoindenter tip: shape / area-function and the compliance"""
import math
from collections.abc import Callable, Sized
from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton


class Tip:
  """The main class to define indenter shape and other default values."""
  def __init__(self, shape:Any="perfect", interpFunction:Callable[[np.ndarray], Any]|None=None, compliance:float=0.0, plot:bool=False, verbose:int=0):
    """
    Initialize indenter shape

    Args:
      shape (list): list of prefactors (default = "perfect")
      interpFunction (function): tip-shape function Ac = f(hc), when it is given, other information is superseded
      compliance (float): additional compliance in test [um/mN] (sensible values: 0.0001..0.01)
      plot (bool): plot indenter shape
      verbose (bool): output
    """
    #define indenter shape: could be overwritten
    self.shape = 'perfect'
    self.areaPrefactors = []
    self.interpFunction:Callable[[np.ndarray], Any]|None = None
    if callable(interpFunction):
      self.shape = 'interpolation'
      self.interpFunction = interpFunction
    elif shape[-1]=="sphere" or shape[-1]=="iso":
      self.shape = shape[-1]
      self.areaPrefactors = shape[:-1]
    elif isinstance(shape, list):  #assume iso
      self.areaPrefactors = shape
      self.shape = 'iso'
    # Compliance
    self.compliance = compliance
    self.complianceSlope       = -1
    self.relativeStandardError = -1
    #verify and set default values
    if self.compliance > 0.01 or self.compliance < 0.0000001:
      if compliance == 0:
        if verbose>1:
          print("*WARNING*: stiffness outside domain 1e5...1e10 N/m: infinite")
      else:
        if verbose>1:
          print("*WARNING*: stiffness outside domain 1e5...1e10 N/m:",round(1000./self.compliance) )
    if plot:
      self.plotIndenterShape()
    return


  @property
  def prefactors(self) -> list[Any]|None:
    """
    Backward-compatible representation of the tip area function.

    Returns:
      list[Any] | None: area-function prefactors followed by the shape name, or None for interpolation tips.
    """
    print('**DEPRECATION** For backward compatibility, use tip.areaPrefactors instead.')
    if self.shape == 'interpolation':
      return None
    return self.areaPrefactors+[self.shape]


  @prefactors.setter
  def prefactors(self, prefactors:list[Any]|None) -> None:
    print('**DEPRECATION** For backward compatibility, use tip.areaPrefactors instead.')
    if prefactors is None:
      self.shape = 'interpolation'
      self.areaPrefactors = []
      return
    if prefactors[-1] in ('iso', 'isoPlusConstant', 'perfect', 'sphere'):
      self.shape = prefactors[-1]
      self.areaPrefactors = prefactors[:-1]
    else:
      self.shape = 'iso'
      self.areaPrefactors = prefactors


  def __repr__(self) -> str:
    """ Print tip information
    Returns:
      str: text representation
    """
    outString = 'compliance: '+str(self.compliance)+';   '
    if self.shape == 'interpolation':
      assert self.interpFunction is not None
      interpPoints = getattr(self.interpFunction, 'x', None)
      if isinstance(interpPoints, Sized):
        outString+= 'with interpolation function with '+str(len(interpPoints))+' points'
      else:
        outString+= 'with interpolation function'
    else:
      outString+= f'shape {self.shape} with prefactors: {self.areaPrefactors}'
    return outString


  def setInterpolationFunction(self, interpFunction:Callable[[np.ndarray], Any]) -> None:
    """
    The interpolation of tip-shape function Ac = f(hc)

    - From Oliver-Pharr Method, projected area of contact Ac can be obtained by measuring contact depth hc.
    - When the interpolation function is given, other information is superseded.
    - The interpolation function takes contact depth in um and returns projected area in um^2.

    Args:
       interpFunction (function): interpolation function from contact depth [um] to projected area [um^2].
    """
    self.shape = 'interpolation'
    self.interpFunction = interpFunction
    self.areaPrefactors = []
    return


  def areaFunction(self, h:np.ndarray) -> np.ndarray:
    """
    AREA FUNCTION: from contact depth hc calculate area |br|
    analytical functions inside are using [nm]; the outside of this function uses [um]|br|
    hence at the start and end there is conversion. Interpolation functions use
    the outside units directly: contact depth [um] and projected area [um^2].

    prefactors:

    - "iso" type area function A=ax^2+bx^1+cx^0.5..., [nm]
    - "perfect" type area function of a perfect Berkovich A=3*sqrt(3)*tan(65.27)^2 hc^2 = 24.494 hc^2
    - "sphere" type: A=pi(2Rh-h^2), h=depth, R indenter radius; for small h-> h^2=0
               prefactors [-pi, 2piR], R in nm
               does not account for cone at top

   Args:
       h (numpy.array): contact depth in um

    Returns:
       area: projected contact area [um^2]
    """
    h = h* 1000.   #starting here: all is in nm
    threshH = 1.e-3 #1pm
    h[h< threshH] = threshH
    area = np.zeros_like(h)
    if self.shape == 'interpolation':
      assert self.interpFunction is not None
      if hasattr(self.interpFunction, 'bounds_error'):
        self.interpFunction.bounds_error=False
      if hasattr(self.interpFunction, 'fill_value'):
        self.interpFunction.fill_value='extrapolate'
      area = np.asarray(self.interpFunction(h/1000.), dtype=float)
      area[area<0] = 0.0
      return area
    if self.shape =='iso':
      for idx, pref in enumerate(self.areaPrefactors):
        exponent = 2./math.pow(2,idx)
        area += pref*np.power(h,exponent)
    elif self.shape=='isoPlusConstant':
      h += self.areaPrefactors[-1]
      for idx, pref in enumerate(self.areaPrefactors[:-1]):
        exponent = 2./math.pow(2,idx)
        area += pref * np.power(h,exponent)
    elif self.shape == 'perfect':
      area = 24.494*np.power(h,2)
    elif self.shape=='sphere':
      radius       = self.areaPrefactors[0]*1000.
      openingAngle = self.areaPrefactors[1]
      cos      = math.cos(openingAngle/180.0*math.pi)
      sin      = math.sin(openingAngle/180.0*math.pi)
      tan      = math.tan(openingAngle/180.0*math.pi)
      mask     = radius-h > radius*sin
      rArea       = np.zeros_like(h)
      rArea[mask] = np.sqrt(radius**2 - (radius-h[mask])**2 )  #spherical section
      deltaY = radius / cos			 #tapered section
      deltaX = radius-h[~mask]
      rArea[~mask] = deltaY - tan*deltaX
      area = math.pi * rArea * rArea
    else:
      print("**ERROR** shape is unknown:", self.shape)
    area[area<0] = 0.0
    return area/1.e6 # conversion of unit from nm^2 to um^2


  def areaFunctionInverse(self, area:np.ndarray, hc0:np.ndarray|None=None) -> np.ndarray|None:
    """
    INVERSE AREA FUNCTION: from area calculate contact depth hc |br|
    using Newton iteration with initial guess contact depth hc0

    prefactors:

    - "perfect" type area function uses the direct inverse of a perfect Berkovich tip
    - other monotonic area functions are inverted numerically

    Args:
       area (numpy.array): projected contact area
       hc0 (numpy.array): initial Guess contact depth

    Returns:
       numpy.array: h = total penetration depth
    """
    area = np.asarray(area, dtype=float)
    area[area<0.0] = 0.0
    if self.shape=="perfect":
      return np.sqrt(area / 24.494)
    if hc0 is None:
      hc0 = np.sqrt(area / 24.494)
    ## define function in form f(x)-y=0
    def function(height:Any) -> Any:
      return self.areaFunction(height)-area
    ## solve
    try:
      h = newton(function, hc0)
    except (RuntimeError, OverflowError, ValueError):
      print("**ERROR** could not invert area function for shape:", self.shape)
      return None
    return h


  def plotIndenterShape(self, maxDepth:float=1, steps:int=50, show:bool=True, tipLabel:str='this tip',
                        fileName:str='') -> None:
    """
    check indenter shape: plot shape function against perfect Berkovich |br|
    analytical: perfect shape is 2.792254*x

    Args:
       maxDepth (numpy.array): maximum depth [um] to plot; default=10um
       steps (int): number of steps for plotting
       show (bool): show figure
       tipLabel (str): label for this tip
       fileName (str): if given, save to file
    """
    zoom = 0.5
    hc = np.linspace(0, maxDepth, steps)
    rNonPerfect = np.sqrt( self.areaFunction(hc)/math.pi)
    rPerfect  = 2.792254*hc
    plt.plot(rPerfect,hc, '-k', label='Berkovich')
    plt.plot(np.tan(np.radians(60.0))*hc,hc, '--k', label='$60^o$')
    plt.plot(rNonPerfect, hc, 'C1-', label=tipLabel)
    plt.legend(loc="best")
    plt.ylabel(r'contact depth [$\mathrm{\mu m}$]')
    plt.xlabel(r'contact radius [$\mathrm{\mu m}$]')
    plt.xlim([0,maxDepth*4./3./zoom])
    plt.ylim([0,maxDepth/zoom])
    plt.grid()
    if show:
      if fileName:
        plt.savefig(fileName, dpi=150, bbox_inches='tight')
      plt.show()
    return
