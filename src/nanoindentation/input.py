"""All instrument specific input functions"""
import io, re, json
from pathlib import Path
from zipfile import ZipFile
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from .definitions import Method, Vendor
#import definitions

def loadAgilent(self, fileName):
  """
  Initialize G200 excel file for processing

  Args:
      fileName: file name
  """
  self.testList = []
  self.fileName = fileName    #one file can have multiple tests
  self.indicies = {}
  workbook = pd.read_excel(fileName,sheet_name='Required Inputs')
  self.metaVendor.update( dict(workbook.iloc[-1]) )
  if self.metaVendor['Poissons Ratio']!=self.nuMat and self.verbose>0:
    print("*WARNING*: Poisson Ratio different than in file.",self.nuMat,self.metaVendor['Poissons Ratio'])
  self.datafile = pd.read_excel(fileName, sheet_name=None)
  tagged = []
  code = {"Load On Sample":"p", "Force On Surface":"p", "LOAD":"p"\
        ,"_Load":"pRaw", "Raw Load":"pRaw","Force":"pRaw"\
        ,"Displacement Into Surface":"h", "DEPTH":"h"\
        ,"_Displacement":"hRaw", "Raw Displacement":"hRaw","Displacement":"hRaw"\
        ,"Time On Sample":"t", "Time in Contact":"t", "TIME":"t", "Time":"tTotal"\
        ,"Contact Area":"Ac", "Contact Depth":"hc"\
        ,"Harmonic Displacement":"hHarmonic", "Harmonic Load":"pHarmonic","Phase Angle":"phaseAngle"\
        ,"Load vs Disp Slope":"pVsHSlope","d(Force)/d(Disp)":"pVsHSlope", "_Column": "Column"\
        ,"_Frame": "Frame"\
        ,"Support Spring Stiffness":"slopeSupport", "Frame Stiffness": "frameStiffness"\
        ,"Harmonic Stiffness":"slopeInvalid"\
        ,"Harmonic Contact Stiffness":"slope", "STIFFNESS":"slope","Stiffness":"slope" \
        ,"Stiffness Squared Over Load":"k2p","Dyn. Stiff.^2/Load":"k2p"\
        ,"Hardness":"hardness", "H_IT Channel":"hardness","HARDNESS":"hardness"\
        ,"Modulus": "modulus", "E_IT Channel": "modulus","MODULUS":"modulus","Reduced Modulus":"modulusRed"\
        ,"Scratch Distance": "s", "XNanoPosition": "x", "YNanoPosition": "y"\
        ,"X Position": "xCoarse", "Y Position": "yCoarse","X Axis Position":"xCoarse"\
        ,"Y Axis Position":"yCoarse"\
        ,"TotalLateralForce": "L", "X Force": "pX", "_XForce": "pX", "Y Force": "pY", "_YForce": "pY"\
        ,"_XDeflection": "Ux", "_YDeflection": "Uy" }
  self.fullData = ['h','p','t','pVsHSlope','hRaw','pRaw','tTotal','slopeSupport']
  if self.verbose>1:
    print("Open Agilent file: "+fileName)
  for dfName in self.datafile.keys():
    df    = self.datafile.get(dfName)
    if "Test " in dfName and not "Tagged" in dfName and not "Test Inputs" in dfName:
      self.testList.append(dfName)
      #print "  I should process sheet |",sheet.name,"|"
      if len(self.indicies)==0:               #find index of colums for load, etc
        for cell in df.columns:
          if cell in code:
            self.indicies[code[cell]] = cell
            if self.verbose>2: print("     %-30s : %-20s "%(cell,code[cell]) )
          else:
            if self.verbose>2: print(" *** %-30s NOT USED"%cell)
          if "Harmonic" in cell or "Dyn. Frequency" in cell:
            self.method = Method.CSM
        #reset to ensure default values are set
        if "p" not in self.indicies: self.indicies['p']=self.indicies['pRaw']
        if "h" not in self.indicies: self.indicies['h']=self.indicies['hRaw']
        if "t" not in self.indicies: self.indicies['t']=self.indicies['tTotal']
        #if self.verbose: print("   Found column names: ",sorted(self.indicies))
    if "Tagged" in dfName: tagged.append(dfName)
  if len(tagged)>0 and self.verbose>1: print("Tagged ",tagged)
  if "t" not in self.indicies or "p" not in self.indicies or \
     "h" not in self.indicies:
    print("*WARNING*: INDENTATION: Some index is missing (t,p,h) should be there")
  self.metaUser['measurementType'] = 'MTS, Agilent Indentation XLS'
  self.allTestList =  list(self.testList)
  self.nextTest()
  return True


