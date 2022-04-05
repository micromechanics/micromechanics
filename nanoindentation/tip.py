"""Nanoindenter tip: shape / area-function and the compliance"""
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

class Tip:
  """
  The main class to define indenter shape and other default values.

  Initialize indenter shape

  Args:
    shape: list of prefactors (defualt = "perfect");

    interpFunction: tip-shape function Ac = f(hc), when it is given, other information are superseeded;

    compliance: additional compliance in test [um/mN] (sensible values: 0.0001..0.01);

    plot: plot indenter shape;

    verbose: output;
  """
  def __init__(self, shape="perfect", interpFunction=None, compliance=0.0, plot=False, verbose=0):
    #define indenter shape: could be overwritten
    if callable(interpFunction):
      self.prefactors = None
      self.interpFunction = interpFunction
    elif shape[-1]=="sphere" or shape[-1]=="iso":
      self.prefactors = shape
    elif isinstance(shape, list):  #assume iso
      self.prefactors = shape
      self.prefactors.append("iso")
    else:
      self.prefactors = ["perfect"]
    self.compliance = compliance
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


  def __repr__(self):
    outString = 'compliance: '+str(self.compliance)+';   '
    if self.prefactors is None:
      outString+= 'with interpolation function with '+str(len(self.interpFunction.x))+' points'
    else:
      outString+= 'prefactors: '+str(self.prefactors)
    return outString


  def setInterpolationFunction(self,interpFunction):
    """
    The interpolation of tip-shape function Ac = f(hc).

    From Oliver-Pharr Method, projected area of contact Ac can be obtained by measuring contact depth hc.

    When the interpolation function is given, other information are superseeded.
    """
    self.interpFunction = interpFunction
    self.prefactors = None
    return


  def areaFunction(self, h):
    """
    AREA FUNCTION: from contact depth hc calculate area

    all functions inside are using [nm]; the outside of this function uses [um];

    hence at the start and end there is conversion

    prefactors:
    - "iso" type area function A=ax^2+bx^1+cx^0.5..., [nm]
    - "perfect" type area function of a perfect Berkovich A=3*sqrt(3)*tan(65.27)^2 hc^2 = 24.494 hc^2
    - "sphere" type: A=pi(2Rh-h^2), h=depth, R indenter radius; for small h-> h^2=0
               prefactors [-pi, 2piR], R in nm
               does not account for cone at top

   Args:
       h [array]: contact depth in um

    Returns:
       area: projected contact area [um^2]
    """
    h = h* 1000.   #starting here: all is in nm
    threshH = 1.e-3 #1pm
    h[h< threshH] = threshH
    area = np.zeros_like(h)
    if self.prefactors is None:
      self.interpFunction.bounds_error=False
      self.interpFunction.fill_value='extrapolate'
      return self.interpFunction(h/1000.)
    if self.prefactors[-1]=='iso':
      for i in range(0, len(self.prefactors)-1):
        exponent = 2./math.pow(2,i)
        area += self.prefactors[i]*np.power(h,exponent)
        #print(i, self.prefactors[i], h,exponent, area)
    elif self.prefactors[-1]=='isoPlusConstant':
      h += self.prefactors[-2]
      for i in range(0, len(self.prefactors)-2):
        exponent = 2./math.pow(2,i)
        area += self.prefactors[i]*np.power(h,exponent)
    elif self.prefactors[-1]=='perfect':
      area = 24.494*np.power(h,2)
    elif self.prefactors[-1]=='sphere':
      radius = self.prefactors[0]*1000.
      openingAngle = self.prefactors[1]
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
      print("*ERROR*: prefactors last value does not contain type")
    area[area<0] = 0.0
    return area/1.e6 # conversion of unit from nm^2 to um^2


  def areaFunctionInverse(self, area, hc0=70):
    """
    INVERSE AREA FUNCTION: from area calculate contact depth hc

    using Newton iteration with initial guess contact depth hc0

    prefactors:
    -  "iso" type area function A=ax^2+bx^1+cx^0.5..., [nm]
    -  "perfect" type area function of a perfect Berkovich A=3*sqrt(3)*tan(65.27)^2 hc^2 = 24.494 hc^2

    Args:
       area: projected contact area

       hc0: initial Guess contact depth

    Returns:
       h: total penetration depth
    """
    ## define function in form f(x)-y=0
    def function(height):
      return self.areaFunction(np.array([height]))-area
    ## solve
    if self.prefactors[-1]=="iso":
      h = newton(function, hc0)
    elif self.prefactors[-1]=="perfect":
      h = math.sqrt(area / 24.494)
    else:
      print("*ERROR*: prefactors last value does not contain type")
    return h


  def plotIndenterShape(self, maxDepth=1, steps=50, show=True, tipLabel=None, fileName=None):
    """
    check indenter shape: plot shape function against perfect Berkovich

    analytical: perfect shape is 2.792254*x

    Args:
       maxDepth: maximum depth [um] to plot; default=10um

       steps: number of steps for plotting

       show: show figure

       tipLabel: label for this tip

       fileName: if given, save to file
    """
    zoom = 0.5
    hc = np.linspace(0, maxDepth, steps)
    rNonPerfect = np.sqrt( self.areaFunction(hc)/math.pi)
    rPerfect  = 2.792254*hc
    if tipLabel is None:
      tipLabel = 'this tip'
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
      if fileName is not None:
        plt.savefig(fileName, dpi=150, bbox_inches='tight')
      plt.show()
    return
