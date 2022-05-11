"""VERIFY METHODS"""
import numpy as np
import matplotlib.pyplot as plt
from .definitions import Method
#import definitions

def verifyOneData(self):
  """
  Test one data set to ensure everything still working: OliverPharrMethod and area functions
  (normal and inverse)
  """
  self.tip.prefactors = [32.9049, -6418.303798, 288484.8518, -989287.0625, 103588.5588, 675977.3345, "iso"]
  print("Test CSM method, and area functions (normal and inverse)")
  #values from time=78.47sec of Cu_500muN_Creep_Vergleich
  harmStiff   = 159111.704268288/1000.   #  159111.704268288N/m
  load        = 0.491297865144331        #  0.491297865144331mN
  totalDepth  = 111.172457420282/1000.   #  111.901346020458nm
  print("   Set Poisson's ratio 0.35")
  self.nuMat = 0.35
  print("   From Agilent software")
  print("      harmStiff   = 159111.704268288 N/m")
  print("      load        = 0.49129786514433 mN")
  print("      totalDepth  = 111.901346020458 nm")
  print("      H           = 0.82150309678705 GPa")
  print("      E           = 190.257729329881 GPa")
  print("      modulusRed  = 182.338858733495 GPa")
  print("      Stiffness Squared Over Load=51529.9093101531 GPa")
  print("      ContactArea = 598047.490101769 nm^2")
  [modulusRed, Ac, _]  = self.OliverPharrMethod(np.array([harmStiff]), np.array([load]), \
    np.array([totalDepth]))
  print("   Evaluated by this python method")
  print("      reducedModulus [GPa] =",round(modulusRed[0],4),"  with error=", \
    round((modulusRed[0]-182.338858733495)*100/182.338858733495,4),'%')
  print("      ContactArea    [um2] =",round(Ac[0],4),"  with error=", \
    round((Ac[0]-598047.490101769/1.e6)*100/598047.490101769/1.e6,4),'%')
  modulus = self.YoungsModulus(modulusRed)
  print("      Youngs Modulus [GPa] =",round(modulus[0],4),"  with error=", \
    round((modulus[0]-190.257729329881)*100/190.257729329881,4),'%')
  totalDepth2 = self.inverseOliverPharrMethod(np.array([harmStiff]), np.array([load]), modulusRed)
  print("      By using inverse methods: total depth h=",totalDepth2[0], "[um]  with error=", \
    round((totalDepth2[0]-totalDepth)*100/totalDepth,4),'%')
  print("End Test")
  return

def verifyOneData1(self):
  """
  Test one data set to ensure everything still working: OliverPharrMethod and area functions (normal and inverse)
  """
  self.tip.prefactors = [24.8204,402.507,-3070.91,3699.87,"iso" ]
  self.tip.compliance = 1000.0/9.2358e6
  print("Test CSM method, and area functions (normal and inverse)")
  #values from time=78.47sec of FS.xls in 5Materials
  harmStiff   = 25731.8375827836/1000.   #  25731.8375827836 N/m
  load        = 0.987624311132669        #  0.987624311132669 mN
  totalDepth  = 88.2388854303261/1000.   #  88.2388854303261 nm
  print("   Set Poisson's ratio 0.18")
  self.nuMat = 0.18
  print("   From Agilent software")
  print("      harmContactStiff = 25731.8375827836 N/m")
  print("      load             = 0.987624311132669 mN")
  print("      totalDepth       = 88.2388854303261 nm")
  print("      H           = 10.0514655820034 GPa")
  print("      E           = 75.1620054287519 GPa")
  print("      Stiffness Squared Over Load=670.424429535749 GPa")
  [modulusRed, _, _]  = self.OliverPharrMethod(np.array([harmStiff]), np.array([load]), \
    np.array([totalDepth]))
  modulus = self.YoungsModulus(modulusRed)
  print("      Youngs Modulus [GPa] =",modulus[0],"  with error=", \
    round((modulus[0]-75.1620054287519)*100/75.1620054287519,4),'%'  )
  totalDepth2 = self.inverseOliverPharrMethod(np.array([harmStiff]), np.array([load]), modulusRed)
  print("      By using inverse methods: total depth h=",totalDepth2[0], "[um]  with error=", \
    round((totalDepth2[0]-totalDepth)*100/totalDepth,4), '%')
  print("End Test")
  return