def nextAgilentTest(self, newTest=True):
  """
  Go to next sheet in worksheet and prepare indentation data

  Data: _Raw: without frame stiffness correction, _Frame:  with frame stiffness correction
    (remove postscript finally)
  - only affects/applies directly depth (h) and stiffness (s)
  - modulus, hardness and k2p always only use the one with frame correction

  Args:
    newTest: take next sheet (default)
  """
  if self.vendor!=Vendor.Agilent: return False #cannot be used
  if len(self.testList)==0: return False   #no sheet left
  if newTest:
    self.testName = self.testList.pop(0)

  #read data and identify valid data points
  df     = self.datafile.get(self.testName)
  h       = np.array(df[self.indicies['h'    ]][1:-1], dtype=np.float64)
  validFull = np.isfinite(h)
  if 'slope' in self.indicies:
    slope   = np.array(df[self.indicies['slope']][1:-1], dtype=np.float64)
    self.valid =  np.isfinite(slope)
    self.valid[self.valid] = slope[self.valid] > 0.0  #only valid points if stiffness is positiv
  else:
    self.valid = validFull
  for index in self.indicies:
    data = np.array(df[self.indicies[index]][1:-1], dtype=np.float64)
    mask = np.isfinite(data)
    mask[mask] = data[mask]<1e99
    self.valid = np.logical_and(self.valid, mask)                       #adopt/reduce mask continously

  #Run through all items again and crop to only valid data
  for index in self.indicies:
    data = np.array(df[self.indicies[index]][1:-1], dtype=np.float64)
    if not index in self.fullData:
      data = data[self.valid]
    else:
      data = data[validFull]
    setattr(self, index, data)

  self.valid = self.valid[validFull]
  #  now all fields (incl. p) are full and defined

  success = self.identifyLoadHoldUnload()
  if self.onlyLoadingSegment and self.method==Method.CSM:
    # print("Length test",len(self.valid), len(self.h[self.valid]), len(self.p[self.valid])  )
    iMin, iMax = 2, self.iLHU[0][1]
    self.valid[iMax:] = False
    self.valid[:iMin] = False
    self.slope = self.slope[iMin:np.sum(self.valid)+iMin]

  #correct data and evaluate missing
  self.h /= 1.e3 #from nm in um
  if "Ac" in self.indicies         : self.Ac /= 1.e6  #from nm in um
  if "slope" in self.indicies       : self.slope /= 1.e3 #from N/m in mN/um
  if "slopeSupport" in self.indicies: self.slopeSupport /= 1.e3 #from N/m in mN/um
  if 'hc' in self.indicies         : self.hc /= 1.e3  #from nm in um
  if 'hRaw' in self.indicies        : self.hRaw /= 1.e3  #from nm in um
  if not "k2p" in self.indicies and 'slope' in self.indicies:
    self.k2p = self.slope * self.slope / self.p[self.valid]
  return success


