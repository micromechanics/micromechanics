"""CALIBRATION METHODS"""
from typing import TYPE_CHECKING
from typing_extensions import TypedDict, Unpack
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter#, medfilt
from scipy import interpolate
import lmfit
from .definitions import Method

if TYPE_CHECKING:
  from .core import Indentation

class CalibrationKwargs(TypedDict, total=False):
  """ Calibration kwargs  for type-annotations """
  constantTerm: bool
  returnArea: bool
  frameCompliance: float


class IndentationCalibrationMixin:
  """
  Tip and frame-stiffness calibration methods for :class:`Indentation`.
  """


  def calibration(self:'Indentation', eTarget:float=72.0, numPolynomial:int|None=3,critDepthStiffness:float=1.0, # type: ignore[misc]
                  critForce:float=1.0, critDepthTip:float=0.0, plotStiffness:bool=False, plotTip:bool=False,
                  **kwargs: Unpack[CalibrationKwargs]) -> bool|tuple[np.ndarray, np.ndarray]:
    """
    Calibrate by first frame-stiffness and then area-function calibration

    Args:
        eTarget (float): target Young's modulus (not reduced), nu is known
        numPolynomial (int | None): number of area function polynomial; if None: create and store an interpolation area function on ``self.tip``
        critDepthStiffness (float): what is the minimum depth of data used
        critDepthTip (float): area function what is the minimum depth of data used
        critForce (float): frame stiffness: what is the minimum force used for fitting
        plotStiffness (bool): plot stiffness graph with compliance
        plotTip (bool): plot tip shape after fitting
        **kwargs (dict): additional keyword arguments

          - constantTerm (bool): add constant term into area function
          - returnArea (bool): return contact depth and area
          - frameCompliance (float): frame compliance (if not given, determine)

    Returns:
      bool | tuple[np.ndarray, np.ndarray]: success flag, or contact depth and area when ``returnArea=True``.
    """
    constantTerm = kwargs.get('constantTerm', False)
    if 'frameCompliance' in kwargs:
      frameCompliance = kwargs['frameCompliance']
    else:
      res = self.calibrateStiffness(critDepth=critDepthStiffness, critForce=critForce, plotStiffness=plotStiffness)
      if isinstance(res, float):
        frameCompliance = res
      else:
        print('**ERROR** calibration failed.')
        return False
    ## re-create data-frame of all files
    self.restartFile()
    self.tip.compliance = frameCompliance
    slope, h, p = np.array([], dtype=float), np.array([],dtype=float), np.array([],dtype=float)
    if self.method==Method.CSM:
      self.nextTest(newTest=False)  #rerun to ensure that onlyLoadingSegment used
      while True:
        if self.output['progressBar'] is not None:
          self.output['progressBar'](1-len(self.testList)/len(self.allTestList), 'calibration1' )
        self.analyse()
        slope = np.hstack((slope, self.slope))
        h     = np.hstack((h,     self.h[self.valid]))
        p     = np.hstack((p,     self.p[self.valid]))
        if not self.testList:
          break
        success = self.nextTest()
        if not success:
          break
    else:
      while True:
        if self.output['progressBar'] is not None:
          self.output['progressBar'](1-len(self.testList)/len(self.allTestList), 'calibration2')
        self.analyse()
        slope = np.hstack((slope, self.metaUser['S_mN/um']))
        h     = np.hstack((h,     self.metaUser['hMax_um']))
        p     = np.hstack((p,     self.metaUser['pMax_mN']))
        if len(self.testList)==0:
          break
        success = self.nextTest()
        if not success:
          break

    #depth has to be positive
    mask = h>critDepthTip
    slope = slope[mask]
    h = h[mask]
    p = p[mask]

    ## fit shape function
    #reverse OliverPharrMethod to determine area function
    modulusRedGoal = self.ReducedModulus(eTarget, self.nuMat)
    Ac = np.array( np.power( slope  / (2.0*modulusRedGoal/np.sqrt(np.pi))  ,2))
    beta = self.model['beta']
    if not isinstance(beta, float):
      beta = 0.75
    hc = np.array( h - beta*p/slope )
    #calculate shape function as interpolation of 30 points (log-spacing)
    #  first calculate the  savgol-average using a adaptive window-size
    if numPolynomial is None:  # use interpolation function using random points
      # create a 2xn data-array of valid values
      mask = np.logical_and.reduce((np.isfinite(hc), np.isfinite(Ac), hc>0, Ac>0))
      if np.count_nonzero(mask)<5:
        print('**ERROR** calibration interpolation needs at least five finite, positive data points.')
        return False
      data = np.vstack((hc[mask],Ac[mask]))
      data = data[:, data[0].argsort()] # sorts the two-row data array by contact depth
      _, uniqueIdx = np.unique(data[0], return_index=True) # remove duplicate contact-depth values in next line
      data = data[:, np.sort(uniqueIdx)]
      if data.shape[1]<5:
        print('**ERROR** calibration interpolation needs at least five unique contact depths.')
        return False
      maxWindowSize = data.shape[1] if data.shape[1]%2==1 else data.shape[1]-1
      windowSize = min(maxWindowSize, max(5, data.shape[1]//20|1))
      output = np.asarray(savgol_filter(data, windowSize,3), dtype=float)
      output = output[:, np.logical_and.reduce((np.isfinite(output[0,:]), np.isfinite(output[1,:]), output[0,:]>0, output[1,:]>0))]
      output = output[:, np.unique(output[0], return_index=True)[1]]
      if output.shape[1]<2:
        print('**ERROR** calibration interpolation needs at least two filtered contact depths.')
        return False
      minDepth = max(0.0001, float(np.min(output[0,:]))+0.0001)
      maxDepth = float(np.max(output[0,:]))-0.0001
      if maxDepth<=minDepth:
        print('**ERROR** calibration interpolation depth range is invalid.')
        return False
      interpolationFunct = interpolate.interp1d(output[0,:],output[1,:])
      hc_ = np.logspace(np.log(minDepth), np.log(maxDepth), num=50, base=np.exp(1))
      Ac_ = np.asarray(interpolationFunct(hc_), dtype=float)
      interpolationFunct = interpolate.interp1d(hc_, Ac_)
      self.tip.setInterpolationFunction(interpolationFunct)
      del output, data
    else:
      #It is possible to crop only interesting contact depth: hc>1nm
      # Ac = Ac[hc>0.001]
      # hc = hc[hc>0.001]
      if constantTerm:
        appendix = 'isoPlusConstant'
      else:
        appendix = 'iso'

      def fitFunct(params:lmfit.Parameters) -> np.ndarray:     #error function
        self.tip.prefactors = [params[x].value for x in params]+[appendix]
        tempArea = self.tip.areaFunction(hc)          #use all datapoints as critDepth is for compliance plot
        residual     = np.abs(Ac-tempArea)/len(Ac)    #normalize by number of points
        return residual

      # Parameters, 'value' = initial condition, 'min' and 'max' = boundaries
      params = lmfit.Parameters()
      params.add('m0', value= 24.3, min=10.0, max=60.0)
      for idx in range(1,numPolynomial):
        startVal = np.power(100,idx)
        params.add('m'+str(idx), value= startVal/1000, min=-startVal*100, max=startVal*100)
      if constantTerm:
        params.add('c',  value= 20, min=0.5, max=300.0) ##all prefactors are in nm, this has to be too
      # do fit, here with leastsq model; args=(hc, Ac)
      result = lmfit.minimize(fitFunct, params, max_nfev=10000, nan_policy='omit')
      self.tip.prefactors = [result.params[x].value for x in result.params]+[appendix]
      print("\nTip shape:")
      print("  iterated prefactors",[round(i,1) for i in self.tip.prefactors[:-1]])
      stderr = [result.params[x].stderr for x in result.params]
      print("    standard error",['NaN' if x is None else round(x,2) for x in stderr])

    if plotTip:
      rNonPerfect = np.sqrt(Ac/np.pi)
      plt.figure()
      plt.plot(rNonPerfect, hc,'C0o', label='data')
      self.tip.plotIndenterShape(maxDepth=0.5, show=False)
      plt.show()
      #Error plot
      plt.figure()
      plt.plot(hc,(Ac-self.tip.areaFunction(hc))/Ac,'o',markersize=2)
      plt.axhline(0,color='k',linewidth=2)
      plt.xlabel(r"Depth [$\mathrm{\mu m}$]")
      plt.ylabel("Relative area error")
      plt.ylim([-0.1,0.1])
      plt.xlim(left=0)
      plt.yticks([-0.1,-0.05,0,0.05,0.1])
      plt.show()

    if kwargs.get('returnArea', False):
      return hc, Ac
    return True


  def calibrateStiffness(self:'Indentation',critDepth:float=0.5,critForce:float=0.0001,plotStiffness:bool=True, returnData:bool=False) -> float|tuple[np.ndarray, np.ndarray]:# type: ignore[misc]
    """
    Calibrate by first frame-stiffness from K^2/P of individual measurement

    Args:
        critDepth (float): frame stiffness: what is the minimum depth of data used
        critForce (float): frame stiffness: what is the minimum force used for fitting
        plotStiffness (bool): plot stiffness graph with compliance
        returnData (bool): return data for external plotting

    Returns:
        numpy.arary: data as chosen by arguments
    """
    print("Start compliance fitting")
    ## output representative values
    if self.method==Method.CSM:
      x: None|np.ndarray = None
      y: None|np.ndarray = None
      h: None|np.ndarray = None
      while True:
        self.analyse()
        if x is None or y is None or h is None:
          x = 1./np.sqrt(self.p[self.valid]-np.min(self.p[self.valid])+0.001) #add 1nm:prevent runtime error
          y = 1./self.slope
          h = self.h[self.valid]
        elif np.count_nonzero(self.valid)>0:
          x = np.hstack((x,    1./np.sqrt(self.p[self.valid]-np.min(self.p[self.valid])+0.001) ))
          y = np.hstack((y,    1./self.slope))
          h = np.hstack((h, self.h[self.valid]))
        if not self.testList:
          break
        self.nextTest()
      mask = np.logical_and(h>critDepth, x<1./np.sqrt(critForce))
      if len(mask[mask])==0:
        print("WARNING too restrictive filtering, no data left. Use high penetration: 50% of force and depth")
        mask = np.logical_and(h>np.max(h)*0.5, x<np.max(x)*0.5)
    else:
      ## create data-frame of all files
      pAll_: list[float] = []
      hAll_: list[float] = []
      sAll_: list[float] = []
      while True:
        if self.output['progressBar'] is not None:
          self.output['progressBar'](1-len(self.testList)/len(self.allTestList), 'calibrateStiffness')
        self.analyse()
        if isinstance(self.metaUser['pMax_mN'], list):
          pAll_ = pAll_+list(self.metaUser['pMax_mN'])
        elif isinstance(self.metaUser['pMax_mN'], float):
          pAll_ = pAll_+[self.metaUser['pMax_mN']]
        if isinstance(self.metaUser['hMax_um'], list):
          hAll_ = hAll_+list(self.metaUser['hMax_um'])
        elif isinstance(self.metaUser['hMax_um'], float):
          hAll_ = hAll_+[self.metaUser['hMax_um']]
        if isinstance(self.metaUser['S_mN/um'], list):
          sAll_ = sAll_+list(self.metaUser['S_mN/um'])
        elif isinstance(self.metaUser['S_mN/um'], float):
          sAll_ = sAll_+[self.metaUser['S_mN/um']]
        if not self.testList:
          break
        self.nextTest()
      pAll = np.array(pAll_)
      hAll = np.array(hAll_)
      sAll = np.array(sAll_)
      ## determine compliance by intersection of 1/sqrt(p) -- compliance curve
      x = 1./np.sqrt(pAll)
      y = 1./sAll
      mask = hAll > critDepth
      mask = np.logical_and(mask, pAll>critForce)
      print("number of data-points:", len(x[mask]))
    if len(mask[mask])==0:
      print("**ERROR** too much filtering, no data left. Decrease critForce and critDepth")
      return -1

    param, covM = np.polyfit(x[mask],y[mask],1, cov=True)
    print("fit f(x)=",round(param[0],5),"*x+",round(param[1],5))
    frameStiff      = 1./param[1]
    frameCompliance = param[1]
    self.tip.complianceSlope = param[0]
    # according to https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    # To compute standard deviation (standard errors), use perr = np.sqrt(np.diag(pcov))
    # according to https://www.cdc.gov/nchs/hus/sources-definitions/rse.htm
    # Relative standard error (RSE): A measure of an estimate’s reliability. The RSE of an estimate is obtained
    # by dividing the standard error of the estimate, SE(r), by the estimate itself, r. This quantity is
    # expressed as a percentage of the estimate and is calculated as: RSE=100[SE(r)/r]
    self.tip.relativeStandardError = np.abs( np.sqrt(np.diag(covM)[1]) / param[1] * 100. )
    print(f"  frame compliance: {frameCompliance:8.4e} um/mN = {frameCompliance/1000.:8.4e} m/N")
    print("  compliance and stiffness standard error in %: "+str(round(self.tip.relativeStandardError,2)) )
    print(f"  frame stiffness: {frameStiff:6.0f} mN/um = {1000.*frameStiff:6.2e} N/m")
    self.tip.compliance = frameCompliance

    #end of function
    if returnData:
      return x,y
    if plotStiffness or self.output['ax'] is not None:
      if plotStiffness:
        _, ax = plt.subplots()
      else:
        ax = self.output['ax']
      ax.plot(x[~mask], y[~mask], 'o', color='#165480', fillstyle='none', markersize=1, label='excluded')
      ax.plot(x[mask], y[mask],   'C0o', markersize=5, label='for fit')
      x_ = np.linspace(0, np.max(x)*1.1, 50)
      y_ = np.polyval(param, x_)
      ax.plot(x_,y_,'w-')
      ax.plot(x_,y_,'C0--')
      ax.plot([0,np.min(x)/2],[frameCompliance,frameCompliance],'k')
      ax.text(np.min(x)/2,frameCompliance,'frame compliance')
      ax.set_xlabel(r"1/sqrt(p) [$\mathrm{mN^{-1/2}}$]")
      ax.set_ylabel(r"meas. compliance [$\mathrm{\mu m/mN}$]")
      ax.legend(loc=4)
      ax.set_xlim((0, np.max(x[mask])*1.5))
      ax.set_ylim((0, np.max(y[mask])*1.5))
      if plotStiffness:
        plt.show()
    return frameCompliance