def verifyReadCalc(self, plot=True):
  """
  Compare Young's modulus data saved in the file to Young's modulus data calculated by these functions

  Args:
    plot: plot comparison
  """
  modulusRed,Ac,hc = self.OliverPharrMethod(self.slope, self.p[self.valid], self.h[self.valid])
  modulus = self.YoungsModulus(modulusRed)
  hardness = self.p[self.valid] / Ac
  if self.method==Method.CSM:
    if plot:
      plt.semilogy(self.t[self.valid],self.hc,'o',label='read')
      plt.semilogy(self.t[self.valid],hc,label='calc')
      plt.legend(loc=0)
      plt.xlim(left=0)
      plt.ylim([0,np.max(self.hc)])
      plt.xlabel('time [s]')
      plt.ylabel('contact depth $h_c$ [$\mu m$]')  # pylint: disable=anomalous-backslash-in-string
      plt.title("Error in hc: {0:.2e}".format(np.linalg.norm(hc-self.hc)) )
      plt.show()
    else:
      print("  Error in hc: {0:.2e}".format(np.linalg.norm(hc-self.hc)) )
  else:
    print("Error in hc: %.3e %% between %.3e and %.3e" %(abs(hc-self.hc)*100./hc, hc, self.hc) )
  if self.method==Method.CSM:
    if plot:
      plt.semilogy(self.t[self.valid],self.Ac,'o',label='read')
      plt.semilogy(self.t[self.valid],Ac,label='calc')
      plt.legend(loc=0)
      plt.xlim(left=0)
      plt.ylim([0,np.max(self.Ac)])
      plt.xlabel('time [s]')
      plt.ylabel('contact area $A_c$ [$\mu m^2$]')# pylint: disable=anomalous-backslash-in-string
      plt.title("Error in Ac: {0:.2e}".format(np.linalg.norm((Ac-self.Ac))) )
      plt.show()
    else:
      print("  Error in Ac: {0:.2e}".format(np.linalg.norm((Ac-self.Ac))))
  else:
    print("Error in Ac: %.3e %% between %.3e and %.3e" %(abs(Ac-self.Ac)*100./Ac,Ac,self.Ac) )
  if self.method==Method.CSM:
    if plot:
      plt.plot(self.t[self.valid],self.modulusRed,'o',label='read')
      plt.plot(self.t[self.valid],modulusRed,label='calc')
      plt.legend(loc=0)
      plt.xlabel('time [s]')
      plt.ylabel('reduced modulus [GPa]')
      plt.xlim(left=0)
      plt.ylim([0,np.max(self.modulusRed)])
      plt.title("Error in modulusRed: {0:.2e}".format(np.linalg.norm((modulusRed-self.modulusRed))))
      plt.show()
    else:
      print("  Error in modulusRed: {0:.2e}".format(np.linalg.norm((modulusRed-self.modulusRed))))
  else:
    print("Error in modulusRed: %.3e %% between %.3e and %.3e" \
      %(abs(modulusRed-self.modulusRed)*100./modulusRed,modulusRed,self.modulusRed) )
  if self.method==Method.CSM:
    if plot:
      plt.plot(self.t[self.valid],self.modulus,'o',label='read')
      plt.plot(self.t[self.valid],modulus,label='calc')
      plt.legend(loc=0)
      plt.xlabel('time [s]')
      plt.ylabel('modulus E [GPa]')
      plt.xlim(left=0)
      plt.ylim([0,np.max(self.modulus)])
      plt.title("Error in modulus: {0:.2e}".format(np.linalg.norm((modulus-self.modulus))) )
      plt.show()
    else:
      print("  Error in modulus: {0:.2e}".format(np.linalg.norm((modulus-self.modulus))))
  else:
    print("Error in modulus:  %.3e %% between %.3e and %.3e" \
      %(abs(modulus-self.modulus)*100./modulus, modulus,self.modulus) )
  if self.method==Method.CSM:
    if plot:
      plt.plot(self.t[self.valid],self.hardness,'o',label='read')
      plt.plot(self.t[self.valid],hardness,label='calc')
      plt.legend(loc=0)
      plt.xlabel('time [s]')
      plt.ylabel('hardness [GPa]')
      plt.xlim(left=0)
      plt.ylim([0,np.max(self.hardness)])
      plt.title("Error in hardness: {0:.2e}".format(np.linalg.norm((hardness-self.hardness))) )
      plt.show()
    else:
      print("  Error in hardness: {0:.2e}".format(np.linalg.norm((hardness-self.hardness))))
  else:
    print("Error in hardness:  %.3e %% between %.3e and %.3e" \
      %(abs(hardness-self.hardness)*100./hardness, hardness,self.hardness) )
  return