def loadHysitron(self, fileName, plotContact=False):
  """
  Load Hysitron hld or txt file for processing, only contains one test

  Args:
      fileName: file name

      plotContact: plot intial contact identification (use this method for access)
  """
  from io import StringIO
  self.fileName = fileName
  with open(self.fileName, 'r',encoding='iso-8859-1') as inFile:
    #### HLD FILE ###
    if self.fileName.endswith('.hld'):
      line = inFile.readline()
      if not "File Version: Hysitron" in line:
        #not a Hysitron file
        return False
      if self.verbose>1:
        print("Open Hysitron file: "+self.fileName)

      #read meta-data
      prefact = [0]*6
      segmentTime = []
      segmentDeltaP = []
      segmentPoints = []
      while True:
        line = inFile.readline()
        label = line.split(":")[0]
        try:
          data = line.split(":")[1].split(" ")
          value = float(data[1])
        except:
          value = line.split(":")[1].rstrip()
        #pylint: disable=multiple-statements
        if label == "Sample Approach Data Points": break
        if label == "Machine Comp": self.compliance = value #assume nm/uN = um/mN
        if label == "Tip C0":       prefact[0] = value #nm^2/nm^2
        if label == "Tip C1":       prefact[1] = value #nm^2/nm
        if label == "Tip C2":       prefact[2] = value #nm^2/nm^0.5
        if label == "Tip C3":       prefact[3] = value #nm^2/nm^0.25
        if label == "Tip C4":       prefact[4] = value #nm^2/nm^0.125
        if label == "Tip C5":       prefact[5] = value #nm^2/nm^0.0625
        if label == "Contact Threshold": forceTreshold = value/1.e3 #uN
        if label == "Drift Rate":   self.metaVendor['drift_rate'] = value/1.e3 #um/s
        if label == "Number of Segments"  : numSegments  = value
        if label == "Segment Begin Time"  : segmentTime.append(value)
        if label == "Segment Begin Demand": pStart     = value
        if label == "Segment End Demand"  : segmentDeltaP.append( (value-pStart)/1.e3 ) #to mN
        if label == "Segment Points"      : segmentPoints.append(int(value))
        if label == "Time Stamp"          : self.timeStamp = ":".join(line.rstrip().split(":")[1:])
        #pylint: enable=multiple-statements
      self.tip.prefactors = prefact
      self.tip.prefactors.append('iso')
      if (numSegments!=len(segmentTime)) or (numSegments!=len(segmentDeltaP)):
        print("*ERROR*", numSegments,len(segmentTime),len(segmentDeltaP ) )
      segmentDeltaP = np.array(segmentDeltaP)
      segmentPoints = np.array(segmentPoints)
      segmentTime   = np.array(segmentTime)

      #read approach data
      line = inFile.readline() #Time_s  MotorDisp_mm    Piezo Extension_nm"
      data = ""
      for idx in range(int(value)):
        data +=inFile.readline()

      #read drift data
      value = inFile.readline().split(":")[1]
      line = inFile.readline()  #Time_s	Disp_nm",value
      data = ""
      for idx in range(int(value)):
        data +=inFile.readline()
      if len(data)>1:
        self.dataDrift = np.loadtxt( StringIO(str(data))  )
        self.dataDrift[:,1] /= 1.e3  #into um

      #read test data
      #Time_s	Disp_nm	Force_uN	LoadCell_nm	PiezoDisp_nm	Disp_V	Force_V	Piezo_LowV
      value = inFile.readline().split(":")[1]
      line = inFile.readline()
      data = ""
      for idx in range(int(value)):
        data +=inFile.readline()
      dataTest = np.loadtxt( StringIO(str(data))  )
      #store data
      self.t = dataTest[:,0]
      self.h = dataTest[:,1]/1.e3
      self.p = dataTest[:,2]/1.e3
      self.valid=np.ones_like(self.h, dtype=bool)

      # create loading-holding-unloading cycles
      #since the first / last point of each segment are double in both segments
      listLoading = np.where(segmentDeltaP>0.1 )[0]
      listUnload  = np.where(segmentDeltaP<-0.1)[0]
      segmentPoints  -= 1
      segmentPoints[0]+=1
      segPnts   = np.cumsum(segmentPoints)
      #don't use identifyLoadHoldUnload since those points are known
      self.iLHU = []
      for idx, _ in enumerate(listLoading):
        iSurface = segPnts[listLoading[idx]-1]+1
        iLoad    = segPnts[listLoading[idx]]
        iHold    = segPnts[listUnload[idx]-1]+1
        iUnload  = segPnts[listUnload[idx]]
        self.iLHU.append( [iSurface,iLoad,iHold,iUnload] )

    #### TXT FILE ###
    if self.fileName.endswith('.txt'):
      line0 = inFile.readline()
      line1 = inFile.readline()
      line2 = inFile.readline()
      line3 = inFile.readline()
      self.metaUser = {'measurementType': 'Hysitron Indentation TXT', 'dateMeasurement':line0.strip()}
      if line1 != "\n" or "Number of Points" not in line2 or not "Depth (nm)" in line3:
        return False #not a Hysitron file
      if self.verbose>1: print("Open Hysitron file: "+self.fileName)
      dataTest = np.loadtxt(inFile)
      #store data
      self.t = dataTest[:,2]
      self.h = dataTest[:,0]/1.e3
      self.p = dataTest[:,1]/1.e3
      #set unknown values
      self.valid = np.ones_like(self.h)
      forceTreshold = 0.25 #250uN
      self.identifyLoadHoldUnload()

    #correct data
    #flatten intial section of retraction
    idxMinH  = np.argmin(self.h)
    self.p[:idxMinH] = self.p[idxMinH]
    self.h[:idxMinH] = self.h[idxMinH]
    idxMask = int( np.where(self.p>forceTreshold)[0][0])
    fractionMinH = 0.5
    hFraction    = (1.-fractionMinH)*self.h[idxMinH]+fractionMinH*self.h[idxMask]
    idxMask = np.argmin(np.abs(self.h-hFraction))
    if idxMask>2:
      mask     = np.zeros_like(self.h, dtype=bool)
      mask[:idxMask] = True
      fit = np.polyfit(self.h[mask],self.p[mask],1)
      self.p -= np.polyval(fit,self.h)

      #use force signal and its threshold to identify surface
      #Option: use lowpass-filter and then evaluate slope: accurate surface identifaction possible,
      #    however complicated
      #Option: use lowpass-filter and then use force-threshold: accurate surface identifaction,
      #    however complicated
      #Best: use medfilter or wiener on force signal and then use force-threshold: accurate and easy
      #see also Bernado_Hysitron/FirstTests/PhillipRWTH/testSignal.py
      pZero    = np.average(self.p[mask])
      pNoise   = max(pZero-np.min(self.p[mask]), np.max(self.p[mask])-pZero )
      #from initial loading: back-extrapolate to zero force
      maskInitLoad = np.logical_and(self.p>pZero+pNoise*2. , self.p<forceTreshold)
      maskInitLoad[np.argmax(self.p):] = False
      fitInitLoad  = np.polyfit(self.p[maskInitLoad],self.h[maskInitLoad],2)#inverse h-p -> next line easier
      hZero        = np.polyval(fitInitLoad, pZero)
      ## idx = np.where(  self.p>(pZero+pNoise)  )[0][0] OLD SYSTEM NOT AS ACCURATE, better fitInitLoad
      if plotContact:
        plt.axhline(pZero,c='g', label='pZero')
        plt.axhline(pZero+pNoise,c='g',linestyle='dashed', label='pNoise')
        plt.axvline(self.h[idxMinH],c='k')
        plt.axvline(self.h[idxMask],c='k')
        plt.plot(self.h,self.p)
        plt.plot(self.h[mask],self.p[mask], label='used for pNoise')
        plt.plot(self.h[maskInitLoad],self.p[maskInitLoad], label='used for backfit')
        plt.axvline(hZero,c='r',linestyle='dashed',label='Start')
        plt.plot(hZero,pZero, "ro", label="Start")
        plt.legend(loc=0)
        plt.ylim(np.min(self.p), self.p[idx]+forceTreshold )
        plt.xlim(-0.1,self.h[idx]+0.05)
        plt.show()
        print ("Debug pZero and pNoise:",pZero,pNoise)
    else:
      print("Error", forceTreshold,np.where(self.p>forceTreshold)[0][:10])
      pZero = 0
      idx   = 0
    ## self.t -= self.t[idx] #do not offset time since segment times are given
    self.h -= hZero
    self.p -= pZero
  return True



