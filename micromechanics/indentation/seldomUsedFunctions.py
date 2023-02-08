# pylint: skip-file
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import interpolate
from .definitions import Vendor, Method

def tareDepthForce(self, slopeThreshold=100, compareRead=False, plot=False):
  """
  Calculate surface contact (by slope being larger than threshold)
  and offset depth,force,time by the surface

  Future improvements:

  - surface identification in future
  - handle more cases

  Args:
      slopeThreshold: threshold slope in P-h curve for contact: 200,300

      compareRead: compare new results to the ones from the file

      plot: plot comparison new data and data from file
  """
  if self.vendor!=Vendor.Agilent or self.method==Method.CSM:
    print("tareDepthForce only valid for ISO method of Agilent at this moment")
    return
  iSurface = np.min(np.where(self.pVsHSlope>slopeThreshold))#determine point of contact
  h = self.hRaw   - self.hRaw[iSurface]                   #tare to point of contact
  p = self.pRaw   - self.pRaw[iSurface]
  t = self.tTotal - self.tTotal[iSurface]
  h-= p/self.frameStiffness                               #compensate depth for instrument deflection
  maskDrift = np.zeros_like(h, dtype=bool)
  maskDrift[self.iDrift[0]:self.iDrift[1]]   =  True
  tMiddle = (t[self.iDrift[1]]+t[self.iDrift[0]])/2
  maskDrift = np.logical_and(maskDrift, t>=tMiddle)
  iDriftS, iDriftE = np.where(maskDrift)[0][0],np.where(maskDrift)[0][-1]
  driftRate        = (h[iDriftE]-h[iDriftS])/(t[iDriftE]-t[iDriftS])
  #calc. as rate between last and first point
  #  according to plot shown in J.Hay Univerisity part 3; fitting line would be different
  print("Drift rate: %.3f nm/s"%(driftRate*1e3))
  h-= driftRate*t                                          #compensate thermal drift
  #compensate supporting mechanism (use original data since h changed)
  p-= self.slopeSupport*(self.hRaw-self.hRaw[iSurface])
  if compareRead:
    mask = self.h>0.010                                    #10nm
    error = (h[mask]-self.h[mask])/self.h[mask]
    print("Error in h: {0:.2f}%".format(np.linalg.norm(error)/len(error)*100.) )
    error = (p[mask]-self.p[mask])/self.p[mask]
    print("Error in p: {0:.2f}%".format(np.linalg.norm(error)/len(error)*100.) )
    error = (t[mask]-self.t[mask])/self.t[mask]
    print("Error in t: {0:.2f}%".format(np.linalg.norm(error)/len(error)*100.) )
  if plot:
    _, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(t,p, label='new')
    ax1.plot(self.t,self.p, label='read')
    ax1.axhline(0, linestyle='dashed', c='k')
    ax1.axvline(0, linestyle='dashed', c='k')
    ax1.legend(loc=2)
    ax2.plot(self.t, self.pVsHSlope, "C2--", label='pVsHSlope')
    ax1.set_xlabel(r"depth [$\mathrm{\mu m}$]")
    ax1.set_ylabel(r"force [$\mathrm{mN}$]")
    ax2.set_ylabel(r"depth [$\mathrm{mN/\mu m}$]", color='C2')
    plt.show()
  #set newly obtained data
  self.h, self.p, self.t = h, p, t
  return


