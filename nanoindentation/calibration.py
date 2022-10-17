"""CALIBRATION METHODS"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter#, medfilt
import scipy.interpolate as interpolate
import lmfit
#import definitions
from .definitions import Method

def calibration(self,eTarget=72.0,numPolynomial=3,critDepthStiffness=1.0, critForce=1.0, critDepthTip=0.0, plotStiffness=False,\
  plotTip=False, **kwargs):
  """
  Calibrate by first frame-stiffness and then area-function calibration

  Args:
      eTarget: target Young's modulus (not reduced), nu is known
      numPolynomial: number of area function polynomial; if None: return interpolation function
      critDepthStiffness: what is the minimum depth of data used
      critDepthTip: area function what is the minimum depth of data used
      critForce: frame stiffness: what is the minimum force used for fitting
      plotStiffness: plot stiffness graph with compliance
      pltTip: plot tip shape after fitting
      constantTerm: add constant term into area function
      returnArea: return contact depth and area
  """
  constantTerm = kwargs.get('constantTerm', False)
  frameCompliance = self.calibrateStiffness(critDepth=critDepthStiffness,critForce=critForce,
    plotStiffness=plotStiffness)

  ## re-create data-frame of all files
  temp = {'method': self.method, 'onlyLoadingSegment': self.onlyLoadingSegment}
  self.restartFile()
  self.tip.compliance = frameCompliance
  for item in temp:
    setattr(self, item, temp[item])
  slope, h, p = np.array([], dtype=np.float64), np.array([],dtype=np.float64), np.array([],dtype=np.float64)
  if self.method==Method.CSM:
    self.nextTest(newTest=False)  #rerun to ensure that onlyLoadingSegment used
    while True:
      self.analyse()
      slope = np.hstack((slope, self.slope))
      h     = np.hstack((h,     self.h[self.valid]))
      p     = np.hstack((p,     self.p[self.valid]))
      if not self.testList:
        break
      self.nextTest()
  else:
    while True:
      self.analyse()
      slope = np.hstack((slope, self.metaUser['S_mN/um']))
      h     = np.hstack((h,     self.metaUser['hMax_um']))
      p     = np.hstack((p,     self.metaUser['pMax_mN']))
      if len(self.testList)==0:
        break
      self.nextTest()

  #depth has to be positive
  mask = h>critDepthTip
  slope = slope[mask]
  h = h[mask]
  p = p[mask]

  ## fit shape function
  #reverse OliverPharrMethod to determine area function
  modulusRedGoal = self.ReducedModulus(eTarget, self.nuMat)
  Ac = np.array( np.power( slope  / (2.0*modulusRedGoal/np.sqrt(np.pi))  ,2))
  hc = np.array( h - self.beta*p/slope )
  #calculate shape function as interpolation of 30 points (log-spacing)
  #  first calculate the  savgol-average using a adaptive window-size
  if numPolynomial is None:
    # use interpolation function using random points
    data = np.vstack((hc,Ac))
    data = data[:, data[0].argsort()]
    windowSize = int(len(Ac)/20) if int(len(Ac)/20)%2==1 else int(len(Ac)/20)-1
    output = savgol_filter(data,windowSize,3)
    interpolationFunct = interpolate.interp1d(output[0,:],output[1,:])
    hc_ = np.logspace(np.log(0.0001),np.log(np.max(output[0,:])),num=50,base=np.exp(1))
    Ac_ = interpolationFunct(hc_)
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
    def fitFunct(params):     #error function
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
    result = lmfit.minimize(fitFunct, params, max_nfev=10000)
    self.tip.prefactors = [result.params[x].value for x in result.params]+[appendix]
    print("\nTip shape:")
    print("  iterated prefactors",[round(i,1) for i in self.tip.prefactors[:-1]])
    stderr = [result.params[x].stderr for x in result.params]
    print("    standard error",['NaN' if x is None else round(x,2) for x in stderr])

  if plotTip:
    rNonPerfect = np.sqrt(Ac/np.pi)
    plt.plot(rNonPerfect, hc,'C0o', label='data')
    self.tip.plotIndenterShape(maxDepth=1.5)
    #Error plot
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


def calibrateStiffness(self,critDepth=0.5,critForce=0.0001,plotStiffness=True, returnAxis=False,\
  returnData=False):
  """
  Calibrate by first frame-stiffness from K^2/P of individual measurement

  Args:
      critDepth: frame stiffness: what is the minimum depth of data used

      critForce: frame stiffness: what is the minimum force used for fitting

      plotStiffness: plot stiffness graph with compliance

      returnAxis: return axis of plot

      returnData: return data for external plotting
  """
  print("Start compliance fitting")
  ## output representative values
  if self.method==Method.CSM:
    x, y, h = None, None, None
    while True:
      self.analyse()
      if x is None:
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
    pAll, hAll, sAll = [], [], []
    while True:
      self.analyse()
      if isinstance(self.metaUser['pMax_mN'], list):
        pAll = pAll+list(self.metaUser['pMax_mN'])
        hAll = hAll+list(self.metaUser['hMax_um'])
        sAll = sAll+list(self.metaUser['S_mN/um'])
      else:
        pAll = pAll+[self.metaUser['pMax_mN']]
        hAll = hAll+[self.metaUser['hMax_um']]
        sAll = sAll+[self.metaUser['S_mN/um']]
      if not self.testList:
        break
      self.nextTest()
    pAll = np.array(pAll)
    hAll = np.array(hAll)
    sAll = np.array(sAll)
    ## determine compliance by intersection of 1/sqrt(p) -- compliance curve
    x = 1./np.sqrt(pAll)
    y = 1./sAll
    mask = hAll > critDepth
    mask = np.logical_and(mask, pAll>critForce)
    print("number of data-points:", len(x[mask]))
  if len(mask[mask])==0:
    print("ERROR too much filtering, no data left. Decrease critForce and critDepth")
    return None

  param, covM = np.polyfit(x[mask],y[mask],1, cov=True)
  print("fit f(x)=",round(param[0],5),"*x+",round(param[1],5))
  frameStiff = 1./param[1]
  frameCompliance = param[1]
  print("  frame compliance: %8.4e um/mN = %8.4e m/N"%(frameCompliance,frameCompliance/1000.))
  stderrPercent = np.abs( np.sqrt(np.diag(covM)[1]) / param[1] * 100. )
  print("  compliance and stiffness standard error in %:",round(stderrPercent,2) )
  print("  frame stiffness: %6.0f mN/um = %6.2e N/m"%(frameStiff,1000.*frameStiff))
  self.tip.compliance = frameCompliance

  #end of function
  if returnData:
    return x,y
  if plotStiffness:
    _, ax = plt.subplots()
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
    ax.set_ylim([0,np.max(y[mask])*1.5])
    ax.set_xlim([0,np.max(x[mask])*1.5])
    if returnAxis:
      return ax
    plt.show()
  return frameCompliance