def loadMicromaterials(self, fileName):
  """
  Load Micromaterials txt/zip file for processing, contains only one test

  Args:
      fileName: file name or file-content
  """
  if isinstance(fileName, io.TextIOWrapper) or fileName.endswith('.txt'):
    #if singe file or file in zip-archive
    try:            #file-content given
      dataTest = np.loadtxt(fileName)  #exception caught
      if not isinstance(fileName, io.TextIOWrapper):
        self.fileName = fileName
        if self.verbose>1: print("Open Micromaterials file: "+self.fileName)
        self.metaUser = {'measurementType': 'Micromaterials Indentation TXT'}
    except:
      if self.verbose>1:
        print("Is not a Micromaterials file")
      return False
    self.t = dataTest[:,0]
    self.h = dataTest[:,1]/1.e3
    self.p = dataTest[:,2]
    self.valid = np.ones_like(self.t, dtype=bool)
    self.identifyLoadHoldUnload()
  elif fileName.endswith('.zip'):
    #if zip-archive of multilpe files
    self.datafile = ZipFile(fileName)
    self.testList = self.datafile.namelist()
    if len(np.nonzero([not i.endswith('txt') for i in self.datafile.namelist()])[0])>0:
      print('Not a Micromaterials zip of txt-files')
      return False
    if self.verbose>1:
      print("Open Micromaterials zip of txt-files: "+fileName)
    self.allTestList =  list(self.testList)
    self.fileName = fileName
    self.metaUser = {'measurementType': 'Micromaterials Indentation ZIP'}
    self.nextTest()
  return True