def isFusedSilica(self, bounds=[[610,700],[71,73],[8.9,10.1]], numPoints=50):
  # -> how useful
  """
  Plot K2P, Modulus, Hardness plot to determine, if test if made on fused silica

  Args:
    bounds: min,max boundaries to determine if K2P,E,H are correct

    numPoints: number of points plotted in depth, used for interpolation
  """
  value      = ['k2p',      'modulus',   'hardness']
  plotBounds = [ [j-(j-i)*4,i+(j-i)*4] for [i,j] in bounds]
  _, ax = plt.subplots(1,3,figsize=(10,5))
  result = {'vendor':{ 'average':[],'in boundaries':[]},\
    'recalibration':{ 'average':[],'in boundaries':[]} }

  #vendor data
  x, y = [],[[],[],[]]
  while True:
    for j in range(3):
      ax[j].plot(self.h[self.valid],     getattr(self,value[j]), c='C0', alpha=0.3)
      y[j] = np.concatenate((y[j], getattr(self,value[j])))
    x    = np.concatenate((x,self.h[self.valid]))
    if len(self.testList)==0: break
    self.nextTest()
  # create interpolating function
  f1 = []
  for j in range(3):
    # use interpolation function smoothing
    data = np.vstack((x,y[j]))
    data = data[:, data[0].argsort()]
    windowSize = int(len(x)/numPoints) if int(len(x)/numPoints)%2==1 else int(len(x)/numPoints)-1
    output = savgol_filter(data,windowSize,3)
    # save to array
    f1.append(interpolate.interp1d(output[0,:],output[1,:] ,'linear', fill_value="extrapolate"))
  # calculate statistics
  x1   = np.linspace(np.min(x), np.max(x), numPoints)
  mask = x1 > np.max(x1)/2
  print('\nVendor data (last 50%):')
  for j in range(3):
    average = round(np.average(f1[j](x1)[mask]),2)
    result['vendor']['average'].append(average)
    inBounds= np.logical_and( bounds[j][0]<=f1[j](x1)[mask], f1[j](x1)[mask]<=bounds[j][1] )
    inBounds= round(inBounds.sum()*1.0 / len(inBounds),2)
    result['vendor']['in boundaries'].append(inBounds)
    success = bounds[j][0]<=average and average<=bounds[j][1]
    result['vendor']['success'] = success
    print('  Average '+value[j]+':',average,'[GPa] in boundary:',round(inBounds*100),'%','success:',success)
  print()

  #new calibration
  self.restartFile()
  result['calibration'] = self.calibration(critDepth=0.5, plotStiffness=False, plotTip=False)
  self.restartFile()
  x, y = [],[[],[],[]]
  while True:
    self.analyse()
    for j in range(3):
      ax[j].plot(self.h[self.valid], getattr(self,value[j]), c='C1', alpha=0.3)
      y[j] = np.concatenate((y[j],   getattr(self,value[j])))
    x    = np.concatenate((x, self.h[self.valid]))
    if len(self.testList)==0: break
    self.nextTest()
  # create interpolating function
  f2 = []
  for j in range(3):
    # use interpolation function smoothing
    data = np.vstack((x,y[j]))
    data = data[:, data[0].argsort()]
    windowSize = int(len(x)/numPoints) if int(len(x)/numPoints)%2==1 else int(len(x)/numPoints)-1
    output = savgol_filter(data,windowSize,3)
    # save to array
    f2.append(interpolate.interp1d(output[0,:],output[1,:] ,'linear', fill_value="extrapolate"))
  # calculate statistics
  x2   = np.linspace(np.min(x), np.max(x), numPoints)
  mask = x2 > np.max(x2)/2
  print('\nRecalibration data (last 50%):')
  for j in range(3):
    average = round(np.average(f2[j](x2)[mask]),2)
    result['recalibration']['average'].append(average)
    inBounds= np.logical_and( bounds[j][0]<=f2[j](x2)[mask], f2[j](x2)[mask]<=bounds[j][1] )
    inBounds= round(inBounds.sum()*1.0 / len(inBounds),2)
    result['recalibration']['in boundaries'].append(inBounds)
    success = bounds[j][0]<=average and average<=bounds[j][1]
    result['recalibration']['success'] = success
    print('  Average '+value[j]+':',average,'[GPa] in boundary:',round(inBounds*100),'%','success:',success)
  print('\n')

  # add fake lines for legend
  ax[1].plot(0,-10, color='C0',label='vendor')
  ax[1].plot(0,-10, color='C1',label='re-calibrate')
  ax[1].plot(0,-10, color='k', label='boundary')
  ax[1].legend(loc=4)
  #plot avarages, bounds, format axis
  for j in range(3):
    ax[j].plot(x1,f1[j](x1), linewidth=3,c='C0')
    ax[j].plot(x2,f2[j](x2), linewidth=3,c='C1')
    ax[j].axhline(bounds[j][0] ,color='k',linewidth=2)
    ax[j].axhline(bounds[j][1], color='k',linewidth=2)
    ax[j].yaxis.tick_right()
    ax[j].tick_params(axis="y",direction="in", pad=-22)
    ax[j].tick_params(axis="x",direction="in", pad=-15)
    ax[j].text(.5,.95,value[j].upper(), horizontalalignment='center', transform=ax[j].transAxes,\
        fontsize=14)
    if j==0:
      ax[j].text(.5,.05,r'depth [$\mathrm{\mu m}$]',horizontalalignment='center', transform=ax[j].transAxes,\
      fontsize=10)
    ax[j].set_ylim(plotBounds[j])
    ax[j].set_xlim(left=0)
  #finalize
  plt.subplots_adjust(left=0.0,right=1,bottom=0.0,top=1.,wspace=0.)
  return result


def analyseDrift(self, plot=True, fraction=None, timeStart=None):
  """
  Analyse drift segment by:

  - Hysitron before the test
  - Micromaterials after the test

  Args:
      plot: plot drift data

      fraction: fraction of data used for fitting (Micromaterials uses last 0.6)
      timeStart: initial timestamp used for drift analysis; e.g. after 20sec;
                this superseeds fraction

  Results:
      drift in um/s
  """
  drift = None
  if self.vendor == Vendor.Hysitron and self.fileName.endswith('.hld'):
    t = self.dataDrift[:,0]
    h = self.dataDrift[:,1]
    rate = np.zeros_like(t)
    rate[:] = np.nan
    for idxEnd,ti in enumerate(t):
      if ti<20: continue
      idxStart = np.argmin(np.abs( t[:]-(ti-20.) )  )
      rate[idxEnd] = (h[idxEnd]-h[idxStart])/(t[idxEnd]-t[idxStart])
    idxEnd = np.argmin(np.abs( t[:]-(40.) )  )
    drift = rate[idxEnd]
    print("Drift:", round(drift*1.e3,3),"nm/s")
    self.metaUser['drift'] = drift
    if plot:
      _, ax1 = plt.subplots()
      ax2 = ax1.twinx()
      ax1.plot(t,rate*1.e3,'r')
      ax1.axhline(0.05,c='r',linestyle='dashed')
      ax2.plot(t,h*1.e3,'b')
      ax1.set_xlabel(r'time [$\mathrm{s}$]')
      ax1.set_ylabel(r'drift rate [$\mathrm{nm/s}$]', color='r')
      ax2.set_ylabel(r'depth [$\mathrm{nm}$]', color='b')
      plt.show()
  elif self.vendor == Vendor.Micromaterials and self.fileName.endswith('hdf5'):
    branch = self.datafile[self.testName]['drift']
    time = np.array(branch['time'])
    depth = np.array(branch['depth'])
    if fraction is None:
      fraction = 0.6
    if timeStart is None:
      timeStart = (1-fraction)*time[-1]+fraction*time[0]
    inc = np.argmin(np.abs(time-timeStart))-1
    drift = np.polyfit(time[inc:],depth[inc:],1)[0]/1000.
  return drift