def nextMicromaterialsTest(self):
  """
  Go to next file in zip or hdf5-file
  """
  if self.vendor!=Vendor.Micromaterials: #cannot be used
    return False
  if len(self.testList)==0: #no sheet left
    return False
  self.testName = self.testList.pop(0)
  myFile = self.datafile.open(self.testName)
  txt = io.TextIOWrapper(myFile, encoding="utf-8")
  success = self.loadMicromaterials(txt)
  return success


def loadFischerScope(self,fileName):
  """
  Initialize txt-file from Fischer-Scope for processing

  Args:
    fileName: file name
  """
  self.metaVendor = {'date':[], 'shape correction':[], 'coordinate x':[], 'coordinate y':[],
          'work elastic':[], 'work nonelastic':[], 'EIT/(1-vs^2) [GPa]':[], 'HIT [N/mm]':[],
          'HUpl [N/mm]': [], 'hr [um]':[], 'hmax [um]':[], 'Compliance [um/N]':[],
          'epsilon':[], 'fit range': []}
  self.workbook = []
  self.testList = []
  self.fileName = fileName
  block = None
  with open(fileName,'r',encoding='iso-8859-1') as fIn:
    # read initial lines and initialialize
    line = fIn.readline()
    if ".hap	Name of the application" not in line:
      print("Not a Fischer Scope")
      return False
    identifier = line.split()[0]
    _ = fIn.readline()
    self.metaVendor['Indent_Type'] = fIn.readline().split()[0]
    self.metaVendor['Indent_F'] = ' '.join( fIn.readline().split()[2:] )
    self.metaVendor['Indent_C'] = ' '.join( fIn.readline().split()[2:] )
    self.metaVendor['Indent_R'] = ' '.join( fIn.readline().split()[2:] )
    #read all lines after initial lines
    for line in fIn:
      pattern = identifier+r"   \d\d\.\d\d\.\d\d\d\d  \d\d:\d\d:\d\d"
      dataInLine = line.replace(',','.').split()
      dataInLine = [float(item) if isfloat(item) else None for item in dataInLine]
      if re.match(pattern, line) is not None:
        ## finish old individual measurement
        if block is not None:
          if np.array(block).shape[1]==5:
            df = pd.DataFrame(np.array(block), columns=['F','h','t','HMu','HM'] )
          else:
            df = pd.DataFrame(np.array(block), columns=['F','h','t'] )
          self.workbook.append(df)
        ## start new  individual measurement
        block = []
        self.metaVendor['date'] += [' '.join(line.split()[-2:])]
        self.testList.append('_'.join(line.split()[-2:]))
      elif line.startswith('Indenter shape correction:'):
        self.metaVendor['shape correction'] += [line.split()[-1]]
      elif 'x=  ' in line and 'y=  ' in line:
        self.metaVendor['coordinate x'] += [float(line.split()[1])]
        self.metaVendor['coordinate y'] += [float(line.split()[3])]
      elif line.startswith('We	['):
        self.metaVendor['work elastic'] += [line.split()[-1]]
      elif line.startswith('Wr	['):
        self.metaVendor['work nonelastic'] += [line.split()[-1]]
      elif line.startswith('EIT/(1-vs^2)	[GPa]') and not line.endswith('------\n'):
        self.metaVendor['EIT/(1-vs^2) [GPa]'] += [float(line.split()[-1])]
      elif line.startswith('HIT	[N/mm') and not line.endswith('------\n'):
        self.metaVendor['HIT [N/mm]'] += [float(line.split()[-1])]
      elif line.startswith('HUpl	[N/mm') and not line.endswith('------\n'):
        self.metaVendor['HUpl [N/mm]'] += [float(line.split()[-1])]
      elif line.startswith('hr	[') and not line.endswith('------\n'):
        self.metaVendor['hr [um]'] += [float(line.split()[-1])]
      elif line.startswith('hmax	[') and not line.endswith('------\n'):
        self.metaVendor['hmax [um]'] += [float(line.split()[-1])]
      elif line.startswith('Compliance	[') and not line.endswith('------\n'):
        self.metaVendor['Compliance [um/N]'] += [float(line.split()[-1])]
      elif 'Epsilon =' in line:
        self.metaVendor['epsilon'] += [float(line.split()[-1])]
        self.metaVendor['fit range'] += [' '.join(line.split()[:-3])]
      elif ( len(dataInLine)==3 or len(dataInLine)==5 ) and not None in dataInLine:
        block.append( dataInLine )
    ## add last dataframe
    if np.array(block).shape[1]==5:
      df = pd.DataFrame(np.array(block), columns=['F','h','t','HMu','HM'] )
    else:
      df = pd.DataFrame(np.array(block), columns=['F','h','t'] )
    self.workbook.append(df)
  if self.verbose>2:
    print("Meta information:",self.metaVendor)
    print("Number of measurements read:",len(self.workbook))
  self.metaUser['measurementType'] = 'Fischer-Scope Indentation TXT'
  if self.metaVendor['Indent_F'].startswith('ESP'):
    self.method = Method.MULTI
  else:
    self.method = Method.ISO
  self.nextTest()
  return True


def nextFischerScopeTest(self):
  """
  Go to next test
  """
  df = self.workbook.pop(0)
  self.testName = self.testList.pop(0)
  self.t = np.array(df['t'])
  self.h = np.array(df['h'])
  self.p = np.array(df['F'])
  self.valid = np.ones_like(self.t, dtype=bool)
  self.identifyLoadHoldUnload()
  return True


def loadHDF5(self,fileName):
  """
  Initialize hdf5-file that all converters are producing

  Args:
    fileName: file name
  """
  self.datafile = h5py.File(fileName, mode='r') #mode='r+', locking=False)
  if self.verbose>1:
    print("Open hdf5-file: "+fileName)
  self.fileName = fileName
  self.metaVendor = {}
  self.testList = []
  if 'version' not in self.datafile.attrs or self.datafile.attrs['version']!='2.0':
    print("**ERROR** Only hdf5 version 2 supported")
    return False
  #read config and convert to dictionary
  try:
    if 'post_test_analysis' in self.datafile and \
      'com_github_micromechanics' in self.datafile['post_test_analysis'] and \
      'config' in self.datafile['post_test_analysis']['com_github_micromechanics'].attrs:
      self.config = self.datafile['post_test_analysis']['com_github_micromechanics'].attrs['config']
      self.config = json.loads(self.config)
    else:
      self.config = {}
  except:
    self.config = {}
  if "_" in self.surfaceFind and bool(self.config):
    self.surfaceFind = { i:self.config[i] for i in self.config if not i.startswith('test_')}
  for key in self.datafile:
    if re.match(r'test_\d+',key):
      self.testList.append(key)
  for key in self.datafile['instrument'].attrs:
    if isinstance(self.datafile['instrument'].attrs[key], dict):
      self.metaVendor = self.datafile['instrument'].attrs[key]
    else:
      self.metaVendor[key] = self.datafile['instrument'].attrs[key]
  converter = self.datafile.attrs['uri'].split('/')[-1]
  if 'json' in self.metaVendor:
    metaVendor = json.loads(self.metaVendor['json'])
    if 'SAMPLE' in metaVendor:  #G200X data
      templateName = metaVendor['SAMPLE']['@TEMPLATENAME']
      if 'Dynamic' in templateName or 'Essential' in templateName or 'Displacement' in templateName:
        self.method = Method.CSM
  if converter == 'hap2hdf.py':
    self.metaUser = {'measurementType': 'Fischer Scope Indentation HDF5'}
    self.unloadPMax = 0.99
    self.unloadPMin = 0.21
    self.zeroGradDelta = 0.02  #reduced accuracy
  elif converter == 'Micromaterials2hdf.py':
    self.metaUser = {'measurementType': 'Micromaterials Indentation HDF5'}
    self.unloadPMax = 0.99
    self.unloadPMin = 0.5
  elif converter == 'nmd2hdf.py':
    self.metaUser = {'measurementType': 'KLA Indentation HDF5'}
    self.unloadPMax = 0.99
    self.unloadPMin = 0.5
    self.zeroGradDelta = 0.005  #enhanced accuracy
  elif converter == 'xls2hdf.py':
    self.metaUser = {'measurementType': 'MTS / Agilent Indentation HDF5'}
    self.unloadPMax = 0.99
    self.unloadPMin = 0.5
  elif converter == 'converter_tdm.py':
    self.metaUser = {'measurementType': 'HysitronInsitu Indentation HDF5'}
    self.unloadPMax = 0.99
    self.unloadPMin = 0.5
    self.zeroGradDelta = 0.04
  else:
    print("ERROR UNKNOWN CONVERTER",converter)
  self.allTestList =  list(self.testList)
  self.nextTest()
  return True


def nextHDF5Test(self):
  """
  Go to next branch in HDF5 file

  TODO check for non CSM
  """
  #organize general data
  if len(self.testList)==0: #no sheet left
    return False
  while len(self.testList)>0:
    self.testName = self.testList.pop(0)
    if self.testName not in self.config or 'ignore' not in self.config[self.testName]:
      break
  branch = self.datafile[self.testName]['data']
  inFile = list(branch.keys())
  nameDict   = json.load(open(Path(__file__).parent/'names.json'))
  if self.metaUser['measurementType'].split()[0] in nameDict:
    nameDict = nameDict[self.metaUser['measurementType'].split()[0]]
  else:
    print("**ERROR instrument not in names.json", self.metaUser['measurementType'].split()[0])

  #determine valid masks: loop through all entries and ensure that they all make sense
  self.valid = None
  for key in nameDict:
    if key in ['__ignore__','__note__']:
      continue
    for name, _ in nameDict[key]:
      if name in branch:
        data = np.array(branch[name], dtype=np.float64)
        mask = np.logical_and(np.isfinite(data), data<1e99)
        if self.valid is None:
          self.valid = mask
        else:
          self.valid = np.logical_and(self.valid, mask) #adopt/reduce mask continuously
        if key=='slope':
          self.valid = np.logical_and(self.valid, data>0.0)
        if key=='h':
          validFull = np.isfinite(np.array(branch[name], dtype=np.float64))
        break

  #Run through all items again and crop to only valid data
  for key in nameDict:
    if key in ['__ignore__','__note__']:
      continue
    for name, multiplyer in nameDict[key]:
      if name in branch:
        data = np.array(branch[name], dtype=np.float64)
        if key in ['h','p','t']:
          data = data[validFull]
        else:
          data = data[self.valid]
        setattr(self, key, data*multiplyer)
        inFile.remove(name)
        break

  # Test if essential items exist
  for attrib in ['h','t','p']:
    if not hasattr(self, attrib) or len(getattr(self, attrib))==0:
      print('Missing information for',self.metaUser['measurementType'].split()[0],': ',attrib)
      print('Keys exist',inFile)
  self.valid = self.valid[validFull]

  #cleaning
  self.p -= self.p[0]
  converter = self.datafile.attrs['uri'].split('/')[-1]
  if converter == 'hap2hdf.py':
    mask = np.array(self.h)>=0
    self.h = np.array(self.h)[mask]
    self.p = np.array(self.p)[mask]
    self.t = np.array(self.t)[mask]
    self.valid = self.valid[mask]
  inFile = [element for element in inFile if element not in nameDict['__ignore__']]
  if len(inFile)>0:
    print("**INFO on",self.metaUser['measurementType'].split()[0],"fields not imported:",inFile)
  if hasattr(self, 'slope') and len(self.slope)>60: #if more than 30: CSM
    self.method = Method.CSM
  self.identifyLoadHoldUnload()
  return True


def isfloat(value):
  """
  Determine if value is float

  Args:
    value: number to be tested
  """
  try:
    float(value)
    return True
  except ValueError:
    return False


def restartFile(self):
  """
  Restart processing the current file by resetting all values back to the initial
  """
  self.testList = list(self.allTestList)
  self.nextTest()
  return
